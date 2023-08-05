# Python
```
from aws_cdk import core
from ddbsizemetric import DDBSizeLib


class MyStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        DDBSizeLib(self, "MyDynamoTableScanner")
```

