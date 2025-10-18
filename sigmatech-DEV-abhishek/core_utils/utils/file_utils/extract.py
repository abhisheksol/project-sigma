import io
import requests
import pandas as pd
from typing import Any, List, Tuple
from pandas.core.frame import DataFrame
from requests.models import Response


def fetch_dataframe_from_url(file_url: str) -> Tuple[DataFrame, str]:
    """
    Fetch a file from the given URL and return it as a pandas DataFrame.

    Args:
        file_url (str): The URL of the file.

    Returns:
        Tuple[DataFrame, str]: A tuple containing the DataFrame and detected file extension.

    Raises:
        ValueError: If the file extension is unsupported.
        Exception: If the file could not be read.
    """
    file_extension: str = file_url.lower().split(".")[-1]

    if file_extension not in ["xlsx", "xls", "csv"]:
        raise ValueError(f"Unsupported file format: {file_extension}")

    response: Response = requests.get(file_url, stream=True)
    response.raise_for_status()

    if file_extension in ["xlsx", "xls"]:
        df: DataFrame = pd.read_excel(io.BytesIO(response.content), engine="openpyxl")
    else:  # csv
        df: DataFrame = pd.read_csv(io.BytesIO(response.content))
    # df: DataFrame = pd.read_excel(
    #     "/Users/rohith/Desktop/coding/Django/Aptagrim/sigma/backend/project/Axis_Credit_Card.xlsx")
    return df


def fetch_dataframe_headers_from_url(file_url: str) -> List[str]:
    """
    Fetch an Excel/CSV file from the given URL and return its headers.

    Args:
        file_url (str): The URL of the file.

    Returns:
        List[str]: A list of headers (column names).

    Raises:
        ValueError: If the file extension is unsupported.
        Exception: If the file could not be read.
    """
    file_extension: str = file_url.lower().split(".")[-1]

    if file_extension not in ["xlsx", "xls", "csv"]:
        raise ValueError(f"Unsupported file format: {file_extension}")

    response: Response = requests.get(file_url, stream=True)
    response.raise_for_status()

    if file_extension in ["xlsx", "xls"]:
        df: DataFrame = pd.read_excel(
            io.BytesIO(response.content), engine="openpyxl", nrows=0
        )
    else:  # csv
        df: DataFrame = pd.read_csv(io.BytesIO(response.content), nrows=0)

    return df.columns.tolist()


def fetch_field_exclude_nan_values_from_url(
    file_url: str, field_name: str
) -> List[Any]:
    """
    Fetch an Excel/CSV file from the given URL and return all values of a specific field.

    Args:
        file_url (str): The URL of the file.
        field_name (str): The column name whose values should be returned.

    Returns:
        List[Any]: A list of values from the specified field.

    Raises:
        ValueError: If the file extension is unsupported or the field does not exist.
        Exception: If the file could not be read.
    """
    df, file_extension = (
        fetch_dataframe_from_url(file_url),
        file_url.lower().split(".")[-1],
    )

    if field_name not in df.columns:
        raise ValueError(f"Field '{field_name}' not found in file headers.")

    return df[field_name].dropna().tolist()


def fetch_field_values_from_url(file_url: str, field_name: str) -> List[Any]:
    """
    Fetch an Excel/CSV file from the given URL and return all values of a specific field.
    NaN values are replaced with None.

    Args:
        file_url (str): The URL of the file.
        field_name (str): The column name whose values should be returned.

    Returns:
        List[Any]: A list of values from the specified field (NaN replaced with None).

    Raises:
        ValueError: If the file extension is unsupported or the field does not exist.
        Exception: If the file could not be read.
    """
    df = fetch_dataframe_from_url(file_url)

    if field_name not in df.columns:
        raise ValueError(f"Field '{field_name}' not found in file headers.")

    # Replace NaN with None
    return [None if pd.isna(v) else v for v in df[field_name].tolist()]
