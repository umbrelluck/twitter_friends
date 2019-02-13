import folium

friends_map = folium.Map(tiles="Mapbox Bright")
friends_fg = folium.FeatureGroup(name="User friends")


def add_friend(where, what, friends=friends_fg):
    friends.add_child(
        folium.CircleMarker(location=[where.latitude, where.longtitude], popup=what))


def run(friends_m=friends_map, friends=friends_fg):
    friends_m.add_child(friends)
    friends_m.add_child(folium.LayerControl())
    friends_m.save("Friends.html")
