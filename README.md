conky-twitch
============

Show your live followed Twitch.tv channels in conky.

![preview](http://i.imgur.com/RTlZxYw.png)

### Setup

- Download twitch.py script and place where you want
- Set your Twitch.tv username in twitch.py
- Add `${execpi 600 cat /path/to/streams.txt}` to your conky config (path is the same as twitch.py)
- Add `*/10 * * * * python /path/to/twitch.py` to crontab (`crontab -e`)

### License

This code is free software; you can redistribute it and/or modify it under the terms of the zlib License. A copy of this license can be found in the included LICENSE file.
