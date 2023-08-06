# Cloaken SDK 

Python SDK for cloaken  
resources.py contains the enpoints to use to interact with Cloaken  

# Examples:

```python
from cloakensdk.client import SyncClient
from cloakensdk.resources import Url
import os  
  
server = os.environ["SERVER_URL"]
username = os.environ["USERNAME"]
password = os.environ["PASSWORD"]
client = SyncClient(server_url=server,
                    username=username,
                    password=password)
  
resource = Url(client)
  
#unshorten a url
#todo(aj)
  
#create a url entry manually in the database
resource.create(url="http://test.com",unshortened_url="http://long.com")
data = resource.full_request()
```

See ./tests/unittests.py

# Unit test instructions:

1. set environment variables:  
    a. SERVER_URL = http://servername:port/  
    b. USERNAME  
    c. PASSWORD  
2. python tests/unittests.py 

# Packaging
1. update version in setup.py
2. `python setup.py sdist bdist_wheel`
3. `twine upload dist/*`
