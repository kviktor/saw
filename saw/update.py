# - * - encoding: utf-8 - * -
from helpers import update_subreddit, get_subreddits


# this script should run periodically (every 15-20 minutes)
if __name__ == "__main__":
    for s in get_subreddits():
        update_subreddit(s.name)
