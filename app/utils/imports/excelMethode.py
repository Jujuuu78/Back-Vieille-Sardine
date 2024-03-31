import io
from typing import Type

import pandas as pd

from app.utils.convertType import from_df_to_list_schema


async def from_excel_to_list_schema(file, schema_type: Type):
    file_content = await file.read()
    excel_data = io.BytesIO(file_content)
    df = pd.read_excel(excel_data)
    df = df.replace({float('nan'): None})

    list_schema = from_df_to_list_schema(df, schema_type)

    return list_schema
