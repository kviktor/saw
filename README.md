# SAW (Subreddit Activity Watcher)

Monitor currently online users for subreddits. It checks the online user count every ~20 minutes.

## Installation
First install the requirements with

```
$ pip install -r requirements.txt
```

Then run ``saw/update.py`` periodically. An example with cron:
`*/20 * * * * python /path/to/saw/saw/update.py` (if you use `virtualenv` see [this](http://stackoverflow.com/a/3287063/1112653) link)

Also change the secret key in ``saw/settings.py``.

## Run

To run the website via Flask's web server first disable debug mode in ``saw/settings.py`` then run the following command

`$ python saw/server.py`

With uwsgi modify the ini file then simply run 

`$ uwsgi --ini uwsgi.ini`

## TODO

- see how well pickling performs with more data, then maybe change to some light db
- tests after db
- no js?
