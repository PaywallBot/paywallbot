import pickledb

from settings import (
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_USER,
    REDDIT_PASSWORD,
    USER_AGENT_NAME,
    SUBREDDITS
)

from bot import Bot

def main():
    db = pickledb.load('comment.db', False)

    bot = Bot(
        REDDIT_USER,
        REDDIT_PASSWORD,
        REDDIT_CLIENT_ID,
        REDDIT_CLIENT_SECRET,
        SUBREDDITS,
        USER_AGENT_NAME,
        db=db
    )

    bot.start()

if __name__ == '__main__':
    main()
