# CloudBlast API Client Python Library

This library provides the interface to get the list of supported databases,
    submit a search job, query for status and get search result.

## Installation

```bash
pip install ncbi-cloudblast-api
```

## Tutorial

### Prerequisite

This libray requires a running CloudBlast API service (e.g. spawned by the `spawner.sh` script)

### 1. Create client object

```python
from ncbi_cloudblast_api.api_client import APIClient

# Create a client with CloudBlast API address
client=APIClient("35.245.159.177:5000")
```

### 2. Get list of supported Blast databases

```python
# Get the list of supported Blast databases (in a JSON string)
dbs = client.dblist()

# Read the list as a dictionary
import json
dbs = json.loads(client.dblist())

#  Get the first db name ('BLAST-NT DB')
print (dbs['db'][0]['name'])

```

### 3. Perform a Blast search

```python
# Search by sequence accession id
job_id=client.search_by_seq_accession("NM_001234.2")
# e.g. 85bed0b6-3eb5-403e-9863-489f49370ffd
print (job_id)

# Or search by verbatim sequence
job_id=client.search_by_seq_literal("ACGTGGCACTT")

# Or search using a file storing verbatim sequence
job_id=client.search_by_seq_literal("seq_file.txt", is_file=True)

# Query the status of the job, which could be on of the following:
# PENDING, RUNNING, SUCCESS, FAILURE
status=client.status (job_id)

# Once the job finishes, get the result (in a JSON string):
res = client.result(job_id)
# Read the result into a dictionary
res = json.loads(client.result(job_id))
```
