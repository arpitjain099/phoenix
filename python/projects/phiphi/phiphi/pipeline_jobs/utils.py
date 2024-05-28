"""Utility functions for data processing and uploading."""
import os

import pandas as pd

from phiphi import config


def write_data(
    df: pd.DataFrame,
    dataset: str,
    table: str,
) -> None:
    """Upload DataFrame to BigQuery or save as Parquet file locally based on configuration.

    Args:
        df (pd.DataFrame): DataFrame to be uploaded or saved.
        dataset (str): BigQuery dataset name.
        table (str): BigQuery table name.
    """
    if config.settings.USE_MOCK_BQ:
        parquet_file_path = os.path.join(
            config.settings.MOCK_BQ_ROOT_DIR, dataset, table + ".parquet"
        )
        os.makedirs(os.path.dirname(parquet_file_path), exist_ok=True)

        if os.path.exists(parquet_file_path):
            existing_df = pd.read_parquet(parquet_file_path)
            df = pd.concat([existing_df, df])  # noqa: PD901

        df.to_parquet(parquet_file_path, index=False)
    else:
        df.to_gbq(destination_table=f"{dataset}.{table}", if_exists="append")
