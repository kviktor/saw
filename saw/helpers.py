from datetime import datetime, timedelta
from random import randrange
import requests

from models import Subreddit, Activity
from database import db_session
from settings import USER_AGENT


def get_active(subreddit):
    """Returns the currently online user count for the specified subreddit

    :param subreddit: the subreddit we are curious about
    """

    headers = {'User-Agent': USER_AGENT}
    r = requests.get("http://reddit.com/r/%s/about.json" % subreddit,
                     headers=headers)
    try:
        return r.json()['data'].get('accounts_active')
    except:
        return None


def get_subreddits():
    """ Returns the list of monitored subreddits
    """
    return Subreddit.query.all()


def add_subreddit(sub):
    """Adds a new subreddit to watch

    :param sub: new subreddit's name
    """

    if get_active(sub) is None:
        return "Invalid subreddit!"

    if Subreddit.query.filter_by(name=sub).first():
        return "/r/%s is already monitored!" % sub

    s = Subreddit(name=sub, added=datetime.utcnow())
    try:
        db_session.add(s)
        db_session.commit()
        return True
    except:
        db_session.rollback()
        return "Unknown error!"


def get_subreddit(sub, span):
    """Returns the active numbers for the given time span

    :param sub: subreddit
    :param span: can be either weekly or daily
    """

    query = Activity.query.filter_by(subreddit=sub).order_by(
        Activity.time.asc())
    delta = {
        'daily': timedelta(hours=24),
        'weekly': timedelta(weeks=1)
    }.get(span)
    if delta:
        return query.filter(Activity.time > datetime.utcnow() - delta).all()
    else:
        # then wat?
        return None


def update_subreddit(sub):
    """Updates the subreddit's data

    :param sub: subreddit to update
    """

    active = get_active(sub)
    a = Activity(users=active, time=datetime.utcnow(), subreddit=sub)
    try:
        db_session.add(a)
        db_session.commit()
        return True
    except:
        db_session.rollback()


def remove_subreddit(sub):
    """Removes the specifies subreddit

    :param sub: subreddit
    """

    s = Subreddit.query.filter_by(name=sub).first()
    if s is None:
        print("No subreddit named: %s" % sub)

    try:
        db_session.delete(s)
        db_session.commit()
    except:
        db_session.rollback()
        return "Unknown error!"


def data_gen():
    """Generates (lots of) random data
    """
    data = []
    now = datetime.now()
    for i in range(1, 16000):
        data.append({
            'users': randrange(5, 155),
            'date': now + timedelta(minutes=i * 15)
        })
    return data


if __name__ == "__main__":
    print("You should not run this file ...")
