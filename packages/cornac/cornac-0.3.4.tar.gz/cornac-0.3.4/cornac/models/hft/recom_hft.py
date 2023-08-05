# Copyright 2018 The Cornac Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

import numpy as np

from ..recommender import Recommender
from ...exception import ScoreException


class HFT(Recommender):
    """Collaborative Topic Regression

    Parameters
    ----------
    name: string, default: 'HFT'
        The name of the recommender model.

    k: int, optional, default: 10
        The dimension of the latent factors.

    max_iter: int, optional, default: 50
        Maximum number of iterations for EM step

    grad_iter: int, optional, default: 50
        Maximum number of iterations for l-bfgs

    init_params: dictionary, optional, default: None
        List of initial parameters, e.g., init_params = {'alpha':alpha,'beta_u':beta_u,'beta_i':beta_i,
        'gamma_u':gamma_u, 'gamma_v':gamma_v}

        alpha: float
            Model offset, optional initialization via init_params.

        beta_u: ndarray. shape (n_user, 1)
            User biases, optional initialization via init_params.

        beta_u: ndarray. shape (n_item, 1)
            Item biases, optional initialization via init_params.

        gamma_u: ndarray, shape (n_users,k)
            The user latent factors, optional initialization via init_params.

        gamma_v: ndarray, shape (n_items,k)
            The item latent factors, optional initialization via init_params.

    lambda_text: float, default : 0.1
        Weight of likelihood in loss function

    l2_reg: float, default : 0.001
        Regularization for user item latent factor

    vocab_size: int, optional, default: 8000
        Vocab size for auxiliary text data

    seed: int, optional, default: None
        Random seed for weight initialization.

    trainable: boolean, optional, default: True
        When False, the model is not trained and Cornac assumes that the model already
        pre-trained (gamma_u and gamma_v are not None).

    References
    ----------
    Julian McAuley, Jure Leskovec. "Hidden Factors and Hidden Topics: Understanding Rating Dimensions with Review Text"
    RecSys '13 Proceedings of the 7th ACM conference on Recommender systems Pages 165-172
    """

    def __init__(self, name='HFT', k=10, lambda_text=0.1, l2_reg=0.001, vocab_size=8000,
                 max_iter=50, grad_iter=50, trainable=True, verbose=True, init_params=None,
                 seed=None):
        super().__init__(name=name, trainable=trainable, verbose=verbose)
        self.k = k
        self.lambda_text = lambda_text
        self.l2_reg = l2_reg
        self.grad_iter = grad_iter
        self.name = name
        self.max_iter = max_iter
        self.verbose = verbose
        self.init_params = {} if not init_params else init_params
        self.seed = seed
        self.vocab_size = vocab_size

    def fit(self, train_set):
        """Fit the model to observations.

        Parameters
        ----------
        train_set: object of type TrainSet, required
            An object contraining the user-item preference in csr scipy sparse format,\
            as well as some useful attributes such as mappings to the original user/item ids.\
            Please refer to the class TrainSet in the "data" module for details.
        """
        Recommender.fit(self, train_set)
        from ...utils.init_utils import normal

        self.n_item = self.train_set.num_items
        self.n_user = self.train_set.num_users

        self.alpha = self.init_params.get('alpha', train_set.global_mean)
        self.beta_u = self.init_params.get('beta_u', normal(self.n_user, std=0.01, random_state=self.seed))
        self.beta_i = self.init_params.get('beta_i', normal(self.n_item, std=0.01, random_state=self.seed))
        self.gamma_u = self.init_params.get('gamma_u', normal((self.n_user, self.k), std=0.01, random_state=self.seed))
        self.gamma_i = self.init_params.get('gamma_i', normal((self.n_item, self.k), std=0.01, random_state=self.seed))

        if self.trainable:
            self._fit_hft()

    @staticmethod
    def _build_data(csr_mat):
        index_list = []
        rating_list = []
        for i in range(csr_mat.shape[0]):
            j, k = csr_mat.indptr[i], csr_mat.indptr[i + 1]
            index_list.append(csr_mat.indices[j:k])
            rating_list.append(csr_mat.data[j:k])
        return index_list, rating_list

    def _fit_hft(self):
        from .hft import Model
        from tqdm import trange

        # document data
        bow_mat = self.train_set.item_text.batch_bow(np.arange(self.n_item), keep_sparse=True)
        documents, _ = self._build_data(bow_mat)  # bag of word feature
        # Rating data
        user_data = self._build_data(self.train_set.matrix)
        item_data = self._build_data(self.train_set.matrix.T.tocsr())

        model = Model(n_user=self.n_user, n_item=self.n_item, alpha=self.alpha, beta_u=self.beta_u, beta_i=self.beta_i,
                      gamma_u=self.gamma_u, gamma_i=self.gamma_i, n_vocab=self.vocab_size, k=self.k,
                      lambda_text=self.lambda_text, l2_reg=self.l2_reg, grad_iter=self.grad_iter)

        model.init_count(docs=documents)

        # training
        loop = trange(self.max_iter, disable=not self.verbose)
        for _ in loop:
            model.assign_word_topics(docs=documents)
            loss = model.update_params(rating_data=(user_data, item_data))
            loop.set_postfix(loss=loss)

        self.alpha, self.beta_u, self.beta_i, self.gamma_u, self.gamma_i = model.get_parameter()

        if self.verbose:
            print('Learning completed!')

    def score(self, user_id, item_id=None):
        """Predict the scores/ratings of a user for an item.

        Parameters
        ----------
        user_id: int, required
            The index of the user for whom to perform score prediction.

        item_id: int, optional, default: None
            The index of the item for that to perform score prediction.
            If None, scores for all known items will be returned.

        Returns
        -------
        res : A scalar or a Numpy array
            Relative scores that the user gives to the item or to all known items
        """
        if item_id is None:
            if self.train_set.is_unk_user(user_id):
                raise ScoreException("Can't make score prediction for (user_id=%d)" % user_id)

            known_item_scores = self.alpha + self.beta_u[user_id] + self.beta_i + self.gamma_i.dot(
                self.gamma_u[user_id, :])
            return known_item_scores
        else:
            if self.train_set.is_unk_user(user_id) or self.train_set.is_unk_item(item_id):
                raise ScoreException("Can't make score prediction for (user_id=%d, item_id=%d)" % (user_id, item_id))

            user_pred = self.alpha + self.beta_u[user_id] + self.beta_i[item_id] + self.gamma_i[item_id, :].dot(
                self.gamma_u[user_id, :])

            return user_pred
