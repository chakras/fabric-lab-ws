# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "c4887621-495e-4187-b50d-7e6ae952071c",
# META       "default_lakehouse_name": "SalesLH",
# META       "default_lakehouse_workspace_id": "5f31fb3a-3b20-4e08-ab17-19063afc09d5",
# META       "known_lakehouses": [
# META         {
# META           "id": "c4887621-495e-4187-b50d-7e6ae952071c"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

import pandas as pd
from tqdm.auto import tqdm
base = "https://synapseaisolutionsa.z13.web.core.windows.net/data/AdventureWorks"

# load list of tables
df_tables = pd.read_csv(f"{base}/adventureworks.csv", names=["table"])

for table in (pbar := tqdm(df_tables['table'].values)):
    pbar.set_description(f"Uploading {table} to lakehouse")

    # download
    df = pd.read_parquet(f"{base}/{table}.parquet")

    # save as lakehouse table
    spark.createDataFrame(df).write.mode('overwrite').saveAsTable(table)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
