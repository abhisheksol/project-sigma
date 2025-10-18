# core_utils/utils/dataframe_utils.py

import pandas as pd
import numpy as np
from typing import List, Dict, Any


def dataframe_to_records_json(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Convert a pandas DataFrame into a list of Python dicts
    with only Python primitive types (int, float, str, None).
    - np.nan -> None
    - numpy scalars -> Python primitives
    """
    # Replace NaN with None
    df: pd.DataFrame = df.where(pd.notnull(df), None)

    records: List[Dict[str, Any]] = []
    for i in range(len(df)):
        row: Dict[str, Any] = df.iloc[i].apply(
            lambda x: (
                None if pd.isna(x) else x.item() if isinstance(x, np.generic) else x
            )
        )
        records.append(dict(row))

    return records
