import praw
import traceback
import logging

from time import sleep
from urlparse import urlparse, urljoin

from settings import WATCHED_DOMAINS, KEYWORDS, SERVICES, REPLY_TEMPLATE


class Bot:
    def __init__(self,
                 username,
                 password,
                 client_id,
                 client_secret,
                 subreddits,
                 user_agent,
                 db,
                 limit=1000,
                 debug=False):
        print("Initiating Reddit Instance")
        self.user_agent = user_agent
        self.subreddits = subreddits
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.db = db
        self.limit = limit
        self.debug = debug
        self.rest_time = 3

    def start(self):
        print("Logging into Reddit...")
        reddit = praw.Reddit(
            user_agent=self.user_agent,
            client_id=self.client_id,
            client_secret=self.client_secret,
            username=self.username,
            password=self.password

        )
        print("Starting the comments stream...")
        subreddits = reddit.subreddit(self.subreddits)
        comments = subreddits.stream.comments()
        return self._watch(comments)

    def _watch(self, comments):
        while True:
            try:
                self._search_comments(comments)
            except Exception as e:
                self._handle_exception(e)

    def _search_comments(self, comments):
        for comment in comments:
            if self._should_reply(comment):
		url = urljoin(comment.submission.url, urlparse(comment.submission.url).path)
                text = REPLY_TEMPLATE.format(url)
                self._make_comment(comment, text)

    def _make_comment(self, comment, text):
        if self.debug:
            print(text)
        else:
            comment.reply(text)
            self.db.set(comment.submission.id, comment.submission.url)
            self.db.dump()
        print("Replied to {} at {}".format(comment.author.name, comment.permalink))

    def _should_reply(self, comment):
        existing = self.db.get(comment.submission.id)
        if existing:
            return False

        if urlparse(comment.submission.url).netloc in WATCHED_DOMAINS:
        # Check if comment body contains any keywords
            if (
                any(word in comment.body.lower() for word in KEYWORDS) and
                not any(service in comment.body.lower() for service in SERVICES)
            ):
                return True

        return False

    def _handle_exception(self, e):
        traceback.print_exc()
        logging.warning("### Error: {}".format(e))
        sleep(self.rest_time)
        self.start()
        exit()
