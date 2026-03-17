from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd
import hashlib


class BaseParser(ABC):
    """
    Base parser class that different bank parser objects will inherit from to parse CSV exports
    """

    def __init__(self, source_bank: str, account_type: str):
        self.source_bank = source_bank
        self.account_type = account_type

    @abstractmethod
    def _read_raw(self, filepath: Path) -> pd.DataFrame:
        """
        Reads the bank-specific CSV into a raw DataFrame
        Args:
            filepath (Path): File path of raw bank export CSV 
        """
        pass

    @abstractmethod
    def _normalize(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Takes raw DF and transforms it to normalized schema from config. Does
        column renaming, sign flipping, and type casting

        Args:
            df (Pandas.DataFrame): Raw bank data DataFrame
        """
        pass

    def _generate_transaction_id(self, row: pd.Series) -> str:
        """
        Takes a row and returns a hash string to generate corresponding transcation ID

        Args:
            row (_type_): _description_
        """
        concat_string = row['transaction_date'] + '|' + \
            row['description'] + '|' + str(row['amount']) + '|' + self.source_bank

        transaction_id = concat_string.encode('utf-8')

        transaction_id = hashlib.sha256(transaction_id).hexdigest()[:16]

        return transaction_id

    def parse(self, filepath: Path) -> pd.DataFrame:
        """
        Parses raw data

        Args:
            filepath (Path): _description_
        """
        # calls _read_raw(), then _normalize(), adds source_bank and account_type columns,
        # generates transaction_id for each row, and converts date columns using pd.to_datetime.

        # validate file existence
        if not filepath.exists():
            raise FileNotFoundError

        # read the raw data and parse transactions into our schema
        parse_df = self._read_raw(filepath)
        parse_df = self._normalize(parse_df)

        # add source bank and account type columns
        parse_df['source_bank'] = self.source_bank
        parse_df['account_type'] = self.account_type

        # create ids for each transaction
        parse_df['transaction_id'] = parse_df.apply(self._generate_transaction_id, axis=1)

        # convert cols to pd.date_time
        parse_df['transaction_date'] = pd.to_datetime(
            parse_df['transaction_date'], errors='coerce')

        parse_df['post_date'] = pd.to_datetime(
            parse_df['post_date'], errors='coerce')

        return parse_df

    def parse_directory(self, directory: Path):
        """
        Finds all .csv files in a directory, calls parse() on each one,
        concatenates the results, and deduplicates by transaction_id.

        Args:
            directory (pathlib.Path): File directory of bank's raw CSV files
        """
        csv_files = directory.glob('*.csv')
        parsed_csvs = []

        for file in csv_files:
            parsed_csvs.append(self.parse(file))

        df = pd.concat(parsed_csvs)

        df.drop_duplicates(subset=["transaction_id"], keep="first")
        return df
