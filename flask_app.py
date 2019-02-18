import urllib.request
import json
import twurl
import ssl
import folium
import random

from flask import Flask, render_template, request
# from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

friends_map = folium.Map(tiles="Mapbox Bright")
friends_fgs = []

URL_friends = "https://api.twitter.com/1.1/friends/list.json"
geolocator = Nominatim(user_agent='qwert', timeout=3)
# geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

app = Flask(__name__)


def color_pick():
    return random.choice(['red', 'blue', 'green', 'purple', 'orange', 'darkred',
                          'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue',
                          'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen',
                          'gray', 'black', 'lightgray'])


def add_friend(where, what, col):
    friends_fgs[-1].add_child(
        folium.Marker(location=[where.latitude, where.longitude], popup=what,
                      icon=folium.Icon(color=col)))


def run_map():
    for friends_fg in friends_fgs:
        friends_map.add_child(friends_fg)
    friends_map.add_child(folium.LayerControl())
    # friends_map.save("templates/Friends.html")
    # return render_template("Friends.html")
    return friends_map.get_root().render()


def main(accs):
    for acc in accs.split(" "):
        try:
            icon = color_pick()
            friends_fgs.append(folium.FeatureGroup(name=acc + "`s friends"))
            url = twurl.augment(URL_friends, {"screen_name": acc})
            # print('Retrieving', url)
            connection = urllib.request.urlopen(url, context=ctx)
            data = connection.read().decode()
            # print(data[:250])
            headers = dict(connection.getheaders())
            # # print headers
            print('Remaining', headers['x-rate-limit-remaining'])

            users = json.loads(data)["users"]
            locations = {}
            for user in users:
                who = user["name"] + " (" + user["screen_name"] + ")"
                try:
                    place = geolocator.geocode(user["location"])
                    if str(place) in locations:
                        locations[str(place)].append(who)
                    else:
                        locations[str(place)] = [who]
                except Exception as e:
                    print(e)
            for place in locations:
                location = geolocator.geocode(place)
                who = "".join(name + ' --- ' if name != locations[place][-1] else name for name in
                              locations[place])
                add_friend(location, who, icon)
        except Exception:
            continue
    return run_map()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def register():
    if not request.form.get("acc"):
        return render_template("failure.html")
    acc = request.form.get("acc")
    return main(acc)


if __name__ == "__main__":
    app.run()
