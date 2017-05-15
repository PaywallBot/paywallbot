# paywallbot
Reddit bot that comments on paywalled submissions with links to archiving websites

### Initial Setup (requires virtualenv)
```
virtualenv env -p python2.7
. env /bin/activate
pip install -r requirements.txt
```

### settings.py
Create a `settings.py` file to define the initial configuration. Here is a template to get started:

```
REDDIT_CLIENT_SECRET = '{{your client secret}}
REDDIT_CLIENT_ID = '{{your client id}}'
REDDIT_USER = '{{your reddit username}}'
REDDIT_PASSWORD = '{{your reddit password}}'

USER_AGENT_NAME = 'Reddit Paywall Bot by /u/{}'.format(REDDIT_USER)

SUBREDDITS = '+'.join(
    [
        {{list of subreddits}}
    ]
)

WATCHED_DOMAINS = [{{list of domains to match}}]
KEYWORDS = [{{list of keywords to search for}}]
SERVICES = [{{search for existing comments containing these services}}]

REPLY_TEMPLATE = """{{ENTER YOUR AUTOREPLY TEXT IN MARKDOWN FORMAT]}}"""

```

### Running Locally
```
. env/bin/activate && python watch.py
```
