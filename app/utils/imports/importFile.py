from typing import Type

from app.utils.imports.excelMethode import from_excel_to_list_schema


async def upload_data_from_excel_to_static_table(excel_file, schema_type: Type, db):
    new_data = await from_excel_to_list_schema(excel_file, schema_type)
    schema_type.delete_all(db)
    schema_type.add_all(new_data, db)
