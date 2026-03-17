from locale import normalize
from pathlib import Path
import pandas as pd
from pandas.core.api import DataFrame as DataFrame
from src.ingestion.parsers.base import BaseParser


class WellsFargoParser(BaseParser):
    def __init__(self):
        super().__init__('wells_fargo', 'checking')

    def _read_raw(self, filepath: Path) -> DataFrame:
        """
        Reads a raw CSV of Wells Fargo activity data into a Pandas DataFrame

        Args:
            filepath (Path): Path to raw Wells Fargo CSV

        Returns:
            DataFrame: Raw Wells Fargo CSV DataFrame
        """

        raw_df = pd.read_csv(filepath,
                             header=None,
                             names=['date', 'amount', "star",
                                    "blank", "description"],
                             dtype=str,)

        return raw_df

    def _normalize(self, df: DataFrame) -> DataFrame:
        '''
        Formats raw Wells Fargo DF into our schema

        Args:
            df (DataFrame): Raw dataframe of Wells Farg CSV data

        Returns:
            DataFrame: Normalized Wells Fargo CSV dataframe
        '''
        normalized = pd.DataFrame()

        normalized['transacation_date'] = df['date']
        normalized['post_date'] = df['date']
        normalized['original_description'] = df['description'].str.strip()
        normalized['description'] = normalized['original_description'].str.upper()
        normalized['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        normalized['category'] = df.get('category', None)

        return normalized
