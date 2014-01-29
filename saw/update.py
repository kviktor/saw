# - * - encoding: utf-8 - * -
from helpers import update_subreddit
import os


# this script should run periodically (every 15-20 minutes)
if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), "data", "subreddits")
    with open(path, "r") as f:
        for subs in f.read().strip().split(','):
            update_subreddit(subs)
