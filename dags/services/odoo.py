import pandas as pd
import os, time

class OdooService:
    def __init__(self, connection):
        self.conn = connection

    def read_query(self, filename: str) -> str:
        path = "dags/queries"
        path_sql = os.path.join(os.getcwd(), path, f"{filename}.sql")
        print(f"Leyendo {path_sql} [...]")
        with open(path_sql, "r", encoding="utf-8") as file:
            sql_query = file.read()
        return sql_query
    
    def direct_consult(self, filename: str) -> pd.DataFrame:
        start_time = time.time()
        cursor = self.conn.cursor()
        query = self.read_query(filename)
        cursor.execute(query)
        rows = cursor.fetchall()
        if len(rows) <= 0:
            return pd.DataFrame([])
        column_names = [desc[0] for desc in cursor.description]
        end_time = time.time()
        print(f"[PostgreSQL] Finish {filename}: {end_time - start_time:.4f} segundos")

        return pd.DataFrame(rows, columns=column_names)