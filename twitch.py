import json
import urllib2
import os.path

# Settings
twitch_username = "your-twitch-username-here"

# Let's fetch and parse data from twitch
r = urllib2.urlopen("https://api.twitch.tv/kraken/users/"+ twitch_username +"/follows/channels").read()
raw_data = json.loads(r)

output = ""
for channel in raw_data["follows"]:
	channel_name = channel["channel"]["name"]
	
	# Fetching data of individual channels
	r = urllib2.urlopen("https://api.twitch.tv/kraken/streams/" + channel_name).read()
	raw_channel_data = json.loads(r)

	# We need only live channels
	if raw_channel_data["stream"] != None:
		channel_title = raw_channel_data["stream"]["channel"]["status"]
		channel_game = raw_channel_data["stream"]["channel"]["game"]

		output += "${color white}" + channel_name + " is ${color LawnGreen}LIVE\n${color white}"+channel_title+"\n${color yellow}"+channel_game+"\n\n"

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
