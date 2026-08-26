# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "4afb14c8-6f15-43ae-a32c-42790a94ba5c",
# META       "default_lakehouse_name": "demolakehouse_events",
# META       "default_lakehouse_workspace_id": "5f31fb3a-3b20-4e08-ab17-19063afc09d5",
# META       "known_lakehouses": [
# META         {
# META           "id": "4afb14c8-6f15-43ae-a32c-42790a94ba5c"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

df = spark.read.table("OrderHistory")
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
