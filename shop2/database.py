import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json
from pathlib import Path

json_base_path = Path(__file__).resolve().parent
db_config_path = json.load(open(json_base_path / "database.json"))
sql_driver = 'ODBC+Driver+17+for+SQL+Server'
sql_server = db_config_path["host"]
sql_database = db_config_path["database"]
sql_username = db_config_path["user"]
sql_password = db_config_path["password"]

connection_string = f"DRIVER={sql_driver};SERVER={sql_server};DATABASE={sql_database};UID={sql_username};PWD={sql_password}"
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string,})
engine = sqlalchemy.create_engine(connection_url,convert_unicode=True, echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)
