from typing import Type

from sqlalchemy import text


def delete_all(db, model_type: Type):
    try:
        db.query(model_type).delete()

        db.execute(text("ALTER TABLE {} AUTO_INCREMENT = 1".format(model_type.__tablename__)))
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def add_list_schemas(db, model_type: Type, list_schemas):
    try:
        if list_schemas:
            list_model = [model_type(**schema.dict()) for schema in list_schemas]
            db.add_all(list_model)
            db.commit()
    except Exception as e:
        raise e
    finally:
        db.close()
