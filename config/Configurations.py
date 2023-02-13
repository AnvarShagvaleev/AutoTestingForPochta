import pandas as pd
import puretransport
from sqlalchemy import create_engine
from config.HiveFixedDialect import _HiveFixedDialect


input_user_data = pd.read_excel("input.xlsx")['Unnamed: 1']
USER_NAME = input_user_data[0]
USER_PASSWORD = input_user_data[1]

LM_URL = f"postgresql://{USER_NAME}:{USER_PASSWORD}@10.5.92.58:5432/dc_data"

transport = puretransport.transport_factory(
    host='dc-uat.russianpost.ru',
    port=10010,
    username=USER_NAME,
    password=USER_PASSWORD
)

engine = create_engine(
    'hive://username@/default',
    connect_args={'thrift_transport': transport}
)