# Discord Internship Bot - How to run

To start off, before you can begin developing on this bot, you'll need to install the following:

* pip install discord
* pip install dateparser
* pip install pandas
* pip install parsel
* pip install webdriver-manager
* install selenium
* pip install python-dotenv

## Implementing a local .env file

Everything found within the env is kept hidden to prevent the leaking of discord bot tokens or other personal information. Each user will be provided a template file named ".env(example)", which will contain the following:

1. A "BOT_TOKEN", where you simply need to place in the bot token that you're currently running

2. "USER_DATA_DIR", which should link to a local folder where user cookies will be stored. The location of this folder is up to the user, but make sure the location is placed in the ".env"

3. "LINKEDIN_URL" is the url of the Page that you want scraped, this can be a page with an already filled in search result so you can get specific jobs in the queue

4. "CHANNEL_ID" is the channel that the bot will message in, you can find the channel ID by right clicking a channel and selected the bottom option listed as "Copy Channel ID"