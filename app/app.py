from flask import Flask, render_template, request, redirect, flash, url_for
from flask_tweepy import Tweepy
import tweepy
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.config.setdefault('TWEEPY_CONSUMER_KEY', 'SERTs8Erl7WuDgtulnQHHfuIW')
app.config.setdefault('TWEEPY_CONSUMER_SECRET', 'Xf7YZXbQakJnZl2hTJeoyLj2B4dFAibNEVe7EFYXRFcYj00MD7')
app.config.setdefault('TWEEPY_ACCESS_TOKEN_KEY', '1376714172327731200-JoYZL80bap886MeICM3t0nRsQ2M8E1')
app.config.setdefault('TWEEPY_ACCESS_TOKEN_SECRET', '5RjBnZdg9ntSPujciM0RJXFXS0kZgrmyWU7hBfyGEYEwD')
app.secret_key = b'GnyCJPpjC/FNbHO'

tweep = Tweepy(app)
bar_temp = 0
pie_temp = 0

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":

        if len(str(request.form.get('tweet'))) > 280:
            # Add a popup that says too many characters
            # Change this render_template
            # flash("Too many characters in the tweet. Please use less than 280", category=str)
            return render_template('homeTooManyChars.html')
        else:
            # TODO: SEND TO SQL SERVER ON PI
            tweep.api.update_status(request.form.get('tweet'))

        return render_template('home.html')

    else:
        return render_template('home.html')


@app.route("/Graph Input", methods=["GET", "POST"])
def graph_input():
    if request.method == "POST":
        if len(str(request.form.get('tweet'))) > 280:
            return render_template('graph.html')
        elif request.form['graph'] == 'pie':
            # TODO: CLEAR CACHE ON RELOAD OR SAME PICTURE WILL DISPLAY OR CHANGE FILE NAME
            query = request.form.get("tweet")
            graph_name = func(query, 1)
            return render_template('pie.html', url=graph_name)
        elif request.form['graph'] == 'bar':
            query = request.form.get("tweet")
            graph_name = func(query, 2)
            return render_template('bar.html', url=graph_name)
        else:
            return render_template('graph.html')
    else:
        return render_template('graph.html')


def func(query, command):
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
    global pie_temp
    global bar_temp
    if command == 1:
        pie_temp += 1
        plt.pie(list(count.values()), labels=list(count.keys()), autopct='%.1f%%', textprops={'color': "w"})
        plt.savefig("static/piegraph" + str(pie_temp) + ".png", transparent=True)
        plt.close()
        return "piegraph" + str(pie_temp) + ".png"

    if command == 2:
        bar_temp += 1
        plt.bar(range(len(count)), list(count.values()), align='center')
        plt.xticks(range(len(count)), list(count.keys()), color='white', rotation='vertical')
        plt.subplots_adjust(bottom=0.27)
        plt.yticks(color='white')
        plt.savefig("static/bargraph" + str(bar_temp) + ".png", transparent=True)
        plt.close()
        return "bargraph" + str(bar_temp) + ".png"


app.run()
