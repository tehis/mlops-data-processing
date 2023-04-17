import os
import pandas as pd
from sqlalchemy import create_engine
import sys


def insert_csv_to_postgres(origin_path: str):
    without_suffix = os.path.splitext(origin_path)[0]
    table_path = os.path.basename(without_suffix)
    table_df = pd.read_csv(origin_path, index_col=[0])

    table_name = os.path.basename(os.path.normpath(table_path)).replace("-", "_")

    engine = create_engine('postgresql://admin:admin@localhost:5432/mlsd_experiments')
    table_df.to_sql(table_name, engine)


if __name__ == '__main__':
    # print(sys.argv)
    insert_csv_to_postgres(str(sys.argv[1]))
