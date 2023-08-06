# idingtalk

Tools package for dingtalk.


## install

```
pip install idingtalk
```


## demo

```
from idingtalk import dingtalk_incoming

token = ""

dingtalk_incoming(
    token, 
    title="This is title",
    text=["# This is title", "> This is first line.", "> This is second line."],
    at_mobiles=["18600000000"],
    at_all=False
)

# or


payload = {
    "msgtype" : "markdown",
    "markdown": {
        "title": "This is push title!",
        "text" : "\n\n".join([
            "# This is text title.",
            "> This is first line.",
            "> This is second line.",
            ])
    },
    "at" : {
        "atMobiles": ["18600000000"],
        "isAll": False
    }
}
dingtalk_incoming(token, payload=payload, at_mobiles=["18600000000"])
```
