import numpy as np
import pandas as pd
from sklearn.metrics import explained_variance_score
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error


def output_score(labels, predictions):
    labels = np.asarray(labels, dtype='float64')
    predictions = np.asarray(predictions, dtype='float64')

    print('explained_variance_score:', round(explained_variance_score(labels, predictions), 6))
    print('r2_score:                ', round(r2_score(labels, predictions), 6))
    print('mean_squared_error:      ', round(mean_squared_error(labels, predictions), 6))
    print('mean_absolute_error:     ', round(mean_absolute_error(labels, predictions), 6))
    print()


def output_feature_importance(model, features):
    importance = list(model.feature_importances_)
    feature_importance = [(feature, round(importance, 2)) for feature, importance in zip(features.columns, importance)]
    feature_importance = sorted(feature_importance, key=lambda x: x[1], reverse=True)
    [print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importance]


def read_model_data(filename='features.csv', label='green_energy'):
    potential_labels = ['solar_generation_kw', 'power_use_kw', 'wind_generation_kw', 'green_energy']

    features = pd.read_csv(filename, index_col=0, float_precision='high')
    features.drop(columns=[item for item in potential_labels if item != label], inplace=True)

    return features[label], features.drop(columns=[label])
