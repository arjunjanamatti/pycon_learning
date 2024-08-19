from sqlalchemy import create_engine

database_type = 'sqlite'
db_api_type = 'pysqlite'
db_name = 'marketdb'
engine = create_engine(url = f"{database_type}+{db_api_type}:///{db_name}",
                       echo = True)