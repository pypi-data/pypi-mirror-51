# -*- coding: utf-8 -*-
from skydl.model.default_estimator_model import DefaultEstimatorModel
from tfv2 import iris_data
#########################
# 方便查看源代码
from tensorflow_estimator import estimator
from tensorflow.python import feature_column


class MyEstimatorModel(DefaultEstimatorModel):
    """
    tensorflow estimator model
    """
    def adjust_parse_args_value(self):
        super().adjust_parse_args_value()

    def load_data(self):
        # (train_x, train_y), (test_x, test_y) = iris_data.load_data()
        return iris_data.load_data()

    def fit(self):
        from tfv2 import iris_data
        batch_size = 128
        train_steps = 10
        (train_x, train_y), (test_x, test_y) = self.load_data()
        # Feature columns describe how to use the input.
        my_feature_columns = []
        for key in train_x.keys():
            my_feature_columns.append(feature_column.numeric_column(key=key))
        self.model.train(
            input_fn=lambda: iris_data.train_input_fn(train_x, train_y, batch_size),
            steps=train_steps)
        eval_result = self.model.evaluate(input_fn=lambda: iris_data.eval_input_fn(test_x, test_y, batch_size))
        print('\nTest set accuracy: {accuracy:0.3f}\n'.format(**eval_result))
        return self

    def fit2(self):
        import numpy as np
        import pandas as pd
        from matplotlib import pyplot as plt
        import tensorflow as tf
        #########################
        # 方便查看源代码
        from tensorflow_estimator import estimator
        from tensorflow.python import feature_column
        #########################

        # Load dataset.
        # dftrain = pd.read_csv('~/tensorflow_datasets/manual_downloads/titanic/train.csv')
        # dfeval = pd.read_csv('~/tensorflow_datasets/manual_downloads/titanic/eval.csv')
        dftrain = pd.read_csv('https://storage.googleapis.com/tf-datasets/titanic/train.csv')
        dfeval = pd.read_csv('https://storage.googleapis.com/tf-datasets/titanic/eval.csv')

        y_train = dftrain.pop('survived')
        y_eval = dfeval.pop('survived')

        tf.random.set_seed(123)

        fc = feature_column
        CATEGORICAL_COLUMNS = ['sex', 'n_siblings_spouses', 'parch', 'class', 'deck',
                               'embark_town', 'alone']
        NUMERIC_COLUMNS = ['age', 'fare']

        def one_hot_cat_column(feature_name, vocab):
            return feature_column.indicator_column(
                feature_column.categorical_column_with_vocabulary_list(feature_name,
                                                                       vocab))

        feature_columns = []
        for feature_name in CATEGORICAL_COLUMNS:
            # Need to one-hot encode categorical features.
            vocabulary = dftrain[feature_name].unique()
            feature_columns.append(one_hot_cat_column(feature_name, vocabulary))

        for feature_name in NUMERIC_COLUMNS:
            feature_columns.append(feature_column.numeric_column(feature_name,
                                                                 dtype=tf.float32))

        example = dict(dftrain.head(1))
        class_fc = feature_column.indicator_column(
            feature_column.categorical_column_with_vocabulary_list('class', ('First', 'Second', 'Third')))
        print('Feature value: "{}"'.format(example['class'].iloc[0]))
        print('One-hot encoded: ', tf.keras.layers.DenseFeatures([class_fc])(example).numpy())

        print(tf.keras.layers.DenseFeatures(feature_columns)(example).numpy())

        # Use entire batch since this is such a small dataset.
        NUM_EXAMPLES = len(y_train)

        def make_input_fn(X, y, n_epochs=None, shuffle=True):
            def input_fn():
                dataset = tf.data.Dataset.from_tensor_slices((dict(X), y))
                if shuffle:
                    dataset = dataset.shuffle(NUM_EXAMPLES)
                # For training, cycle thru dataset as many times as need (n_epochs=None).
                dataset = dataset.repeat(n_epochs)
                # In memory training doesn't use batching.
                dataset = dataset.batch(NUM_EXAMPLES)
                return dataset
            return input_fn

        # Training and evaluation input functions.
        train_input_fn = make_input_fn(dftrain, y_train)
        eval_input_fn = make_input_fn(dfeval, y_eval, shuffle=False, n_epochs=1)
        self.model.train(train_input_fn, max_steps=100)
        print("eval...........")
        result = self.model.evaluate(eval_input_fn)
        print(pd.Series(result))
        return self

    def evaluate(self, *args, **kwargs):
        return self

    def serving(self):
        return self

