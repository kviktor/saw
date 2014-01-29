import cPickle as pickle
import os
from datetime import datetime, timedelta
from random import randrange
import requests


# path to this file
dir_path = os.path.dirname(__file__)


def get_active(subreddit):
    """Returns the currently online user count for the specified subreddit

    :param subreddit: the subreddit we are curious about
    """

    r = requests.get("http://reddit.com/r/%s/about.json" % subreddit)
    try:
        return r.json()['data'].get('accounts_active')
    except:
        return None


def add_subreddit(sub):
    """Adds a new subreddit to watch

    :param sub: new subreddit's name
    """

    if get_active(sub) is None:
        return "Invalid subreddit!"

    with open(os.path.join(dir_path, 'data/subreddits'), "r+") as f:
        subreddits = f.read().strip().split(',')
        if sub in subreddits:
            return "/r/%s is already monitored!" % sub
        else:
            subreddits.append(sub.lower())
            f.seek(0)
            f.write(','.join(subreddits)),
            pickle_path = os.path.join(dir_path, "data/activities/%s.p" % sub)
            pickle.dump([], open(pickle_path, "wb"))
            return True


def get_subreddit(sub, span):
    """Returns the active numbers for the given time span

    Note: it doesn't actually check timestamps just returns the last
    72 / 504 element. (online number check every 20 minutes -> 3/hour)

    :param sub: subreddit
    :param span: can be either weekly or daily
    """
    try:
        r = pickle.load(open(os.path.join(dir_path,
                                          'data/activities/%s.p' % sub)))
    except:
        return None

    if span == 'daily':
        return r[-24 * 3 - 1:]
    elif span == 'weekly':
        return r[-24 * 3 * 7 - 1:]
    else:
        # then wat?
        return None


def check_subreddit(sub):
    """ Checks whether we are already watching the subreddit or not

    :param sub: subreddit to check
    """

    with open(os.path.join(dir_path, 'data/subreddits'), "r") as f:
        subreddits = f.read().strip().split(',')
        if sub in subreddits:
            return True
        else:
            return False


def update_subreddit(sub):
    """Updates the subreddit's data

    Gets the current online user data for the specified subreddit, then
    appends this value to the picke file.
    (if there is no pickle file it creates a new empty one)

    :param sub: subreddit to update
    """
    active = get_active(sub)
    try:
        file_dir = os.path.join(dir_path, "data", "activities", "%s.p" % sub)
        sub_data = pickle.load(open(file_dir, "rb"))
        sub_data.append({
            'users': active if active is not None else sub_data[-1],
            'date': datetime.utcnow()
        })
        pickle.dump(sub_data, open(file_dir, "wb"))
    except IOError:
        pickle.dump([], open(file_dir, "wb"))
    except Exception:
        pass


def remove_subreddit(sub):
    """Removes the specifies subreddit

    It deletes the name from the subreddit list file and also deletes
    the pickle file.

    :param sub: subreddit
    """
    with open(os.path.join(dir_path, 'data/subreddits'), "r+") as f:
        subreddits = f.read().strip().split(',')
        if sub in subreddits:
            idx = subreddits.index(sub)
            subreddits.pop(idx)
            f.seek(0)
            f.write(",".join(subreddits)),
            f.truncate()
            print "Removed from subreddit list!"
            os.remove(os.path.join(dir_path, "data/activities/%s.p" % sub))
            print "Removed pickle file!"


def data_gen():
    """Generates (lots of) random data
    """
    data = []
    now = datetime.now()
    for i in xrange(1, 16000):
        data.append({
            'users': randrange(5, 155),
            'date': now + timedelta(minutes=i * 15)
        })
    return data


if __name__ == "__main__":
    print "You should not run this file ..."
