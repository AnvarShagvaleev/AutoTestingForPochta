from config.Configurations import engine
import pandas as pd
from loguru import logger
from tests.TestLogger import test_logger


@test_logger
def test_number_of_entries(uat_schema_name, uat_table_name):

    query = f"""SELECT count(*) cnt FROM {uat_schema_name}.{uat_table_name}"""

    tab = pd.read_sql(
            query,
            engine
        )

    return int(tab.values), query