## MOOVAI TOOLBOX

This repository contains reusable code to expedite development. 
To use repository, ensure you are using Python 3.6. 

### Installation:
To use this package, install using pip:

```python
pip install moovai
```

### Google Cloud:
This folder contains code to handle GCP resources. 
Prior to using the methods here, you need to be authenticated to GCP.
If you are using a service account, and have the key JSON file:
- On Linux or MacOS
```python
export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"
```
- On Windows:

```python
set GOOGLE_APPLICATION_CREDENTIALS=[PATH]
```

#### cloud-storage
Before using the code here, first make sure that you have a bucket on GCS. If you don't, create one.

##### upload_to_gcs: 
Uploads a local file to a folder on google cloud storage. The file is then DELETED locally.
###### Parameters:
- file: REQUIRED: [STRING] Local file path to upload to google cloud storage.
- bucket_name: REQUIRED: [STRING]  Name of your bucket.
- folder: REQUIRED: [STRING] Folder path to where you want your file to be uploaded to on GCS.

returns: GCS URI where the file was uploaded
###### Sample usage:

```python
from moovai.google_cloud import cloud_storage

file = "/path/to/my/file.txt"
bucket_name = "my_bucket"
folder = "Folder/Subfolder/"

cloud_storage.upload_to_gcs(file, bucket_name, folder)
# returns "gs://my_bucket/Folder/Subfolder/file.txt"

```

##### download_file_gcs:
Downloads file from google cloud storage to local disk. 
###### Parameters:
- gcs_uri: REQUIRED. [STRING] URI of file located on google cloud storage to be downloaded

returns: None. GCS file is downloaded locally.
###### Sample usage:

```python
from moovai.google_cloud import cloud_storage

gcs_uri = "gs://my_bucket/Folder/Subfolder/my_file.txt"

cloud_storage.download_file_gcs(gcs_uri)
# file "my_file.txt" downloaded locally

```

#### bigquery
##### get_schema_from_json:
Takes a schema.json file and converts it into a schema file compatible with BigQuery.
###### Parameters:
- schema_path: REQUIRED. [STRING] Path to your_schema.json file.

returns: schema to plug into BigQuery upload job.
###### Sample usage:

```python
from moovai.google_cloud import bigquery

schema_file = "/path/to/my/schema.json"
bigquery.get_schema_from_json(schema_file)

```

##### get_schema_from_csv:
Takes a csv file containing your data and extracts the schema from your file.
It is recommended to simply use BigQuery's auto-detect schema feature. Use this as a last resort.
###### Parameters:
- csv_file_path: REQUIRED. [STRING] Path to csv file.

returns: schema to plug into BigQuery upload job.
###### Sample usage:

```python
from moovai.google_cloud import bigquery

csv_file = "/path/to/my/file.csv"
bigquery.get_schema_from_csv(csv_file)

```

##### upload_local_file_to_bq:
Uploads local file to BigQuery. schema_path and schema are optional arguments. They are exclusive of one another, provide only one if you want to.
###### Parameters:
- file: REQUIRED. [STRING] Path to local CSV file to upload
- dataset_id: REQUIRED. [STRING] Name of your BigQuery dataset.
- table_id: REQUIRED. [STRING] Name of your BigQuery table to query.
- schema_path: OPTIONAL. [STRING] Path to schema.json file. 
- schema: OPTIONAL. [STRING] schema compatible with BigQuery. 
- overwrite: OPTIONAL. [BOOL] Defaults to False. if set to True, BigQuery will overwrite table, else, it will append new data to table.

returns: None.
###### Sample usage:
```python
from moovai.google_cloud import bigquery

file = "/path/to/my_file.csv"
dataset_id = "my_dataset_id"
table_id = "my_table_id"
bigquery.upload_local_file_to_bq(file, dataset_id, table_id)

```

##### upload_gcs_file_to_bq:
Uploads file from cloud storage to BigQuery. schema_path and schema are optional arguments. They are exclusive of one another, provide only one if you want to.
###### Parameters:
- gcs_uri: REQUIRED. [STRING] Path to CSV file located on cloud storage to upload to BigQuery.
- dataset_id: REQUIRED. [STRING] Name of your BigQuery dataset.
- table_id: REQUIRED. [STRING] Name of your BigQuery table to query.
- schema_path: OPTIONAL. [STRING] Path to schema.json file. 
- schema: OPTIONAL. [STRING] schema compatible with BigQuery. 
- overwrite: OPTIONAL. [BOOL] Defaults to False. if set to True, BigQuery will overwrite table, else, it will append new data to table.

returns: None.
###### Sample usage:
```python
from moovai.google_cloud import bigquery

gcs_uri = "gs://my_bucket/Path/To/my_file.csv"
dataset_id = "my_dataset_id"
table_id = "my_table_id"
bigquery.upload_local_file_to_bq(gcs_uri, dataset_id, table_id)

```

##### generate_sql_query:
Generates a SQL query string to use to query a BigQuery table.
###### Parameters:
- project: REQUIRED. [STRING] Project ID
- dataset_id: REQUIRED. [STRING] Name of your BigQuery dataset.
- table_id: REQUIRED. [STRING] Name of your BigQuery table to query.
- columns: OPTIONAL. [ARRAY] List of column names you want to select.
- conditions: OPTIONAL. [ARRAY] List of conditions to satisfy.

returns: STRING. Standard SQL query string.
###### Sample usage:

```python
from moovai.google_cloud import bigquery

project = "my_project_id"
dataset_id = "my_dataset_id"
table_id = "my_table_id"
bigquery.generate_sql_query(project, dataset_id, table_id)
#returns "SELECT * FROM `project.dataset_id.table_id`" (return everything from table)

columns = ["col1", "col2"]
conditions = ["Date >= TIMESTAMP('2019-05-01')", "col3 < 3"]

bigquery.generate_sql_query(project, dataset_id, table_id, columns=columns, conditions=conditions)
#returns "SELECT col1, col2 FROM `project.dataset_id.table_id` WHERE Date >= TIMESTAMP('2019-05-01') AND col3 < 3" (returns col1 and col2 that meet the specified conditions)

```

##### get_data_from_bq:
Takes a SQL query string (Standard SQL) and returns pandas dataframe
###### Parameters:
- sql_query: REQUIRED. [STRING] string representing the query you want to make.

returns: pandas Dataframe containg the result of your query.
###### Sample usage:

```python
from moovai.google_cloud import bigquery

sql_query = "SELECT * FROM `my_project.my_dataset.my_table`"
bigquery.get_data_from_bq(sql_query)

```

