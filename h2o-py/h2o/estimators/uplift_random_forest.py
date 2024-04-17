#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# This file is auto-generated by h2o-3/h2o-bindings/bin/gen_python.py
# Copyright 2016 H2O.ai;  Apache License Version 2.0 (see LICENSE for details)
#

from h2o.estimators.estimator_base import H2OEstimator
from h2o.exceptions import H2OValueError
from h2o.frame import H2OFrame
from h2o.utils.typechecks import assert_is_type, Enum, numeric


class H2OUpliftRandomForestEstimator(H2OEstimator):
    """
    Uplift Distributed Random Forest

    Build a Uplift Random Forest model

    Builds a Uplift Random Forest model on an H2OFrame.
    """

    algo = "upliftdrf"
    supervised_learning = True
    _options_ = {'model_extensions': ['h2o.model.extensions.VariableImportance'],
                 'verbose': True}

    def __init__(self,
                 model_id=None,  # type: Optional[Union[None, str, H2OEstimator]]
                 training_frame=None,  # type: Optional[Union[None, str, H2OFrame]]
                 validation_frame=None,  # type: Optional[Union[None, str, H2OFrame]]
                 score_each_iteration=False,  # type: bool
                 score_tree_interval=0,  # type: int
                 response_column=None,  # type: Optional[str]
                 ignored_columns=None,  # type: Optional[List[str]]
                 ignore_const_cols=True,  # type: bool
                 ntrees=50,  # type: int
                 max_depth=20,  # type: int
                 min_rows=1.0,  # type: float
                 nbins=20,  # type: int
                 nbins_top_level=1024,  # type: int
                 nbins_cats=1024,  # type: int
                 max_runtime_secs=0.0,  # type: float
                 seed=-1,  # type: int
                 mtries=-2,  # type: int
                 sample_rate=0.632,  # type: float
                 sample_rate_per_class=None,  # type: Optional[List[float]]
                 col_sample_rate_change_per_level=1.0,  # type: float
                 col_sample_rate_per_tree=1.0,  # type: float
                 histogram_type="auto",  # type: Literal["auto", "uniform_adaptive", "random", "quantiles_global", "round_robin", "uniform_robust"]
                 categorical_encoding="auto",  # type: Literal["auto", "enum", "one_hot_internal", "one_hot_explicit", "binary", "eigen", "label_encoder", "sort_by_response", "enum_limited"]
                 distribution="auto",  # type: Literal["auto", "bernoulli"]
                 check_constant_response=True,  # type: bool
                 custom_metric_func=None,  # type: Optional[str]
                 treatment_column="treatment",  # type: str
                 uplift_metric="auto",  # type: Literal["auto", "kl", "euclidean", "chi_squared"]
                 auuc_type="auto",  # type: Literal["auto", "qini", "lift", "gain"]
                 auuc_nbins=-1,  # type: int
                 stopping_rounds=0,  # type: int
                 stopping_metric="auto",  # type: Literal["auto", "auuc", "ate", "att", "atc", "qini"]
                 stopping_tolerance=0.001,  # type: float
                 ):
        """
        :param model_id: Destination id for this model; auto-generated if not specified.
               Defaults to ``None``.
        :type model_id: Union[None, str, H2OEstimator], optional
        :param training_frame: Id of the training data frame.
               Defaults to ``None``.
        :type training_frame: Union[None, str, H2OFrame], optional
        :param validation_frame: Id of the validation data frame.
               Defaults to ``None``.
        :type validation_frame: Union[None, str, H2OFrame], optional
        :param score_each_iteration: Whether to score during each iteration of model training.
               Defaults to ``False``.
        :type score_each_iteration: bool
        :param score_tree_interval: Score the model after every so many trees. Disabled if set to 0.
               Defaults to ``0``.
        :type score_tree_interval: int
        :param response_column: Response variable column.
               Defaults to ``None``.
        :type response_column: str, optional
        :param ignored_columns: Names of columns to ignore for training.
               Defaults to ``None``.
        :type ignored_columns: List[str], optional
        :param ignore_const_cols: Ignore constant columns.
               Defaults to ``True``.
        :type ignore_const_cols: bool
        :param ntrees: Number of trees.
               Defaults to ``50``.
        :type ntrees: int
        :param max_depth: Maximum tree depth (0 for unlimited).
               Defaults to ``20``.
        :type max_depth: int
        :param min_rows: Fewest allowed (weighted) observations in a leaf.
               Defaults to ``1.0``.
        :type min_rows: float
        :param nbins: For numerical columns (real/int), build a histogram of (at least) this many bins, then split at
               the best point
               Defaults to ``20``.
        :type nbins: int
        :param nbins_top_level: For numerical columns (real/int), build a histogram of (at most) this many bins at the
               root level, then decrease by factor of two per level
               Defaults to ``1024``.
        :type nbins_top_level: int
        :param nbins_cats: For categorical columns (factors), build a histogram of this many bins, then split at the
               best point. Higher values can lead to more overfitting.
               Defaults to ``1024``.
        :type nbins_cats: int
        :param max_runtime_secs: Maximum allowed runtime in seconds for model training. Use 0 to disable.
               Defaults to ``0.0``.
        :type max_runtime_secs: float
        :param seed: Seed for pseudo random number generator (if applicable)
               Defaults to ``-1``.
        :type seed: int
        :param mtries: Number of variables randomly sampled as candidates at each split. If set to -1, defaults to
               sqrt{p} for classification and p/3 for regression (where p is the # of predictors
               Defaults to ``-2``.
        :type mtries: int
        :param sample_rate: Row sample rate per tree (from 0.0 to 1.0)
               Defaults to ``0.632``.
        :type sample_rate: float
        :param sample_rate_per_class: A list of row sample rates per class (relative fraction for each class, from 0.0
               to 1.0), for each tree
               Defaults to ``None``.
        :type sample_rate_per_class: List[float], optional
        :param col_sample_rate_change_per_level: Relative change of the column sampling rate for every level (must be >
               0.0 and <= 2.0)
               Defaults to ``1.0``.
        :type col_sample_rate_change_per_level: float
        :param col_sample_rate_per_tree: Column sample rate per tree (from 0.0 to 1.0)
               Defaults to ``1.0``.
        :type col_sample_rate_per_tree: float
        :param histogram_type: What type of histogram to use for finding optimal split points
               Defaults to ``"auto"``.
        :type histogram_type: Literal["auto", "uniform_adaptive", "random", "quantiles_global", "round_robin", "uniform_robust"]
        :param categorical_encoding: Encoding scheme for categorical features
               Defaults to ``"auto"``.
        :type categorical_encoding: Literal["auto", "enum", "one_hot_internal", "one_hot_explicit", "binary", "eigen", "label_encoder",
               "sort_by_response", "enum_limited"]
        :param distribution: Distribution function
               Defaults to ``"auto"``.
        :type distribution: Literal["auto", "bernoulli"]
        :param check_constant_response: Check if response column is constant. If enabled, then an exception is thrown if
               the response column is a constant value.If disabled, then model will train regardless of the response
               column being a constant value or not.
               Defaults to ``True``.
        :type check_constant_response: bool
        :param custom_metric_func: Reference to custom evaluation function, format: `language:keyName=funcName`
               Defaults to ``None``.
        :type custom_metric_func: str, optional
        :param treatment_column: Define the column which will be used for computing uplift gain to select best split for
               a tree. The column has to divide the dataset into treatment (value 1) and control (value 0) groups.
               Defaults to ``"treatment"``.
        :type treatment_column: str
        :param uplift_metric: Divergence metric used to find best split when building an uplift tree.
               Defaults to ``"auto"``.
        :type uplift_metric: Literal["auto", "kl", "euclidean", "chi_squared"]
        :param auuc_type: Metric used to calculate Area Under Uplift Curve.
               Defaults to ``"auto"``.
        :type auuc_type: Literal["auto", "qini", "lift", "gain"]
        :param auuc_nbins: Number of bins to calculate Area Under Uplift Curve.
               Defaults to ``-1``.
        :type auuc_nbins: int
        :param stopping_rounds: Early stopping based on convergence of stopping_metric. Stop if simple moving average of
               length k of the stopping_metric does not improve for k:=stopping_rounds scoring events (0 to disable)
               Defaults to ``0``.
        :type stopping_rounds: int
        :param stopping_metric: Metric to use for early stopping (AUTO: logloss for classification, deviance for
               regression and anomaly_score for Isolation Forest). Note that custom and custom_increasing can only be
               used in GBM and DRF with the Python client.
               Defaults to ``"auto"``.
        :type stopping_metric: Literal["auto", "auuc", "ate", "att", "atc", "qini"]
        :param stopping_tolerance: Relative tolerance for metric-based stopping criterion (stop if relative improvement
               is not at least this much)
               Defaults to ``0.001``.
        :type stopping_tolerance: float
        """
        super(H2OUpliftRandomForestEstimator, self).__init__()
        self._parms = {}
        self._id = self._parms['model_id'] = model_id
        self.training_frame = training_frame
        self.validation_frame = validation_frame
        self.score_each_iteration = score_each_iteration
        self.score_tree_interval = score_tree_interval
        self.response_column = response_column
        self.ignored_columns = ignored_columns
        self.ignore_const_cols = ignore_const_cols
        self.ntrees = ntrees
        self.max_depth = max_depth
        self.min_rows = min_rows
        self.nbins = nbins
        self.nbins_top_level = nbins_top_level
        self.nbins_cats = nbins_cats
        self.max_runtime_secs = max_runtime_secs
        self.seed = seed
        self.mtries = mtries
        self.sample_rate = sample_rate
        self.sample_rate_per_class = sample_rate_per_class
        self.col_sample_rate_change_per_level = col_sample_rate_change_per_level
        self.col_sample_rate_per_tree = col_sample_rate_per_tree
        self.histogram_type = histogram_type
        self.categorical_encoding = categorical_encoding
        self.distribution = distribution
        self.check_constant_response = check_constant_response
        self.custom_metric_func = custom_metric_func
        self.treatment_column = treatment_column
        self.uplift_metric = uplift_metric
        self.auuc_type = auuc_type
        self.auuc_nbins = auuc_nbins
        self.stopping_rounds = stopping_rounds
        self.stopping_metric = stopping_metric
        self.stopping_tolerance = stopping_tolerance

    @property
    def training_frame(self):
        """
        Id of the training data frame.

        Type: ``Union[None, str, H2OFrame]``.
        """
        return self._parms.get("training_frame")

    @training_frame.setter
    def training_frame(self, training_frame):
        self._parms["training_frame"] = H2OFrame._validate(training_frame, 'training_frame')

    @property
    def validation_frame(self):
        """
        Id of the validation data frame.

        Type: ``Union[None, str, H2OFrame]``.
        """
        return self._parms.get("validation_frame")

    @validation_frame.setter
    def validation_frame(self, validation_frame):
        self._parms["validation_frame"] = H2OFrame._validate(validation_frame, 'validation_frame')

    @property
    def score_each_iteration(self):
        """
        Whether to score during each iteration of model training.

        Type: ``bool``, defaults to ``False``.
        """
        return self._parms.get("score_each_iteration")

    @score_each_iteration.setter
    def score_each_iteration(self, score_each_iteration):
        assert_is_type(score_each_iteration, None, bool)
        self._parms["score_each_iteration"] = score_each_iteration

    @property
    def score_tree_interval(self):
        """
        Score the model after every so many trees. Disabled if set to 0.

        Type: ``int``, defaults to ``0``.
        """
        return self._parms.get("score_tree_interval")

    @score_tree_interval.setter
    def score_tree_interval(self, score_tree_interval):
        assert_is_type(score_tree_interval, None, int)
        self._parms["score_tree_interval"] = score_tree_interval

    @property
    def response_column(self):
        """
        Response variable column.

        Type: ``str``.
        """
        return self._parms.get("response_column")

    @response_column.setter
    def response_column(self, response_column):
        assert_is_type(response_column, None, str)
        self._parms["response_column"] = response_column

    @property
    def ignored_columns(self):
        """
        Names of columns to ignore for training.

        Type: ``List[str]``.
        """
        return self._parms.get("ignored_columns")

    @ignored_columns.setter
    def ignored_columns(self, ignored_columns):
        assert_is_type(ignored_columns, None, [str])
        self._parms["ignored_columns"] = ignored_columns

    @property
    def ignore_const_cols(self):
        """
        Ignore constant columns.

        Type: ``bool``, defaults to ``True``.
        """
        return self._parms.get("ignore_const_cols")

    @ignore_const_cols.setter
    def ignore_const_cols(self, ignore_const_cols):
        assert_is_type(ignore_const_cols, None, bool)
        self._parms["ignore_const_cols"] = ignore_const_cols

    @property
    def ntrees(self):
        """
        Number of trees.

        Type: ``int``, defaults to ``50``.
        """
        return self._parms.get("ntrees")

    @ntrees.setter
    def ntrees(self, ntrees):
        assert_is_type(ntrees, None, int)
        self._parms["ntrees"] = ntrees

    @property
    def max_depth(self):
        """
        Maximum tree depth (0 for unlimited).

        Type: ``int``, defaults to ``20``.
        """
        return self._parms.get("max_depth")

    @max_depth.setter
    def max_depth(self, max_depth):
        assert_is_type(max_depth, None, int)
        self._parms["max_depth"] = max_depth

    @property
    def min_rows(self):
        """
        Fewest allowed (weighted) observations in a leaf.

        Type: ``float``, defaults to ``1.0``.
        """
        return self._parms.get("min_rows")

    @min_rows.setter
    def min_rows(self, min_rows):
        assert_is_type(min_rows, None, numeric)
        self._parms["min_rows"] = min_rows

    @property
    def nbins(self):
        """
        For numerical columns (real/int), build a histogram of (at least) this many bins, then split at the best point

        Type: ``int``, defaults to ``20``.
        """
        return self._parms.get("nbins")

    @nbins.setter
    def nbins(self, nbins):
        assert_is_type(nbins, None, int)
        self._parms["nbins"] = nbins

    @property
    def nbins_top_level(self):
        """
        For numerical columns (real/int), build a histogram of (at most) this many bins at the root level, then decrease
        by factor of two per level

        Type: ``int``, defaults to ``1024``.
        """
        return self._parms.get("nbins_top_level")

    @nbins_top_level.setter
    def nbins_top_level(self, nbins_top_level):
        assert_is_type(nbins_top_level, None, int)
        self._parms["nbins_top_level"] = nbins_top_level

    @property
    def nbins_cats(self):
        """
        For categorical columns (factors), build a histogram of this many bins, then split at the best point. Higher
        values can lead to more overfitting.

        Type: ``int``, defaults to ``1024``.
        """
        return self._parms.get("nbins_cats")

    @nbins_cats.setter
    def nbins_cats(self, nbins_cats):
        assert_is_type(nbins_cats, None, int)
        self._parms["nbins_cats"] = nbins_cats

    @property
    def max_runtime_secs(self):
        """
        Maximum allowed runtime in seconds for model training. Use 0 to disable.

        Type: ``float``, defaults to ``0.0``.
        """
        return self._parms.get("max_runtime_secs")

    @max_runtime_secs.setter
    def max_runtime_secs(self, max_runtime_secs):
        assert_is_type(max_runtime_secs, None, numeric)
        self._parms["max_runtime_secs"] = max_runtime_secs

    @property
    def seed(self):
        """
        Seed for pseudo random number generator (if applicable)

        Type: ``int``, defaults to ``-1``.
        """
        return self._parms.get("seed")

    @seed.setter
    def seed(self, seed):
        assert_is_type(seed, None, int)
        self._parms["seed"] = seed

    @property
    def mtries(self):
        """
        Number of variables randomly sampled as candidates at each split. If set to -1, defaults to sqrt{p} for
        classification and p/3 for regression (where p is the # of predictors

        Type: ``int``, defaults to ``-2``.
        """
        return self._parms.get("mtries")

    @mtries.setter
    def mtries(self, mtries):
        assert_is_type(mtries, None, int)
        self._parms["mtries"] = mtries

    @property
    def sample_rate(self):
        """
        Row sample rate per tree (from 0.0 to 1.0)

        Type: ``float``, defaults to ``0.632``.
        """
        return self._parms.get("sample_rate")

    @sample_rate.setter
    def sample_rate(self, sample_rate):
        assert_is_type(sample_rate, None, numeric)
        self._parms["sample_rate"] = sample_rate

    @property
    def sample_rate_per_class(self):
        """
        A list of row sample rates per class (relative fraction for each class, from 0.0 to 1.0), for each tree

        Type: ``List[float]``.
        """
        return self._parms.get("sample_rate_per_class")

    @sample_rate_per_class.setter
    def sample_rate_per_class(self, sample_rate_per_class):
        assert_is_type(sample_rate_per_class, None, [numeric])
        self._parms["sample_rate_per_class"] = sample_rate_per_class

    @property
    def col_sample_rate_change_per_level(self):
        """
        Relative change of the column sampling rate for every level (must be > 0.0 and <= 2.0)

        Type: ``float``, defaults to ``1.0``.
        """
        return self._parms.get("col_sample_rate_change_per_level")

    @col_sample_rate_change_per_level.setter
    def col_sample_rate_change_per_level(self, col_sample_rate_change_per_level):
        assert_is_type(col_sample_rate_change_per_level, None, numeric)
        self._parms["col_sample_rate_change_per_level"] = col_sample_rate_change_per_level

    @property
    def col_sample_rate_per_tree(self):
        """
        Column sample rate per tree (from 0.0 to 1.0)

        Type: ``float``, defaults to ``1.0``.
        """
        return self._parms.get("col_sample_rate_per_tree")

    @col_sample_rate_per_tree.setter
    def col_sample_rate_per_tree(self, col_sample_rate_per_tree):
        assert_is_type(col_sample_rate_per_tree, None, numeric)
        self._parms["col_sample_rate_per_tree"] = col_sample_rate_per_tree

    @property
    def histogram_type(self):
        """
        What type of histogram to use for finding optimal split points

        Type: ``Literal["auto", "uniform_adaptive", "random", "quantiles_global", "round_robin", "uniform_robust"]``,
        defaults to ``"auto"``.
        """
        return self._parms.get("histogram_type")

    @histogram_type.setter
    def histogram_type(self, histogram_type):
        assert_is_type(histogram_type, None, Enum("auto", "uniform_adaptive", "random", "quantiles_global", "round_robin", "uniform_robust"))
        self._parms["histogram_type"] = histogram_type

    @property
    def categorical_encoding(self):
        """
        Encoding scheme for categorical features

        Type: ``Literal["auto", "enum", "one_hot_internal", "one_hot_explicit", "binary", "eigen", "label_encoder",
        "sort_by_response", "enum_limited"]``, defaults to ``"auto"``.
        """
        return self._parms.get("categorical_encoding")

    @categorical_encoding.setter
    def categorical_encoding(self, categorical_encoding):
        assert_is_type(categorical_encoding, None, Enum("auto", "enum", "one_hot_internal", "one_hot_explicit", "binary", "eigen", "label_encoder", "sort_by_response", "enum_limited"))
        self._parms["categorical_encoding"] = categorical_encoding

    @property
    def distribution(self):
        """
        Distribution function

        Type: ``Literal["auto", "bernoulli"]``, defaults to ``"auto"``.
        """
        return self._parms.get("distribution")

    @distribution.setter
    def distribution(self, distribution):
        assert_is_type(distribution, None, Enum("auto", "bernoulli"))
        self._parms["distribution"] = distribution

    @property
    def check_constant_response(self):
        """
        Check if response column is constant. If enabled, then an exception is thrown if the response column is a
        constant value.If disabled, then model will train regardless of the response column being a constant value or
        not.

        Type: ``bool``, defaults to ``True``.
        """
        return self._parms.get("check_constant_response")

    @check_constant_response.setter
    def check_constant_response(self, check_constant_response):
        assert_is_type(check_constant_response, None, bool)
        self._parms["check_constant_response"] = check_constant_response

    @property
    def custom_metric_func(self):
        """
        Reference to custom evaluation function, format: `language:keyName=funcName`

        Type: ``str``.
        """
        return self._parms.get("custom_metric_func")

    @custom_metric_func.setter
    def custom_metric_func(self, custom_metric_func):
        assert_is_type(custom_metric_func, None, str)
        self._parms["custom_metric_func"] = custom_metric_func

    @property
    def treatment_column(self):
        """
        Define the column which will be used for computing uplift gain to select best split for a tree. The column has
        to divide the dataset into treatment (value 1) and control (value 0) groups.

        Type: ``str``, defaults to ``"treatment"``.

        :examples:

        >>> import h2o
        >>> from h2o.estimators import H2OUpliftRandomForestEstimator
        >>> h2o.init()
        >>> data = h2o.import_file("https://s3.amazonaws.com/h2o-public-test-data/smalldata/uplift/criteo_uplift_13k.csv")
        >>> predictors = ["f1", "f2", "f3", "f4", "f5", "f6","f7", "f8"]
        >>> response = "conversion"
        >>> data[response] = data[response].asfactor()
        >>> treatment_column = "treatment"
        >>> data[treatment_column] = data[treatment_column].asfactor()
        >>> train, valid = data.split_frame(ratios=[.8], seed=1234)
        >>> uplift_model = H2OUpliftRandomForestEstimator(ntrees=10,
        ...                                               max_depth=5,
        ...                                               uplift_metric="KL",
        ...                                               min_rows=10,
        ...                                               seed=1234,
        ...                                               auuc_type="qini",
...                                               treatment_column=treatment_column)
        >>> uplift_model.train(x=predictors,
        ...                    y=response,
        ...                    training_frame=train,
        ...                    validation_frame=valid)
        >>> uplift_model.model_performance()
        """
        return self._parms.get("treatment_column")

    @treatment_column.setter
    def treatment_column(self, treatment_column):
        assert_is_type(treatment_column, None, str)
        self._parms["treatment_column"] = treatment_column

    @property
    def uplift_metric(self):
        """
        Divergence metric used to find best split when building an uplift tree.

        Type: ``Literal["auto", "kl", "euclidean", "chi_squared"]``, defaults to ``"auto"``.

        :examples:

        >>> import h2o
        >>> from h2o.estimators import H2OUpliftRandomForestEstimator
        >>> h2o.init()
        >>> data = h2o.import_file("https://s3.amazonaws.com/h2o-public-test-data/smalldata/uplift/criteo_uplift_13k.csv")
        >>> predictors = ["f1", "f2", "f3", "f4", "f5", "f6","f7", "f8"]
        >>> response = "conversion"
        >>> data[response] = data[response].asfactor()
        >>> treatment_column = "treatment"
        >>> data[treatment_column] = data[treatment_column].asfactor()
        >>> train, valid = data.split_frame(ratios=[.8], seed=1234)
        >>> uplift_model = H2OUpliftRandomForestEstimator(ntrees=10,
        ...                                               max_depth=5,
        ...                                               min_rows=10,
        ...                                               seed=1234,
        ...                                               auuc_type="qini",
        ...                                               treatment_column="treatment",
        ...                                               uplift_metric="auto")
        >>> uplift_model.train(x=predictors,
        ...                    y=response,
        ...                    training_frame=train,
        ...                    validation_frame=valid)
        >>> uplift_model.model_performance()
        """
        return self._parms.get("uplift_metric")

    @uplift_metric.setter
    def uplift_metric(self, uplift_metric):
        assert_is_type(uplift_metric, None, Enum("auto", "kl", "euclidean", "chi_squared"))
        self._parms["uplift_metric"] = uplift_metric

    @property
    def auuc_type(self):
        """
        Metric used to calculate Area Under Uplift Curve.

        Type: ``Literal["auto", "qini", "lift", "gain"]``, defaults to ``"auto"``.

        :examples:

        >>> import h2o
        >>> from h2o.estimators import H2OUpliftRandomForestEstimator
        >>> h2o.init()
        >>> data = h2o.import_file("https://s3.amazonaws.com/h2o-public-test-data/smalldata/uplift/criteo_uplift_13k.csv")
        >>> predictors = ["f1", "f2", "f3", "f4", "f5", "f6","f7", "f8"]
        >>> response = "conversion"
        >>> data[response] = data[response].asfactor()
        >>> treatment_column = "treatment"
        >>> data[treatment_column] = data[treatment_column].asfactor()
        >>> train, valid = data.split_frame(ratios=[.8], seed=1234)
        >>> uplift_model = H2OUpliftRandomForestEstimator(ntrees=10,
        ...                                               max_depth=5,
        ...                                               treatment_column=treatment_column,
        ...                                               uplift_metric="KL",
        ...                                               min_rows=10,
        ...                                               seed=1234,
        ...                                               auuc_type="qini")
        >>> uplift_model.train(x=predictors,
        ...                    y=response,
        ...                    training_frame=train,
        ...                    validation_frame=valid)
        >>> uplift_model.model_performance()
        """
        return self._parms.get("auuc_type")

    @auuc_type.setter
    def auuc_type(self, auuc_type):
        assert_is_type(auuc_type, None, Enum("auto", "qini", "lift", "gain"))
        self._parms["auuc_type"] = auuc_type

    @property
    def auuc_nbins(self):
        """
        Number of bins to calculate Area Under Uplift Curve.

        Type: ``int``, defaults to ``-1``.

        :examples:

        >>> import h2o
        >>> from h2o.estimators import H2OUpliftRandomForestEstimator
        >>> h2o.init()
        >>> data = h2o.import_file("https://s3.amazonaws.com/h2o-public-test-data/smalldata/uplift/criteo_uplift_13k.csv")
        >>> predictors = ["f1", "f2", "f3", "f4", "f5", "f6","f7", "f8"]
        >>> response = "conversion"
        >>> data[response] = data[response].asfactor()
        >>> treatment_column = "treatment"
        >>> data[treatment_column] = data[treatment_column].asfactor()
        >>> train, valid = data.split_frame(ratios=[.8], seed=1234)
        >>> uplift_model = H2OUpliftRandomForestEstimator(ntrees=10,
        ...                                               max_depth=5,
        ...                                               treatment_column=treatment_column,
        ...                                               uplift_metric="KL",
        ...                                               min_rows=10,
        ...                                               seed=1234,
        ...                                               auuc_type="qini",
        ...                                               auuc_nbins=100)
        >>> uplift_model.train(x=predictors,
        ...                    y=response,
        ...                    training_frame=train,
        ...                    validation_frame=valid)
        >>> uplift_model.model_performance()
        """
        return self._parms.get("auuc_nbins")

    @auuc_nbins.setter
    def auuc_nbins(self, auuc_nbins):
        assert_is_type(auuc_nbins, None, int)
        self._parms["auuc_nbins"] = auuc_nbins

    @property
    def stopping_rounds(self):
        """
        Early stopping based on convergence of stopping_metric. Stop if simple moving average of length k of the
        stopping_metric does not improve for k:=stopping_rounds scoring events (0 to disable)

        Type: ``int``, defaults to ``0``.
        """
        return self._parms.get("stopping_rounds")

    @stopping_rounds.setter
    def stopping_rounds(self, stopping_rounds):
        assert_is_type(stopping_rounds, None, int)
        self._parms["stopping_rounds"] = stopping_rounds

    @property
    def stopping_metric(self):
        """
        Metric to use for early stopping (AUTO: logloss for classification, deviance for regression and anomaly_score
        for Isolation Forest). Note that custom and custom_increasing can only be used in GBM and DRF with the Python
        client.

        Type: ``Literal["auto", "auuc", "ate", "att", "atc", "qini"]``, defaults to ``"auto"``.
        """
        return self._parms.get("stopping_metric")

    @stopping_metric.setter
    def stopping_metric(self, stopping_metric):
        assert_is_type(stopping_metric, None, Enum("auto", "auuc", "ate", "att", "atc", "qini"))
        self._parms["stopping_metric"] = stopping_metric

    @property
    def stopping_tolerance(self):
        """
        Relative tolerance for metric-based stopping criterion (stop if relative improvement is not at least this much)

        Type: ``float``, defaults to ``0.001``.
        """
        return self._parms.get("stopping_tolerance")

    @stopping_tolerance.setter
    def stopping_tolerance(self, stopping_tolerance):
        assert_is_type(stopping_tolerance, None, numeric)
        self._parms["stopping_tolerance"] = stopping_tolerance


