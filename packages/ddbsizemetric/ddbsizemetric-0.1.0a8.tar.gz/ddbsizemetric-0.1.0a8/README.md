# Python
```python
from aws_cdk import core
from ddbsizemetric import DDBSizeLib


class MyStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The polling frequency defaults to once every 6 hours, which is how frequently DynamoDB updates the
        # Table information. In this example, we set it to once every 12 hours.
        DDBSizeLib(self, "MyDynamoTableScanner", polling_frequency=core.Duration.hours(12))
```

# Javascript
```js

```
