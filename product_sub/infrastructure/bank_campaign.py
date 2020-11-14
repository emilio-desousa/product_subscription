import product_sub.settings as stg
import unidecode
import pandas as pd
from os.path import join
import numpy as np


class MarketingCampaign:
    """
    Performs technical cleaning on marketing campaign dataset

    Attributes
    ----------
    filename: string

    Properties
    ----------
    data: pandas.DataFrame
    """

    def __init__(self, filename):
        """Initialize Class

        Parameters
        ----------
        filename : string
            filename of dataset (must be csv for now)
        """
        self.filename = filename
        pass

    @property
    def data(self):
        """Technical cleaning of customers informations from flat files

        Returns
        -------
        DataFrame
            DataFrame technical cleaned (without accents, Yes/No)

        Raises
        ------
        FileExistsError
            The file must be a csv file for now
        """
        if self.filename.endswith(".csv"):
            df = pd.read_csv(join(stg.RAW_DATA_DIR, self.filename), sep=stg.SEP)
        else:
            raise FileExistsError("Extension must be csv.")

        df_bank = self._get_data_cleaned(df)
        return df_bank

    def _clean_accents(
        self, df, columns_to_clean_accents=[stg.COL_RAW_JOB, stg.COL_RAW_STATUS]
    ):
        df_without_accent = df.copy()
        for col in columns_to_clean_accents:
            df_without_accent[col] = (
                df[col]
                .str.normalize("NFKD")
                .str.encode("ascii", errors="ignore")
                .str.decode("utf-8")
            )
        return df_without_accent

    def _easy_yes_no_converter(
        self,
        df,
        cols_to_binary_convert=[
            stg.COL_RAW_SUBSCRIPTION,
            stg.COL_RAW_HAS_HOUSING_LOAN,
            stg.COL_RAW_HAS_PERSO_LOAN,
            stg.COL_RAW_HAS_DEFAULT,
        ],
    ):
        df_yes_no = df.copy()
        for col in cols_to_binary_convert:
            df_yes_no[col] = df[col].replace(stg.BOOLEAN_ENCODING)
        return df_yes_no

    def _get_data_cleaned(self, df):
        df_with_no_accents = self._clean_accents(df)
        df_with_no_yes_no = self._easy_yes_no_converter(df_with_no_accents)
        return df_with_no_yes_no


if __name__ == "__main__":
    objectMaerketing = MarketingCampaign("data.csv")
    df = objectMaerketing.data
    print(df)