# google-search-client

```python
from google_search_client.search_client import GoogleSearchClient

client = GoogleSearchClient()
results = client.search("hello")
print(results.to_json())
```