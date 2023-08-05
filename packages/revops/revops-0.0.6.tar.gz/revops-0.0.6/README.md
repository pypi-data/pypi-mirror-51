# A python module for integrating RevOps

[RevOps](https://www.revops.io)

## Installation

Install from PyPi using pip, a package manager for Python.

```
pip install revops
```

Don't have pip installed? Try installing it, by running this from the command
line:

    $ curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python

Or, you can [download the source code
(ZIP)](https://github.com/revops-io/revops-python/zipball/master "revops-python
source code") for `revops-python`, and then run:

    python setup.py install

## Getting Started

Create a `RevOpsAPI` client.

```python
  from revops.api import RevOpsAPI
  api = RevOpsAPI()
```

### Authentication

Get your API token from your RevOps instance. Set the token to REVOPS_API_KEY in your environment variables.

    export REVOPS_API_KEY="xxxxxxxxxxxxxxxxxxxxxxx"

```python
  from revops.api import RevOpsAPI
  api = RevOpsAPI()
```

### Send your first UsageEvent
```python
from revops.api import RevOpsAPI

# Make sure you've set your REVOPS_API_KEY env var.
# $> export REVOPS_API_KEY="xxxx"
api = RevOpsAPI()

# Create a UsageEvent Request
product_usage = api.usage.events.create(
    transaction_id = "my-first-usage-event-1",
    mode = "insert",
)

# Add an hourly outbound-voice-minutes with the value 100
# To the UsageEvent request
product_usage.add_metric(
    account_id = "my-first-account-id-1",
    product = "voice-minutes",
    metric_name = "outbound-voice-minutes",
    metric_value = 100,
    metric_resolution = "hour",
)

product_usage.commit()
```
