# islack

Tools package for slack.


## install

```
pip install islack
```


## demo

```
from islack import slack_incoming

slack_incoming_url = "your_slack_incoming_url"

slack_incoming(
    slack_incoming_url,
    channel="#temp",
    username="iSlackRobot",
    icon_url="https://s3-us-west-2.amazonaws.com/slack-files2/bot_icons/2019-08-12/723294116148_48.png",
    pretext="This pretest content is a [<https://slack.com|slack>] incoming test!",
    color="#cd0000",
    title="This is *title*!",
    value="This is _first_ line.\n This is _second_ line."
)

# or

payload = {
    "channel": "#everyone",
    "username": "iSlackIncoming",
    "icon_url": "https://ca.slack-edge.com/TJ2D8P5T8-USLACKBOT-sv41d8cd98f0-72",
    "attachments": [
        {
            "fallback": "[<https://slack.com|slack>] slack incoming!",
            "pretext": "[<https://slack.com|slack>] slack incoming!",
            "color": "#2db67c",
            "fields": [
                {
                    "title": "This is the title",
                    "value": "The content below is the value:\n cant be seprateed by \"\\n\"",
                    "short":  "false"
                }
            ]
        }
    ]
}

slack_incoming(
    slack_incoming_url,
    payload=payload
)
```
