def from_list_model_to_list_schema(list_model, schema_type):
    list_schema = [schema_type(**{k: getattr(model, k) for k in schema_type.__annotations__}) for model in list_model]
    return list_schema


def from_df_to_list_schema(df, schema_type):
    list_schema = []
    columns = df.columns.tolist()
    for _, row in df.iterrows():
        try:
            schema_data = {col: row[col] for col in columns}
            schema = schema_type(**schema_data)
            list_schema.append(schema)
        except Exception as e:
            raise ValueError(e)
    return list_schema
