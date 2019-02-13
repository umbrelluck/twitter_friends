import urllib.request
import json
import twurl
import ssl
import folium

from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

friends_map = folium.Map(tiles="Mapbox Bright")
friends_fg = folium.FeatureGroup(name="User friends")

URL_friends = "https://api.twitter.com/1.1/friends/list.json"
geolocator = Nominatim(user_agent='qwert', timeout=3)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)


def add_friend(where, what):
    friends_fg.add_child(
        folium.CircleMarker(location=[where.latitude, where.longitude], popup=what))


def run_map():
    friends_map.add_child(friends_fg)
    friends_map.add_child(folium.LayerControl())
    friends_map.save("Friends.html")


if __name__ == "__main__":
    while True:
        acc = input("Enter account name: ")
        if len(acc) < 1:
            break
        else:
            url = twurl.augment(URL_friends, {"screen_name": acc})
            # print('Retrieving', url)
            connection = urllib.request.urlopen(url, context=ctx)
            data = connection.read().decode()
            # print(data[:250])
            headers = dict(connection.getheaders())
            # # print headers
            print('Remaining', headers['x-rate-limit-remaining'])

            users = json.loads(data)["users"]
            for user in users:
                try:
                    location = geolocator.geocode(user["location"])
                    who = user["name"] + "\n(" + user["screen_name"] + ")"
                    add_friend(location, who)
                except Exception as e:
                    print(e)
            run_map()
