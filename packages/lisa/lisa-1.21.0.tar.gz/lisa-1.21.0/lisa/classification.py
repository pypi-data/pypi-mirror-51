# ! /usr/bin/python
# -*- coding: utf-8 -*-
from loguru import logger
# logger = logging.getLogger()

import numpy as np


class GMMClassifier():

    def __init__(self, each_class_params=None, **same_params):
        """
        same_params: classifier params for each class are same
        each_class_params: is list of dictionary of params for each
            class classifier. For example:
            [{'covariance_type': 'full'}, {'n_components': 2}])
        """
        self.same_params = same_params
        self.each_class_params = each_class_params

        self.models = []

    def fit(self, X_train, y_train):
        X_train = np.asarray(X_train)
        y_train = np.asarray(y_train)
        # from sklearn.mixture import GMM as GaussianMixture
        from sklearn.mixture import GaussianMixture

        unlabels = range(0, np.max(y_train) + 1)

        for lab in unlabels:
            if self.each_class_params is not None:
                # print 'eacl'
                # print self.each_class_params[lab]
                model = GaussianMixture(**self.each_class_params[lab])
                # print 'po gmm ', model
            elif len(self.same_params) > 0:
                model = GaussianMixture(**self.same_params)
                # print 'ewe ', model
            else:
                model = GaussianMixture()
            X_train_lab = X_train[y_train == lab]
            # logger.debug('xtr lab shape ' + str(X_train_lab))
            model.fit(X_train_lab)

            self.models.insert(lab, model)

    def __str__(self):
        if self.each_class_params is not None:
            return "GMMClassificator(" + str(self.each_class_params) + ')'
        else:
            return "GMMClassificator(" + str(self.same_params) + ')'

    def predict(self, X_test):
        X_test = np.asarray(X_test)

        logger.debug(str(X_test.shape))
        logger.debug(str(X_test))
        scores = np.zeros([X_test.shape[0], len(self.models)])

        for lab in range(0, len(self.models)):

            logger.debug('means shape' + str(self.models[lab].means_.shape))
            sc = self.models[lab].score_samples(X_test)
            scores[:, lab] = sc

        pred = np.argmax(scores, 1)

        return pred
