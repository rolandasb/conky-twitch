import json
import urllib2
import os.path

# Settings
twitch_username = "your-twitch-username-here"

# Let's fetch and parse data from twitch
r = urllib2.urlopen("https://api.twitch.tv/kraken/users/"+ twitch_username +"/follows/channels?limit=75").read()
raw_data = json.loads(r)
output = ""

pages = (raw_data["_total"] - 1) / 75
for page in range(0, pages+1):
  if (page != 0):
    r = urllib2.urlopen("https://api.twitch.tv/kraken/users/"+ twitch_username +"/follows/channels?direction=DESC&limit=75&offset=%d&sortby=created_at" % (75 * page)).read()
    raw_data = json.loads(r)

  # Get followed channels
  followed_channels = []
  for channel in raw_data["follows"]:
    followed_channels.append(channel["channel"]["name"])

  # Get live streams
  r = urllib2.urlopen("https://api.twitch.tv/kraken/streams?channel=%s" % ','.join(followed_channels))
  live_streams = json.loads(r.read())

  for stream in live_streams["streams"]:
    channel_name = stream["channel"]["display_name"]
    
    # For some strange reason channel status and game sometimes temporarely 
    # disappears from Twitch API, causing problems in this script. It this case,
    # we don't show status/game in conky at all.
    try:
      channel_title = stream["channel"]["status"]
    except KeyError:
      channel_title = ""
    
    try:
      channel_game = stream["channel"]["game"]
    except KeyError:
      channel_game = ""

    # Build output string
    output += "${color white}" + channel_name + " is ${color LawnGreen}LIVE"

    if channel_title != "":
      output += "\n${color white}" + channel_title

    if channel_game != "":
      output += "\n${color yellow}" + channel_game

    output += "\n\n"

# No live channels?
if output == "":
   output = "No live channels"

# Write output to file
output = output.replace("#", "\#") # Preventing twitch titles from messing with conky config
path = os.path.dirname(__file__) + "/"

if path == "/":
  path = ""

f = open(path + "streams.txt", "w")
f.write(output.encode('utf8'))
f.close()
