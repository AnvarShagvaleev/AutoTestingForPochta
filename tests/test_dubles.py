from config.Configurations import engine
import pandas as pd
from loguru import logger
from tests.TestLogger import test_logger


@test_logger
def test_dubles(lm_data_pk_flag, uat_schema_name, uat_table_name):
    
    query = f"""
            SELECT COUNT(s1.cnt1) cnt FROM (
            SELECT DISTINCT {', '.join(lm_data_pk_flag)} cnt1 
            FROM {uat_schema_name}.{uat_table_name}
            ) s1
            """

    tab = pd.read_sql(
            query,
            engine
        )

    return int(tab.values), query