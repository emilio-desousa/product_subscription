import product_sub.settings as stg
import unidecode
import pandas as pd
from os.path import join
import numpy as np


class EcoSocioContext:
    """
    Performs technical cleaning eco/social context dataset

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

        df_cleaned = self._clean_employ_rate_nan(df)
        return df_cleaned

    def _add_quarter(self, df):
        ##
        ## [HACK] Add one day to Date to get the good quarter
        ##
        df_quarter = df.assign(
            **{stg.COL_DATE_WITH_ONE: lambda df: pd.to_datetime(df[stg.COL_RAW_DATE]) + pd.DateOffset(1)}
        ).assign(**{stg.COL_QUARTER: lambda df: df[stg.COL_DATE_WITH_ONE].dt.to_period("Q")})

        return df_quarter

    def _clean_employ_rate_nan(self, df):
        df_with_quarter = self._add_quarter(df)
        empl_with_quarter = df_with_quarter.groupby(stg.COL_QUARTER)[stg.COL_RAW_EMPL_VAR_RATE].mean()

        df_with_quarter[stg.COL_RAW_EMPL_VAR_RATE] = df_with_quarter.apply(
            lambda x: empl_with_quarter[x[stg.COL_QUARTER]]
            if np.isnan(x[stg.COL_RAW_EMPL_VAR_RATE])
            else x[stg.COL_RAW_EMPL_VAR_RATE],
            axis=1,
        )
        df_with_quarter = df_with_quarter.drop(columns=[stg.COL_QUARTER, stg.COL_DATE_WITH_ONE])
        return df_with_quarter


if __name__ == "__main__":
    test = EcoSocioContext("socio_eco.csv").data
