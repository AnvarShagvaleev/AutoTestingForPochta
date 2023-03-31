from config.Configurations import engine
import pandas as pd
from loguru import logger
from tests.TestLogger import test_logger


@test_logger
def test_number_of_entries_by_source(uat_schema_name, uat_table_name, sys_id):

    query = f"""
        SELECT tab.{sys_id}, count(1) cnt from {uat_schema_name}.{uat_table_name} tab
        GROUP BY tab.{sys_id}
        """

    tab = pd.read_sql(
        query,
        engine
    )

    return tab['cnt'].sum(), query, tab