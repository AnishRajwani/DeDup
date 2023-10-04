import requests
import streamlit as st
import json
import pandas as pd

url = "http://demo.vdalive.com/api/"
# url = "http://52.136.118.157//api/"
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJGZkEtVWpyZzlEVnFLS09MWGttcE1YMlRSUkYxWEdUbVZKQS1GZmVQUDFvIn0.eyJleHAiOjE2OTEzOTAzMDksImlhdCI6MTY5MTM5MDAwOSwiYXV0aF90aW1lIjoxNjkxMzg5OTE1LCJqdGkiOiIzM2E2ZTlhNi1kMDVmLTQ3YjMtOTcxMi1lOTUyNTVjMDBjMzciLCJpc3MiOiJodHRwOi8vNTIuMTM2LjExOC4xNTc6ODA4MC9yZWFsbXMvc3NtLXRvb2wiLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiMmE4M2E5NTUtMDZlNi00ZjkzLWJlZGQtMmUzNWFmZWYyNGMzIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoic3NtLXVpIiwibm9uY2UiOiJiN2RkMDU1MC03NzFjLTRjM2MtODdmNC1iZmZhMTk1NjM5MmMiLCJzZXNzaW9uX3N0YXRlIjoiMjMxNDJmNWYtNDIxMS00ODY1LWIwNGUtZWQxZWUzZTQyYzA1IiwiYWNyIjoiMCIsImFsbG93ZWQtb3JpZ2lucyI6WyJodHRwOi8vNTIuMTM2LjExOC4xNTciXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIlNVUEVSQURNSU4iLCJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIiwiZGVmYXVsdC1yb2xlcy1zc20tdG9vbCJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJzaWQiOiIyMzE0MmY1Zi00MjExLTQ4NjUtYjA0ZS1lZDFlZTNlNDJjMDUiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsIm5hbWUiOiJ3aGl0ZWtsYXkgd2hpdGVrbGF5IiwicHJlZmVycmVkX3VzZXJuYW1lIjoid2hpdGVrbGF5IiwiZ2l2ZW5fbmFtZSI6IndoaXRla2xheSIsImZhbWlseV9uYW1lIjoid2hpdGVrbGF5In0.LIfgnRqcPea060ZEbddkgyjRP7vtWOAkB3cyXMPJefJPNw9RiIJL6FAF0eE5ZMvHCc9pL6rBLzjnEIMYdPDN0C0HPdgT6QiquIhWGlmY6y3IYawEUuW8gZd6oHZEkGnlk3cubQJP21q26gJVFb372q3Gyzoqbz0eD2Jc7IVdtVjrubYYB_4-V5FFydatfzuxS656WdirvjEuCMv3Rnw_S4scSt11dZEkIByfQ2iLHtLuNab8-A5gam3Om6A7yuMciQVb0iixbaThGcKYX1q8bIeh9GOnU6JZ3-KlAaaV2niHyIIWSEIPqu19-9mD8_AIdIevndSYX63kN60-VbsRYg'
}


def get_tables(cluster: str):
  payload = {
    "operationName": "Datasets",
    "variables": {
      "searchParams": {
        "cluster": cluster + "-*",
        "searchTerm": "",
        "resultsPerPage": 100
      }
    },
    "query": """
      fragment CoreDatasetFields on Dataset {
        columns {
          name
        }
        dbname
        name
      }

      query Datasets($searchParams: DataSetSearch! = {resultsPerPage: 100}) {
        datasets(searchParams: $searchParams) {
          ...CoreDatasetFields
        }
      }
    """
  }
  response = requests.post(url, headers=headers, data=json.dumps(payload))

  tables = []
  for dataset in response.json()["data"]["datasets"]:
    for column in dataset["columns"]:
      tables.append((dataset["name"], column["name"]))

  return tables

payload = ("{\"query\":"
           "\"fragment CoreDatasourceFields on Datasource "
           "{\\r\\n        id\\r\\n        name\\r\\n    }"
           "\\r\\nquery DataSources "
           "{\\r\\n        datasources {\\r\\n            ...CoreDatasourceFields\\r\\n        }\\r\\n    "
           "}\","
           "\"variables\":{}}")
response = requests.request("POST", url, headers=headers, data=payload)

data_source = []
for i in response.json()["data"]["datasources"]:
    data_source.append(i["id"]+"."+i["name"])

column_1, column_2 = st.columns(2)

# Select box for column 1
with column_1:
    selected_data_source_1 = st.selectbox("Select Data Source 1", ["Select"] + data_source)

# Select box for column 2
with column_2:
    selected_data_source_2 = st.selectbox("Select Data Source 2", ["Select"] + data_source)
if selected_data_source_1 != "Select" and selected_data_source_2 != "Select":

    st.write("Select Table")
    table1 = get_tables(selected_data_source_1.split(".")[1])
    table2 = get_tables(selected_data_source_2.split(".")[1])

    table_1 = []
    columnN = []
    for table in table1:
        table_1.append(table[0])
    table_1 = list(set(table_1))
    # st.write("new")
    table_2 = []
    columnN_2 = []
    for table in table2:
        table_2.append(table[0])
    table_2 = list(set(table_2))
    col1, col2 = st.columns(2)
    with col1:
        select_table_to_show_columns = st.selectbox("Table 1", ["Select"] + table_1)
        for table in table1:
            # print(table)
            if select_table_to_show_columns in table:
                # print(table[1])
                columnN.append(table[1])
    with col2:
        select_table_to_show_columns_2 = st.selectbox("Table 2", ["Select"] + table_2)
        for table in table2:
            # print(table)
            if select_table_to_show_columns_2 in table:
                # print(table[1])
                columnN_2.append(table[1])
    if select_table_to_show_columns != "Select" and select_table_to_show_columns_2 != "Select":
        st.write("Select Primary Key")
        p_col, p_col_ = st.columns(2)
        with p_col:
            pk_1 = st.selectbox(f"Select Primary Key Column from Table {select_table_to_show_columns}", ["Select"] + columnN)
        with p_col_:
            pk_2 = st.selectbox(f"Select Primary Key Column from Table {select_table_to_show_columns_2}", ["Select"] + columnN_2)

        if pk_1 != "Select" and pk_2 != "Select":
            st.write("Blocking Columns")
            col1, col2 = st.columns(2)

            with col1:
                select_box_1 = st.multiselect(f"Select blocking columns from Table {select_table_to_show_columns}",columnN)

            with col2:
                select_box_2 = st.multiselect(f"Select blocking columns from Table {select_table_to_show_columns_2}",columnN_2)

            if select_box_1 is not None and select_box_2 is not None and len(select_box_1)==len(select_box_2):
                st.write("Matching Columns")
                block_ = []
                for i in range(len(select_box_1)):
                    block_.append([select_box_1[i], select_box_2[i]])

                # matching columns
                col, col_ = st.columns(2)
                with col:
                    select_column_1 = st.multiselect(f"Columns from Table {select_table_to_show_columns}", columnN)

                with col_:
                    select_column_2 = st.multiselect(f"Columns from Table {select_table_to_show_columns_2}", columnN_2)
                if select_column_1 is not None and select_column_2 is not None and len(select_column_1)==len(select_column_2):
                    match_ = []
                    for i in range(len(select_column_1)):
                        match_.append([select_column_1[i], select_column_2[i]])

                    threshold_match_probability = st.number_input("Enter threshold match probability: ")
                if (st.button("Process")):
                    conf_dic = {
                        "tables" : [
                            selected_data_source_1.split(".")[1] + "." + select_table_to_show_columns,
                            selected_data_source_2.split(".")[1] + "." + select_table_to_show_columns_2
                        ],
                        "primary_keys" : [
                            pk_1,
                            pk_2
                        ],
                        "blockingCols" : [
                            block_
                        ],
                        "comparisonCols" : [
                            match_
                        ],
                        "threshold_match_probability": threshold_match_probability
                    }
                    # st.write(conf_dic)
                    # temp = pd.DataFrame(conf_dic)
                    # st.table(temp)

                    #call your function

                    #use result variable to store your dataframe

                    #uncomment the below line it will print the table
                    # st.table(result)
else:
    st.write("Please select Datasoruces")


