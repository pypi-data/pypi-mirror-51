## Wallpaper Downloader for Reddit

This program downloads wallpapers from subreddits and multireddits of your choosing.

### Configuration

The configuration file is located at `~/.config/reddit-wall.conf`.

Since this relies on [PRAW](https://praw.readthedocs.io/en/latest/index.html), you'll need to get an API key, secret, and user agent. The instructions on how to do that can be found [here](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps). Once you have this info, the program should pick up your PRAW config from your [praw.ini](https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html#praw-ini) file automatically.

You'll also need a client id and secret from Imgur. Instructions for that are [here](https://apidocs.imgur.com/?version=latest). If you don't provide an api key, it will simply skip imgur albums when downloading.