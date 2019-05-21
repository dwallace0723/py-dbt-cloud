# py-dbt-cloud
pydbtcloud is a developer kit for interfacing with the [dbt Cloud v2 API](https://app.swaggerhub.com/apis-docs/Sinter/api_v2/2.0.0a1#/) on Python 3.7 and above.

# Authentication

```python
from pydbtcloud import DbtCloud
dbtcloud = DbtCloud(account_id='account_id', api_token='api_token')
```

# Example Usage

Get information about a specific dbt cloud job:

```python
response = dbtcloud.get_job(1234)
```

You can iterate through pages using the following syntax:

```python
for page in dbtcloud.list_runs():
  for run in page.get('data'):
    print(run.get('id'))
```
