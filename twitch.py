import json
import urllib2
import os.path

# Settings
twitch_username = "your-twitch-username-here"

# Let's fetch and parse data from twitch
r = urllib2.urlopen("https://api.twitch.tv/kraken/users/"+ twitch_username +"/follows/channels?limit=100").read()
raw_data = json.loads(r)

output = ""

# Get followed channels
followed_channels = []
for channel in raw_data["follows"]:
  followed_channels.append(channel["channel"]["name"])

# Get live streams
r = urllib2.urlopen("https://api.twitch.tv/kraken/streams?channel=%s" % ','.join(followed_channels))
live_streams = json.loads(r.read())

for stream in live_streams["streams"]:
  channel_name = stream["channel"]["display_name"]
  channel_title = stream["channel"]["status"]
  channel_game = stream["channel"]["game"]
  output += "${color white}" + channel_name + " is ${color LawnGreen}LIVE\n${color white}" + channel_title + "\n${color yellow}" + channel_game + "\n\n"

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
