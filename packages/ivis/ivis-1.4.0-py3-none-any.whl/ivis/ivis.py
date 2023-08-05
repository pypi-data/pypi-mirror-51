""" scikit-learn wrapper class for the Ivis algorithm. """
from .data.triplet_generators import generator_from_index
from .nn.network import triplet_network, base_network
from .nn.callbacks import ModelCheckpoint
from .nn.losses import triplet_loss, is_categorical, is_multiclass, is_hinge
from .data.knn import build_annoy_index

from keras.callbacks import EarlyStopping
from keras.models import load_model, Model
from keras.layers import Dense, Input
from keras import regularizers
import numpy as np

from sklearn.base import BaseEstimator

import json
import os
import shutil
import multiprocessing
import tensorflow as tf


class Ivis(BaseEstimator):
    """Ivis is a technique that uses an artificial neural network for
    dimensionality reduction, often useful for the purposes of visualization.
    The network trains on triplets of data-points at a time and pulls positive
    points together, while pushing more distant points away from each other.
    Triplets are sampled from the original data using KNN aproximation using
    the Annoy library.

    :param int embedding_dims: Number of dimensions in the embedding space
    :param int k: The number of neighbours to retrieve for each point.
        Must be less than one minus the number of rows in the dataset.
    :param str distance: The loss function used to train the neural network.
        One of "pn", "euclidean", "manhattan_pn", "manhattan", "chebyshev",
        "chebyshev_pn", "softmax_ratio_pn", "softmax_ratio", "cosine",
        "cosine_pn".
    :param int batch_size: The size of mini-batches used during gradient
        descent while training the neural network. Must be less than the
        num_rows in the dataset.
    :param int epochs: The maximum number of epochs to train the model for.
        Each epoch the network will see a triplet based on each data-point
        once.
    :param int n_epochs_without_progress: After n number of epochs without an
        improvement to the loss, terminate training early.
    :param float margin: The distance that is enforced between points by the
        triplet loss functions.
    :param int ntrees: The number of random projections trees built by Annoy to
        approximate KNN. The more trees the higher the memory usage, but the
        better the accuracy of results.
    :param int search_k: The maximum number of nodes inspected during a nearest
        neighbour query by Annoy. The higher, the more computation time
        required, but the higher the accuracy. The default is n_trees * k,
        where k is the number of neighbours to retrieve. If this is set too
        low, a variable number of neighbours may be retrieved per data-point.
    :param bool precompute: Whether to pre-compute the nearest neighbours.
        Pre-computing is a little faster, but requires more memory. If memory
        is limited, try setting this to False.
    :param str model: str or keras.models.Model. The keras model to train using
        triplet loss. If a model object is provided, an embedding layer of size
        'embedding_dims' will be appended to the end of the network.
        If a string, a pre-defined network by that name will be used. Possible
        options are: 'default', 'hinton', 'maaten'. By default, a selu network
        composed of 3 dense layers of 128 neurons each will be created,
        followed by an embedding layer of size 'embedding_dims'.
    :param str supervision_metric: str or function. The supervision metric to
        optimize when training keras in supervised mode. Supports all of the
        classification or regression losses included with keras, so long as
        the labels are provided in the correct format. A list of keras' loss
        functions can be found at https://keras.io/losses/ .
    :param float supervision_weight: Float between 0 and 1 denoting the
        weighting to give to classification vs triplet loss when training
        in supervised mode. The higher the weight, the more classification
        influences training. Ignored if using Ivis in unsupervised mode.
    :param str annoy_index_path: The filepath of a pre-trained annoy index file
        saved on disk. If provided, the annoy index file will be used.
        Otherwise, a new index will be generated and saved to disk in the
        current directory as 'annoy.index'.
    :param list[keras.callbacks.Callback] callbacks: List of keras Callbacks to
        pass model during training, such as the TensorBoard callback. A set of
        ivis-specific callbacks are provided in the ivis.nn.callbacks module.
    :param int verbose: Controls the volume of logging output the model
        produces when training. When set to 0, silences outputs, when above 0
        will print outputs.

    """

    def __init__(self, embedding_dims=2, k=150, distance='pn', batch_size=128,
                 epochs=1000, n_epochs_without_progress=50,
                 margin=1, ntrees=50, search_k=-1,
                 precompute=True, model='default',
                 supervision_metric='sparse_categorical_crossentropy',
                 supervision_weight=0.5, annoy_index_path=None,
                 callbacks=[], verbose=1):

        self.embedding_dims = embedding_dims
        self.k = k
        self.distance = distance
        self.batch_size = batch_size
        self.epochs = epochs
        self.n_epochs_without_progress = n_epochs_without_progress
        self.margin = margin
        self.ntrees = ntrees
        self.search_k = search_k
        self.precompute = precompute
        self.model_def = model
        self.model_ = None
        self.encoder = None
        self.supervision_metric = supervision_metric
        self.supervision_weight = supervision_weight
        self.supervised_model_ = None
        self.loss_history_ = []
        self.annoy_index_path = annoy_index_path
        self.callbacks = callbacks
        for callback in self.callbacks:
            if isinstance(callback, ModelCheckpoint):
                callback = callback.register_ivis_model(self)
        self.verbose = verbose

    def __getstate__(self):
        """ Return object serializable variable dict """

        state = dict(self.__dict__)
        if 'model_' in state:
            state['model_'] = None
        if 'encoder' in state:
            state['encoder'] = None
        if 'supervised_model_' in state:
            state['supervised_model_'] = None
        if 'callbacks' in state:
            state['callbacks'] = []
        return state

    def _fit(self, X, Y=None, shuffle_mode=True):

        if self.annoy_index_path is None:
            self.annoy_index_path = 'annoy.index'
            if self.verbose > 0:
                print('Building KNN index')
            build_annoy_index(X, self.annoy_index_path,
                              ntrees=self.ntrees, verbose=self.verbose)

        datagen = generator_from_index(X, Y,
                                       index_path=self.annoy_index_path,
                                       k=self.k,
                                       batch_size=self.batch_size,
                                       search_k=self.search_k,
                                       precompute=self.precompute,
                                       verbose=self.verbose)

        loss_monitor = 'loss'
        try:
            triplet_loss_func = triplet_loss(distance=self.distance,
                                             margin=self.margin)
        except KeyError:
            raise ValueError('Loss function `{}` not implemented.'.format(self.distance))

        if self.model_ is None:
            if type(self.model_def) is str:
                input_size = (X.shape[-1],)
                self.model_, anchor_embedding, _, _ = \
                    triplet_network(base_network(self.model_def, input_size),
                                    embedding_dims=self.embedding_dims)
            else:
                self.model_, anchor_embedding, _, _ = \
                    triplet_network(self.model_def,
                                    embedding_dims=self.embedding_dims)

            if Y is None:
                self.model_.compile(optimizer='adam', loss=triplet_loss_func)
            else:
                if is_categorical(self.supervision_metric):
                    if not is_multiclass(self.supervision_metric):
                        if not is_hinge(self.supervision_metric):
                            # Binary logistic classifier
                            supervised_output = Dense(1, activation='sigmoid',
                                                      name='supervised')(anchor_embedding)
                        else:
                            # Binary Linear SVM output
                            supervised_output = Dense(1, activation='linear',
                                                      name='supervised',
                                                      kernel_regularizer=regularizers.l2())(anchor_embedding)
                    else:
                        n_classes = len(np.unique(Y, axis=0))
                        if not is_hinge(self.supervision_metric):
                            # Softmax classifier
                            supervised_output = Dense(n_classes, activation='softmax',
                                                      name='supervised')(anchor_embedding)
                        else:
                            # Multiclass Linear SVM output
                            supervised_output = Dense(n_classes, activation='linear',
                                                      name='supervised',
                                                      kernel_regularizer=regularizers.l2())(anchor_embedding)
                else:
                    # Regression
                    supervised_output = Dense(1, activation='linear',
                                              name='supervised')(anchor_embedding)

                final_network = Model(inputs=self.model_.inputs,
                                      outputs=[self.model_.output,
                                               supervised_output])
                self.model_ = final_network
                self.model_.compile(
                    optimizer='adam',
                    loss={
                        'stacked_triplets': triplet_loss_func,
                        'supervised': self.supervision_metric
                         },
                    loss_weights={
                        'stacked_triplets': 1 - self.supervision_weight,
                        'supervised': self.supervision_weight})

                # Store dedicated classification model
                supervised_model_input = Input(shape=(X.shape[-1],))
                embedding = self.model_.layers[3](supervised_model_input)
                softmax_out = self.model_.layers[-1](embedding)

                self.supervised_model_ = Model(supervised_model_input, softmax_out)

        self.encoder = self.model_.layers[3]

        if self.verbose > 0:
            print('Training neural network')

        hist = self.model_.fit_generator(
            datagen,
            steps_per_epoch=X.shape[0] // self.batch_size,
            epochs=self.epochs,
            callbacks=[callback for callback in self.callbacks] +
                      [EarlyStopping(monitor=loss_monitor,
                       patience=self.n_epochs_without_progress)],
            shuffle=shuffle_mode,
            workers=multiprocessing.cpu_count(),
            verbose=self.verbose)
        self.loss_history_ += hist.history['loss']

    def fit(self, X, Y=None, shuffle_mode=True):
        """Fit an ivis model.

        Parameters
        ----------
        X : array, shape (n_samples, n_features)
            Data to be embedded.
        Y : array, shape (n_samples)
            Optional array for supervised dimentionality reduction.

        Returns
        -------
        returns an instance of self
        """

        self._fit(X, Y, shuffle_mode)
        return self

    def fit_transform(self, X, Y=None, shuffle_mode=True):
        """Fit to data then transform

        Parameters
        ----------
        X : array, shape (n_samples, n_features)
            Data to be embedded.
        Y : array, shape (n_samples)
            Optional array for supervised dimentionality reduction.


        Returns
        -------
        X_new : transformed array, shape (n_samples, embedding_dims)
            Embedding of the new data in low-dimensional space.
        """

        self.fit(X, Y, shuffle_mode)
        return self.transform(X)

    def transform(self, X):
        """Transform X into the existing embedded space and return that
        transformed output.

        Parameters
        ----------
        X : array, shape (n_samples, n_features)
            New data to be transformed.

        Returns
        -------
        X_new : array, shape (n_samples, embedding_dims)
            Embedding of the new data in low-dimensional space.
        """

        embedding = self.encoder.predict(X, verbose=self.verbose)
        return embedding

    def score_samples(self, X):
        """Passes X through classification network to obtain predicted
        supervised values. Only applicable when trained in
        supervised mode.

        Parameters
        ----------
        X : array, shape (n_samples, n_features)
            Data to be passed through classification network.

        Returns
        -------
        X_new : array, shape (n_samples, embedding_dims)
            Softmax class probabilities of the data.
        """

        if self.supervised_model_ is None:
            raise Exception("Model was not trained in classification mode.")

        softmax_output = self.supervised_model_.predict(X)
        return softmax_output

    def save_model(self, folder_path, overwrite=False):
        """Save an ivis model

        Parameters
        ----------
        folder_path : string
            Path to serialised model files and metadata
        """

        if overwrite:
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
        os.makedirs(folder_path)
        # serialize weights to HDF5
        self.model_.save(os.path.join(folder_path, 'ivis_model.h5'))
        # Have to serialize supervised model separately
        if self.supervised_model_ is not None:
            self.supervised_model_.save(os.path.join(folder_path,
                                        'supervised_model.h5'))

        json.dump(self.__getstate__(),
                  open(os.path.join(folder_path, 'ivis_params.json'), 'w'))

    def load_model(self, folder_path):
        """Load ivis model

        Parameters
        ----------
        folder_path : string
            Path to serialised model files and metadata

        Returns
        -------
        returns an ivis instance
        """

        ivis_config = json.load(open(os.path.join(folder_path,
                                                  'ivis_params.json'), 'r'))
        self.__dict__ = ivis_config

        loss_function = triplet_loss(self.distance, self.margin)
        self.model_ = load_model(os.path.join(folder_path, 'ivis_model.h5'),
                                 custom_objects={'tf': tf,
                                                 loss_function.__name__: loss_function })
        self.encoder = self.model_.layers[3]
        self.encoder._make_predict_function()

        # If a supervised model exists, load it
        supervised_path = os.path.join(folder_path, 'supervised_model.h5')
        if os.path.exists(supervised_path):
            self.supervised_model_ = load_model(supervised_path)
        return self
