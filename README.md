# Discord-Chatbot
This is a project mostly to entertain/challenge myself. 
So do not expect to 1) understand the reason for features
as they are private and 2) for my code to actually work.

# Setup
Currently I am building this bot in Python 3.8 so that is a given.
The dependencies can be installed with `pip install -r requirements.txt` (Might need sudo).
A file named .env needs to be created and has to have `DISCORD_TOKEN= [Your token here!]` with the token found in the discord developer portal.
After all this is done Run.py needs to be executed using python3.8

# Testing
The tests are somewhat hard to use as this is a bot which responds to web events. I used pytest to test my functions as those can easily be tested with a fake message event.