from pathlib import Path
import pandas as pd
from pandas.core.api import DataFrame as DataFrame
from src.ingestion.parsers.base import BaseParser


class DiscoverParser(BaseParser):
    def __init__(self):
        super().__init__('discover', 'credit_card')

    def _read_raw(self, filepath: Path) -> DataFrame:
        '''
        Reads a raw CSV of Discover data into a Pandas DataFrame

        Args:
            filepath (Path): Path to raw Discover CSV

        Returns:
            DataFrame: Raw Discover CSV DataFrame
        '''
        raw_df = pd.read_csv(filepath)

        # normalizing Discover column names
        raw_df.columns = raw_df.columns.str.strip().str.lower().str.replace('.', '',
                                                                            regex=False).str.replace(' ', '_')

        return raw_df

    def _normalize(self, df: DataFrame) -> DataFrame:
        '''
        Formats raw Discover DF into our schema

        Args:
            df (DataFrame): Raw dataframe of Discover CSV data

        Returns:
            DataFrame: Normalized Discover CSV dataframe
        '''

        normalized = pd.DataFrame()
        normalized['transaction_date'] = df['trans._date']
        normalized['post_date'] = df['post_date']
        normalized['original_description'] = df['description'].str.strip()
        normalized['description'] = normalized['original_description'].str.upper()
        normalized['amount'] = pd.to_numeric(
            df['amount'], errors='coerce') * -1
        normalized['category'] = df.get('category', None)

        return normalized
