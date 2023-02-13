from config.Configurations import engine
import pandas as pd
from loguru import logger
from tests.TestLogger import test_logger


@test_logger
def test_number_of_entries_by_condition(data_columns, uat_schema_name, uat_table_name, condition):

    test_queries = set()
    for attr in data_columns:
        query = f"""SELECT '{attr}' attribute_name, COUNT(1) cnt FROM {uat_schema_name}.{uat_table_name} tab WHERE tab.{attr} {condition}
        """    
        test_queries.add(query)

    query = "UNION ".join(test_queries)
    result = pd.read_sql(query, engine)

    return result, query