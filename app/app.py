from flask import Flask, render_template, request, redirect, flash, url_for
import json
from flask_tweepy import Tweepy
import tweepy
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config.setdefault('TWEEPY_CONSUMER_KEY', 'SERTs8Erl7WuDgtulnQHHfuIW')
app.config.setdefault('TWEEPY_CONSUMER_SECRET', 'Xf7YZXbQakJnZl2hTJeoyLj2B4dFAibNEVe7EFYXRFcYj00MD7')
app.config.setdefault('TWEEPY_ACCESS_TOKEN_KEY', '1376714172327731200-JoYZL80bap886MeICM3t0nRsQ2M8E1')
app.config.setdefault('TWEEPY_ACCESS_TOKEN_SECRET', '5RjBnZdg9ntSPujciM0RJXFXS0kZgrmyWU7hBfyGEYEwD')
app.secret_key = b'GnyCJPpjC/FNbHO'

tweep = Tweepy(app)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":

        if len(str(request.form.get('tweet'))) > 280:
            # Add a popup that says too many characters
            # Change this render_template
            # flash("Too many characters in the tweet. Please use less than 280", category=str)
            return render_template('homeTooManyChars.html')
        else:
            tweep.api.update_status(request.form.get('tweet'))

        return render_template('home.html')

    else:
        return render_template('home.html')


@app.route("/Graph Input", methods=["GET", "POST"])
def graph_input():
    if request.method == "POST":
        if len(str(request.form.get('tweet'))) > 280:
            return render_template('graph.html')
        else:
            query = request.form.get("tweet")
            func(str(query))
            return render_template("map.html")
    else:
        return render_template('graph.html')


# @app.route("/Graph", methods=["GET", "POST"])
# def graph_it():
#     return render_template("map.html")


def func(query):
    # Create api object
    consumer_token = "SERTs8Erl7WuDgtulnQHHfuIW"
    consumer_token_secret = "Xf7YZXbQakJnZl2hTJeoyLj2B4dFAibNEVe7EFYXRFcYj00MD7"
    access_token = "1376714172327731200-JoYZL80bap886MeICM3t0nRsQ2M8E1"
    access_token_secret = "5RjBnZdg9ntSPujciM0RJXFXS0kZgrmyWU7hBfyGEYEwD"

    authen = tweepy.OAuthHandler(consumer_token, consumer_token_secret)
    authen.set_access_token(access_token, access_token_secret)

    api = tweepy.API(authen)

    # Search for a keyword
    filtered_key_word = query + " -filter:retweets"

    language = "en"
    place = api.geo_search(query='USA', granularity="country")
    country_id = place[0].id

    tweets = tweepy.Cursor(api.search, q='{} place:{}'.format(filtered_key_word, country_id), lang=language).items(50)

    # Make list of tweets
    location = [tweet.user.location for tweet in tweets]

    csvfile = open("Cities_Cleaned.csv", newline='')

    csvpd = []
    for line in csvfile:
        line = line.replace("\r", "")
        line = line.replace("\n", "")
        csvpd.append(line)

    finalList = []

    for i in range(len(csvpd)):
        for j in range(len(location)):
            if csvpd[i] == (location[j]):
                finalList.append(location[j])

    # Dictionary to be graphed
    count = {i: finalList.count(i) for i in finalList}

    # plt.bar(range(len(count)), list(count.values()), align='center')
    # plt.xticks(range(len(count)), list(count.keys()))
    plt.pie(list(count.values()), labels=list(count.keys()))
    plt.savefig("static/graph.png")
    plt.show()


app.run()
