# Toshinori_Bot
A discord bot with basic fun features
# How to run?
Start by cloning this repo, this can be done by `git clone <url>` in your terminal, then
create a `.env` file and then put the following variables in it- 
```
TOKEN = discord bot token
HOST = postgres db host
USERNAME = postgres db username
PASSWORD = postgres db password
DATABASE = postgres db name
```
The Postgres credentials are optional, but it will be necessary for some commands to work
After you have filled the `.env` file, install the pip requirements from the requirements.txt by running the commands `pip install -r requirements.txt` in your terminal (make sure to cd to the folder)

Then you can run the bot by `python main.py`
