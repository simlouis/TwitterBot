from flask import Flask, render_template, request, redirect
import json
from flask_tweepy import Tweepy

app = Flask(__name__)
app.config.setdefault('TWEEPY_CONSUMER_KEY', 'SERTs8Erl7WuDgtulnQHHfuIW')
app.config.setdefault('TWEEPY_CONSUMER_SECRET', 'Xf7YZXbQakJnZl2hTJeoyLj2B4dFAibNEVe7EFYXRFcYj00MD7')
app.config.setdefault('TWEEPY_ACCESS_TOKEN_KEY', '1376714172327731200-JoYZL80bap886MeICM3t0nRsQ2M8E1')
app.config.setdefault('TWEEPY_ACCESS_TOKEN_SECRET', '5RjBnZdg9ntSPujciM0RJXFXS0kZgrmyWU7hBfyGEYEwD')

tweepy = Tweepy(app)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        status = tweepy.api.update_status(request.form.get('tweet'))
        status_link = 'http://twitter.com/#!/greswah98/status/%s' % status.id
        # return redirect(status_link)
        return render_template('home.html')
    else:
        return render_template('home.html')


app.run()