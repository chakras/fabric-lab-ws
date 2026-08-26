# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "warehouse": {
# META       "default_warehouse": "473005a4-c46e-4103-879a-7057494e1c04",
# META       "known_warehouses": [
# META         {
# META           "id": "473005a4-c46e-4103-879a-7057494e1c04",
# META           "type": "Lakewarehouse"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

%pip install semantic-link
%pip install openai

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

%pip install azure-ai-projects
%pip install azure-identity
%pip install semantic-link

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import sempy.fabric as fabric

workspace_name = "fabric-lab-ws"
dataset_name = "demo_sales_sm"

dataset = fabric.resolve_dataset_id(
    dataset_name,
    workspace=workspace_name
)

dataset

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

tables = fabric.list_tables(
    dataset=dataset,
    workspace=workspace_name
)

display(tables)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

columns = fabric.list_columns(
    dataset=dataset,
    workspace=workspace_name
)

display(columns)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

measures = fabric.list_measures(
    dataset=dataset,
    workspace=workspace_name
)

display(measures)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import pandas as pd

metadata = columns[
    [
        "Table Name",
        "Column Name",
        "Data Type"
    ]
]

metadata.head()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def build_prompt(table_name, column_name, datatype):

    return f"""
Generate a business friendly Power BI description.

Table: {table_name}

Column: {column_name}

Datatype: {datatype}

Requirements:
- Maximum 40 words
- Explain business meaning
- Mention aggregation guidance if numeric
- Mention when column is identifier
"""

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

os.environ["AZURE_CLIENT_ID"] = "6d7814c5-7b8d-4398-9c83-3624a7bd7b00"
os.environ["AZURE_TENANT_ID"] = "3e7072ad-1eb2-4022-92e6-f67779940553"
os.environ["AZURE_CLIENT_SECRET"] = ""

project_client = AIProjectClient(
    endpoint="https://aif-tprohyryvyaoa.services.ai.azure.com/api/projects/proj-tprohyryvyaoa",
    credential=DefaultAzureCredential()
)

model_client = project_client.get_openai_client()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def generate_description(prompt):

    response = model_client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {
                "role": "system",
                "content": """
You are a Power BI semantic modeling expert.

Generate concise business-friendly metadata descriptions.

Rules:
- Maximum 50 words
- Explain business meaning
- Mention aggregation guidance for numeric columns
- Mention identifier guidance for keys
- Use business terminology
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def build_table_prompt(
        table_name,
        columns):

    return f"""
Generate a Power BI table description.

Table Name:
{table_name}

Columns:
{columns}

Return:
- Business purpose
- Expected grain
- Reporting usage
"""

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def build_column_prompt(
        table_name,
        column_name,
        datatype):

    return f"""
Generate a business description.

Table:
{table_name}

Column:
{column_name}

Datatype:
{datatype}

Requirements:
- Explain meaning
- Explain intended use
- Mention summarization guidance
"""

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import sempy.fabric as fabric

workspace_name = "fabric-lab-ws"
dataset_name = "demo_sales_sm"

columns_df = fabric.list_columns(
        dataset=dataset_name,
        workspace=workspace_name)

measures_df = fabric.list_measures(
        dataset=dataset_name,
        workspace=workspace_name)

tables_df = fabric.list_tables(
        dataset=dataset_name,
        workspace=workspace_name)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

generated_columns = []

for _, row in columns_df.iterrows():
    prompt = build_column_prompt(
        row["Table Name"],
        row["Column Name"],
        row["Data Type"],
    )

    try:
        description = generate_description(prompt)
    except Exception as e:
        description = f"[ERROR calling model: {type(e).__name__} - {getattr(e, 'message', str(e))[:200]}]"

    generated_columns.append(
        {
            "table": row["Table Name"],
            "column_display": row["Column Name"],
            "column_internal": row.get("Column Identifier", row["Column Name"]),
            "description": description,
        }
    )

import pandas as pd
generated_columns_df = pd.DataFrame(generated_columns)

display(generated_columns_df.head())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import pandas as pd

column_desc_df = pd.DataFrame(generated_columns)

display(column_desc_df.head())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from sempy.fabric import connect_semantic_model

with connect_semantic_model(
        dataset_name,
        workspace=workspace_name,
        readonly=False
) as model:

    for _, row in column_desc_df.iterrows():

        table_name = row["table"]
        column_internal = row["column_internal"]

        table_obj = model.model.Tables[table_name]
        column_obj = table_obj.Columns[column_internal]

        column_obj.Description = row["description"]

# Changes are committed automatically when leaving the with-block.


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Select distinct values from the "table" column in column_desc_df
tables_df = column_desc_df[['table']].drop_duplicates().reset_index(drop=True)

display(tables_df)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Generate an overall semantic model description

model_prompt = f"""
Generate an overall business description for a Power BI semantic model.

Model name:
{dataset_name}

Tables:
{', '.join(sorted(tables_df['table'].unique()))}

Return:
- Overall business purpose
- Key subject areas
- Main analytical/reporting scenarios
- Typical consumers (audience)
- High-level data freshness or update expectations
"""

try:
    semantic_model_description = generate_description(model_prompt)
except Exception as e:
    semantic_model_description = f"[ERROR calling model: {type(e).__name__} - {getattr(e, 'message', str(e))[:200]}]"

print(semantic_model_description)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Generate table-level descriptions
import pandas as pd

generated_tables = []

for _, row in tables_df.iterrows():
    table_name = row["table"]

    # Get list of column names for this table to help the LLM
    cols = columns_df[columns_df["Table Name"] == table_name]["Column Name"].tolist()
    cols_str = ", ".join(cols)

    prompt = build_table_prompt(
        table_name=table_name,
        columns=cols_str,
    )

    try:
        description = generate_description(prompt)
    except Exception as e:
        description = f"[ERROR calling model: {type(e).__name__} - {getattr(e, 'message', str(e))[:200]}]"

    generated_tables.append(
        {
            "table": table_name,
            "description": description,
        }
    )

table_desc_df = pd.DataFrame(generated_tables)

display(table_desc_df.head())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Apply table-level and semantic model-level descriptions back to the model
from sempy.fabric import connect_semantic_model

with connect_semantic_model(
        dataset_name,
        workspace=workspace_name,
        readonly=False
) as model:

    # Convert .Tables keys to a Python dict keyed by table name for safe lookup
    # model.model.Tables is a Tabular Collection, not a standard Python dict, so
    # using "in" with a string causes a type conversion error.
    tables_by_name = {t.Name: t for t in model.model.Tables}

    # Update table descriptions
    for _, row in table_desc_df.iterrows():
        table_name = row["table"]

        # Only update if the table exists in the model
        if table_name in tables_by_name:
            table_obj = tables_by_name[table_name]
            table_obj.Description = row["description"]

    # Update semantic model (database) description, if we have one
    if "semantic_model_description" in globals() and semantic_model_description:
        model.model.Description = semantic_model_description

# Changes are committed automatically when leaving the with-block.

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
