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

# MARKDOWN ********************

# ### Connect Azure Key Vault

# CELL ********************

from notebookutils import mssparkutils

# Directly by vault URL:
vault_url = "https://demoakveastus2.vault.azure.net/"
secret_name = "storage-account-key"

secret_value = mssparkutils.credentials.getSecret(vault_url, secret_name)
#print(f"Fetched secret: {secret_value}")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Replace with your values
storage_account_name = "demofabricsaeastus2"
storage_account_key  = secret_value

# Tell Spark/Hadoop about your account key
spark.conf.set(
    f"fs.azure.account.key.{storage_account_name}.dfs.core.windows.net",
    storage_account_key
)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Read the source file into a DataFrame

container_name = "rawdata"
path_in_container = "yellow_tripdata_2025-01.parquet"

abfss_path = (
    f"abfss://{container_name}"
    f"@{storage_account_name}.dfs.core.windows.net/"
    f"{path_in_container}"
)

# Read the Parquet
df = spark.read.parquet(abfss_path)

# Show a few rows
display(df)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Private Azure Key Vault Connection

# CELL ********************

from notebookutils import mssparkutils

# Directly by vault URL:
vault_url = "https://pr-akveastus2.vault.azure.net/"
secret_name = "pr-storage-account-key"

secret_value = mssparkutils.credentials.getSecret(vault_url, secret_name)
print(f"Fetched secret: {secret_value}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Replace with your values
storage_account_name = "prazstaccteastus2"
storage_account_key  = secret_value

# Tell Spark/Hadoop about your account key
spark.conf.set(
    f"fs.azure.account.key.{storage_account_name}.dfs.core.windows.net",
    storage_account_key
)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Read the source file into a DataFrame

container_name = "rawdata"
#path_in_container = "yellow_tripdata_2025-01.parquet"
path_in_container = "2021.csv"
abfss_path = (
    f"abfss://{container_name}"
    f"@{storage_account_name}.dfs.core.windows.net/"
    f"{path_in_container}"
)

# Read the Parquet
#df = spark.read.parquet(abfss_path)
df = spark.read.format("csv").option("header","true").option("inferSchema","true").load(abfss_path)
# Show a few rows
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
