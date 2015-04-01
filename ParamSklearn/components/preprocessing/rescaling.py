from scipy import sparse

from HPOlibConfigSpace.configuration_space import ConfigurationSpace
from HPOlibConfigSpace.hyperparameters import CategoricalHyperparameter

from ParamSklearn.implementations.StandardScaler import StandardScaler
from ParamSklearn.implementations.MinMaxScaler import MinMaxScaler
from ParamSklearn.components.preprocessor_base import ParamSklearnPreprocessingAlgorithm
from ParamSklearn.util import DENSE, SPARSE, INPUT


class Rescaling(ParamSklearnPreprocessingAlgorithm):
    def __init__(self, strategy, random_state=None):
        # TODO pay attention to the cases when a copy is made
        self.strategy = strategy

    def fit(self, X, Y):
        if self.strategy == "min/max":
            self.preprocessor = MinMaxScaler(copy=False)
            # Fix numeric instabilities
            if sparse.issparse(X):
                X.data[X.data < 0] = 0
                X.data[X.data > 1] = 1
            else:
                X[X < 0] = 0
                X[X > 1] = 1
        elif self.strategy == "standard":
            self.preprocessor = StandardScaler(copy=False)
        else:
            raise ValueError(self.strategy)
        self.preprocessor.fit(X, Y)
        return self

    def transform(self, X):
        if self.preprocessor is None:
            raise NotImplementedError()
        return self.preprocessor.transform(X)

    @staticmethod
    def get_properties():
        return {'shortname': 'Rescaling',
                'name': 'Rescaling',
                'handles_missing_values': False,
                'handles_nominal_values': False,
                'handles_numerical_features': True,
                'prefers_data_scaled': False,
                'prefers_data_normalized': False,
                'handles_regression': True,
                'handles_classification': True,
                'handles_multiclass': True,
                'handles_multilabel': True,
                'is_deterministic': True,
                # TODO find out of this is right!
                'handles_sparse': True,
                'handles_dense': True,
                'input': (SPARSE, DENSE),
                'output': INPUT,
                # Add something here...
                'preferred_dtype': None}

    @staticmethod
    def get_hyperparameter_search_space(dataset_properties=None):
        # TODO add replace by zero!
        strategy = CategoricalHyperparameter(
            "strategy", ["min/max", "standard"], default="min/max")
        cs = ConfigurationSpace()
        cs.add_hyperparameter(strategy)
        return cs

    def __str__(self):
        name = self.get_properties()['name']
        return "ParamSklearn %s" % name