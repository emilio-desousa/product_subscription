import product_sub.settings as stg
from product_sub.infrastructure.bank_campaign import MarketingCampaign
from product_sub.infrastructure.eco_social import EcoSocioContext
import unidecode
import pandas as pd
from os.path import join
import numpy as np


class DatasetBuilder:
    """Merge two Dataframes from flat files

    Attributes
    ----------
    dataset_marketing: pandas.DataFrame

    Methods
    -------
    merge

    """

    def __init__(self, filename_bank, filename_socio):
        """initialise class

        Parameters
        ----------
        filename_bank : string
            filename of the marketing campaign dataset (.csv)
        filename_socio : string
            filename of the eco/socio context dataset (.csv)
        """
        self.dataset_marketing = MarketingCampaign(filename=filename_bank).data
        self.dataset_socio = EcoSocioContext(filename=filename_socio).data

    def create_dataset(self):
        dataset_merged = self._merge()
        dataset_with_datetime_date = self._col_date_to_datetime(dataset_merged)
        dataset_with_month_and_weekday = self._add_month_weekday(
            dataset_with_datetime_date
        )
        return dataset_with_month_and_weekday.drop(columns=stg.COL_RAW_DATE)

    def _merge(self):
        """Merge Bank marketing Dataframe with eco/socio context Dataframe
        thanks to the DATE columns

        Returns
        -------
        pandas.DataFrame
            Merged DataFrame
        """
        (
            df_marketing_with_year_month,
            df_socio_with_year_month,
        ) = self._create_year_month_col()
        df_merged = pd.merge(
            df_marketing_with_year_month,
            df_socio_with_year_month,
            how="left",
            on=stg.COL_YEAR_MONTH,
        )

        cols_to_drop = [f"{stg.COL_RAW_DATE}_y", stg.COL_YEAR_MONTH]
        mapping_for_date = {f"{stg.COL_RAW_DATE}_x": stg.COL_RAW_DATE}
        df_merged_dropped = df_merged.drop(columns=cols_to_drop).rename(
            columns=mapping_for_date
        )
        return df_merged_dropped

    def _col_date_to_datetime(self, df):
        return df.assign(
            **{stg.COL_RAW_DATE: lambda df: pd.to_datetime(df[stg.COL_RAW_DATE])}
        )

    def _add_month_weekday(self, df):
        df_weekday_and_month = df.assign(
            **{stg.COL_MONTH: lambda df: df[stg.COL_RAW_DATE].dt.month},
            **{stg.COL_WEEKDAY: lambda df: df[stg.COL_RAW_DATE].dt.weekday},
        )
        return df_weekday_and_month

    def _create_year_month_col(self):
        df_market_year_month = self._add_year_month(self.dataset_marketing)
        df_socio_year_month = self._add_year_month(self.dataset_socio)
        return df_market_year_month, df_socio_year_month

    def _add_year_month(self, df):
        dataset_with_datetime_date = self._col_date_to_datetime(df)
        df_with_year_month = df.assign(
            **{
                stg.COL_YEAR_MONTH: lambda df: dataset_with_datetime_date[
                    stg.COL_RAW_DATE
                ].dt.to_period("M")
            }
        )
        return df_with_year_month


if __name__ == "__main__":
    data = DatasetBuilder("data.csv", "socio_eco.csv").create_dataset()
    print(data.info())