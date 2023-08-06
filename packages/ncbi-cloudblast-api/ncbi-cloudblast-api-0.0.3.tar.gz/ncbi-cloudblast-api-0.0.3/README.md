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
# Get the list of supported Blast databases
dbs = client.dblist()
for db in res.db:
  print (f"Database name: {db.name}")

```

### 3. Perform a Blast search

```python
def print_result(res):
    '''Print search result

    Paramter:
      res (Resultset): Blast search result
    '''
    if len(res.errors):
        for error in res.errors:
            print(f'Error message: {error}')
    else:
        print(f'Number of alignments: {len(res.alignments)}')

# Search by sequence accession id
res=client.search(accession="NM_001234.2")

# Or search by verbatim sequence
res=client.search(verbatim_seq="ACGTGGCACTT")

print_result(res)
```
