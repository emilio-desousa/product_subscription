from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd


class FrequencyEncoder(BaseEstimator, TransformerMixin):
    """Custom transformer to change categorical features into numerical ones, thanks to
        the frequency of each categorie


    Parameters
    ----------
    BaseEstimator
    TransformerMixin
    """

    def __init__(self, feature_names):
        """initilialize transformer with feature names to frequency encode

        Parameters
        ----------
        feature_names : list
            list of features names
        """
        self.feature_names = feature_names

    def fit(self, X, y=None):
        """get the frequency of each categorie

        Parameters
        ----------
        X : pandas.Dataframe
            DataFrame with only categorical features
        y : np.Array, optional
            targets, by default None

        Returns
        -------
        FrequencyEncoder
            instance of the object
        """
        frequency_array = []
        for feature in self.feature_names:
            frequency = X.groupby(feature).size() / len(X)
            frequency_array.append({"freq": frequency, "feature": feature})
        self.frequency_array = frequency_array
        return self

    def transform(self, X, y=None):
        """Transform categorical features into frequency

        Parameters
        ----------
        X : pandas.DataFrame
            DataFrame to frequency Encode
        y : np.Array, optional
            targets, by default None

        Returns
        -------
        pandas.DataFrame
            Dataframe with specified features frequency encoded
        """
        df_with_freq = X.copy()
        for dict_frequency in self.frequency_array:
            freq, feature = dict_frequency.values()
            df_with_freq = df_with_freq.assign(**{feature: lambda df: df[feature].map(freq).astype("float64")})
            # self._change_col_to_freq(X, **dict_frequency)
        return df_with_freq


class OneHotEncoder(BaseEstimator, TransformerMixin):
    """Custom Transformer to One Hot encode specified features
    why  own OneHotEncoder ? Because it is easier for our pipeline
    Parameters
    ----------
    BaseEstimator
    TransformerMixin
    """

    def __init__(self, feature_names):
        """Initialize custom transformer

        Parameters
        ----------
        feature_names : list
            list of feature names to onehot encode
        """
        self.feature_names = feature_names

    def fit(self, X, y=None):
        """fit transformer (nothing is done here)

        Parameters
        ----------
        X : pandas.DataFrame
            Dataframe to one hot encode
        y : np.Array, optional
            targets, by default None

        Returns
        -------
        OneHotEncoder Object
            Instance of OneHotEncoder
        """
        return self

    def transform(self, X, y=None):
        """Transform features to one hot encoded features: for each different values, create a new feature with one


        Parameters
        ----------
        X : pandas.Dataframe
            Dataframe to One Hot encode
        y : np.Array, optional
            targets, by default None

        Returns
        -------
        pandas.Dataframe
            dataframe one hot encoded
        """
        df_to_onehot = X.copy()
        for feature in self.feature_names:
            one_hot_df = pd.get_dummies(df_to_onehot[feature])
            df_to_onehot = df_to_onehot.drop(columns=feature)
            df_to_onehot = df_to_onehot.join(one_hot_df)
        # print(df_to_onehot)
        return df_to_onehot


class LabelEncoder(BaseEstimator, TransformerMixin):
    """Custom transformer to labelEncoder

    Parameters
    ----------
    BaseEstimator
    TransformerMixin
    """

    def __init__(self, feature_names):
        """Initialize custom transformer

        Parameters
        ----------
        feature_names : list
            list of feature names to label encoder
        """
        self.feature_names = feature_names

    def fit(self, X, y=None):
        """fit transformer (nothing is done here)

        Parameters
        ----------
        X : pandas.DataFrame
            Dataframe to one hot encode
        y : np.Array, optional
            targets, by default None

        Returns
        -------
        LabelEncoder Object
            Instance of LabelEncoder
        """
        return self

    def transform(self, X, y=None):
        """Transform features to label encoded ones => replace each value into number

        Parameters
        ----------
        X : pandas.DataFrame
            DataFrame to label encode
        y : np.Array, optional
            targets, by default None

        Returns
        -------
        pandas.Dataframe
            DataFrame with specified categorical features into numbers
        """
        df_to_label_encode = X.copy()
        for feature in self.feature_names:
            df_to_label_encode[feature] = df_to_label_encode[feature].cat.codes
        return df_to_label_encode
