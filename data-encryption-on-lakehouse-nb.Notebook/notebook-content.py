# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "877a3e70-4b3c-4a04-a3cd-b9094714d926",
# META       "default_lakehouse_name": "AdventureWorksLH",
# META       "default_lakehouse_workspace_id": "5f31fb3a-3b20-4e08-ab17-19063afc09d5",
# META       "known_lakehouses": [
# META         {
# META           "id": "877a3e70-4b3c-4a04-a3cd-b9094714d926"
# META         }
# META       ]
# META     },
# META     "warehouse": {
# META       "known_warehouses": []
# META     }
# META   }
# META }

# CELL ********************

from pyspark.sql import functions as F
from pyspark.sql.functions import expr
from pyspark.sql.window import Window

# 32-byte key = AES-256 (also accepts 16 or 24 bytes). Fetch from a secret store, NOT hardcoded.
enr_key = "0123456789abcdef0123456789abcdef"

# Read actual names from the Person table in the default Lakehouse
person_raw = spark.read.table("Person")

# Take a sample of persons and generate deterministic synthetic SSNs
w = Window.orderBy("BusinessEntityID")

person_sample = (
    person_raw
    .select("BusinessEntityID", "FirstName", "LastName")
    .orderBy("BusinessEntityID")
    .limit(30)
    .withColumn("rn", F.row_number().over(w))
)

data_df = (
    person_sample
    .withColumn(
        "ssn",
        F.format_string(
            "%03d-%02d-%04d",
            (F.col("rn") % 900) + 100,   # 100–999
            (F.col("rn") % 90) + 10,     # 10–99
            (F.col("rn") % 9000) + 1000  # 1000–9999
        )
    )
    .select(
        F.col("BusinessEntityID").alias("id"),
        F.concat_ws(" ", "FirstName", "LastName").alias("name"),
        "ssn",
    )
)

df = data_df


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# --- ENCRYPT: replace ssn with an encrypted, base64-encoded string ---
enc = df.withColumn(
    "ssn",
    F.base64(expr(f"aes_encrypt(ssn, '{enr_key}', 'GCM')"))
)

# Write Delta files to the notebook's built-in storage to avoid OneLake/Files path issues
enc.write.format("delta").mode("overwrite").saveAsTable("encrypted_persons")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df=spark.read.table("encrypted_persons")
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# --- DECRYPT: read back and reverse it ---
df = spark.read.table("encrypted_persons")
dec = df.withColumn(
    "ssn",
    expr(f"cast(aes_decrypt(unbase64(ssn), '{enr_key}', 'GCM') as string)")
)
dec.show(truncate=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
