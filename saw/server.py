# - * - encoding: utf-8 - * -
from __future__ import unicode_literals
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for
from helpers import add_subreddit, get_subreddit, get_subreddits

app = Flask(__name__)
app.config.from_object("settings")


@app.route("/")
def index():
    return render_template("index.html", watched=get_subreddits())


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        subreddit = request.form.get("subreddit")
        result = add_subreddit(subreddit)
        if result is True:
            flash("Successfully added subreddit!", "success")
            return redirect(url_for("index"))
        elif subreddit is None:
            flash("wat", "danger")
        elif len(subreddit) < 1:
            flash("Subreddit name too short!", "danger")
        else:
            flash(result, "danger")

    return render_template("register.html", error=error)


@app.route("/<subreddit>/", defaults={'span': "daily"})
@app.route("/<subreddit>/<span>/")
def view(subreddit, span):
    if span not in ["weekly", "daily"]:
        flash("Sorry we can't do %s!" % span, "danger")
        return redirect(url_for("index"))
    if subreddit not in [s.name for s in get_subreddits()]:
        flash("This subreddit is not monitored!", "danger")
        return redirect(url_for("index"))

    data = {
        'daily': get_subreddit(subreddit, span) if span == "daily" else None,
        'weekly': get_subreddit(subreddit, span) if span == "weekly" else None
    }
    return render_template("view.html", data=data, sub=subreddit, span=span,
                           current=datetime.utcnow())


if __name__ == "__main__":
    app.run()
