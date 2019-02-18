import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl
import folium
from geopy.geocoders import Nominatim
# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py


def get_data(acct):
    """
    (string) -> dict

    Function returns dict with name of user as a key and location as a value

    """
    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    dct = dict()

    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '50'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)
    for i in js['users']:
        dct[i["screen_name"]] = i["location"]

    headers = dict(connection.getheaders())
    print('Remaining', headers['x-rate-limit-remaining'])
    return dct


def get_location(dct):
    """
    (dict) -> dict

    Function returns dict with name of the user as a key and specific location as a value\
    """
    dct_loc = dict()
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    for i, val in dct.items():
        try:
            if "," in val:
                val = val.split(",")
                location = geolocator.geocode(val[0])
            else:
                location = geolocator.geocode(val)
            dct_loc[i] = [location.latitude, location.longitude]
        except AttributeError:
            pass
    return dct_loc


def create_map(dct):
    """
    (dict) ->

    Function creates a map saved in HTML file
    """
    map = folium.Map(tiles="Mapbox Bright")
    fg_hc = folium.FeatureGroup(name="Locations of friends")
    for key, value in dct.items():
        fg_hc.add_child(folium.CircleMarker(location=value,
                                            radius=2, popup=key,
                                            color='red', fill_opacity=0.5))
    map.add_child(fg_hc)
    map.add_child(folium.LayerControl())

    map.save("templates/Map1.html")

