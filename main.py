from config.Configurations import LM_URL, engine
from tests.test_number_of_entries_by_condition import test_number_of_entries_by_condition
from tests.test_number_of_entries import test_number_of_entries
from tests.test_number_of_entries_by_source import test_number_of_entries_by_source
from tests.test_dubles import test_dubles

import pandas as pd
from loguru import logger

logger.info("Start AutoTest")
testing_objecs = pd.read_excel("input.xlsx", sheet_name="Таблицы").values
writer = pd.ExcelWriter("Report.xlsx", engine="xlsxwriter")

for obj in testing_objecs:
    lm_schema_name = obj[0]
    lm_table_name = obj[1]
    sys_id = obj[2]
    major_version = obj[3]
    uat_schema_name = obj[4]
    uat_table_name = obj[5]

    logger.info(f"Start {uat_schema_name}.{uat_table_name} testing")
    logger.info(f"Getting data from LM and UAT")

    # GET PK, NULL FLAGS FROM LM and GET COLUMN NAMES FROM UAT

    lm_data = pd.read_sql(
        f"""
        SELECT
        la.attribute_name,
        la.null_flag,
        la.pk_flag
        FROM data_catalog.lm_attribute la
        JOIN data_catalog.lm_attribute_type lat ON la.attribute_type_id = lat.type_id
        JOIN data_catalog.lm_entity le ON la.entity_id = le.entity_id
        JOIN data_catalog.lm_schema ls ON ls.schema_id = le.schema_id
        WHERE ls.schema_name IN ('{lm_schema_name}')
        AND le.entity_name IN ('{lm_table_name}')
        AND le.major_version = {major_version}
        AND (la.null_flag = 'N'
        OR la.pk_flag = 'Y');
        """,
        LM_URL
    )

    lm_data_null_flag = lm_data[lm_data['null_flag'] == 'N']['attribute_name'].squeeze().tolist()
    lm_data_pk_flag = lm_data[lm_data['pk_flag'] == 'Y']['attribute_name'].squeeze().tolist()

    uat_data_columns = pd.read_sql(
        f"""
        SELECT * FROM {uat_schema_name}.{uat_table_name} LIMIT 1
        """,
        engine
    ).columns
    

    # TESTS
    result_empty, query_for_empty_test = test_number_of_entries_by_condition(
        uat_data_columns,
        uat_schema_name,
        uat_table_name,
        "= ''"
    )

    result_null_pk, query_for_null_pk_test = test_number_of_entries_by_condition(
        lm_data_null_flag,
        uat_schema_name,
        uat_table_name,
        "is null"
    )

    result_null_all, query_for_null_all_test = test_number_of_entries_by_condition(
        uat_data_columns,
        uat_schema_name,
        uat_table_name,
        "is null"
    )

    tab1_count, tab1_query, tab1 = test_number_of_entries_by_source(uat_schema_name, uat_table_name, sys_id)
    tab2_count, tab2_query = test_number_of_entries(uat_schema_name, uat_table_name)
    tab3_count, tab3_query = test_dubles(lm_data_pk_flag, uat_schema_name, uat_table_name)

    count_test_tab1n2 = tab1_count == tab2_count
    count_test_tab1n3 = tab1_count == tab2_count

    logger.info(f"Finish {uat_schema_name}.{uat_table_name} testing")

    # Making report
    logger.info("Start making report")
    test_names = [
        "Тест на пустоту",
        "Тест на null в pk ключах",
        "Тест на null по всем атрибам",
        "Тест на количество записей в разрезе источников",
        "Тест на количество записей",
        "Тест на дубли"
    ]

    test_queries = [
        query_for_empty_test,
        query_for_null_pk_test,
        query_for_null_all_test,
        tab1_query,
        tab2_query,
        tab3_query
    ]

    result = [
        {attr: cnt for attr, cnt in result_empty[result_empty['cnt'] != 0].values},
        {attr: cnt for attr, cnt in result_null_pk[result_null_pk['cnt'] != 0].values},
        {attr: cnt for attr, cnt in result_null_all[result_null_all['cnt'] != 0].values},
        {attr: cnt for attr, cnt in tab1.values},
        tab2_count,
        tab3_count
    ]

    status = [
        len(result_empty[result_empty['cnt'] != 0]) == 0,
        len(result_null_pk[result_null_pk['cnt'] != 0]) == 0,
        len(result_null_all[result_null_all['cnt'] != 0]) == 0,
        True,
        count_test_tab1n2,
        count_test_tab1n3
    ]

    report = pd.DataFrame({
        "Наименование теста": test_names,
        "SQL запрос": test_queries,
        "Результат": result,
        "Статус": status
    })

    report.to_excel(writer, sheet_name=f"{uat_schema_name[:30-len(uat_table_name)]}.{uat_table_name}")
    logger.info("Finish making report")

writer.save()
logger.info("Finish AutoTest")