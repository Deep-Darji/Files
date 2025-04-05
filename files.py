from flask import Flask
from threading import Thread
from pyrogram import Client
from tmdbv3api import TMDb, Movie
import asyncio
import time
import os

# Flask app to keep Koyeb instance alive
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

Thread(target=run).start()

# Pyrogram credentials
api_id = 24541460 # replace with your API ID
api_hash = "c6a1afbbdca071d53ce9bb53d4602e58"
bot_token = "7526346918:AAEtkpqz8AkurC_Q_GKz9S-OBB0fyUCIc_Q"

source_bot = "Ary_Movies_request_bot"
target_channel = -1002610319459

# TMDb setup
tmdb = TMDb()
tmdb.api_key = "cf5837b26050f948d0a7e065f3fa7cf5"  # replace with TMDb API key
movie_api = Movie()

# Track already forwarded files
forwarded_files = set()

# Pyrogram client
app_client = Client("movie_forwarder", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

async def search_and_forward_movies():
    async with app_client:
        movies = movie_api.popular()[:1000]  # Fetch first 1000 popular movies

        for m in movies:
            movie_name = m.title
            print(f"Searching: {movie_name}")

            found = False
            async for message in app_client.search_messages(source_bot, query=movie_name):
                if message.video or message.document:
                    file_id = message.video.file_id if message.video else message.document.file_id

                    if file_id in forwarded_files:
                        print(f"Skipping duplicate: {file_id}")
                        continue

                    try:
                        await message.forward(target_channel)
                        print(f"Forwarded: {movie_name} - {file_id}")
                        forwarded_files.add(file_id)
                        time.sleep(1)
                        found = True
                    except Exception as e:
                        print(f"Error forwarding: {e}")
                        time.sleep(5)

            if not found:
                print(f"Movie not found: {movie_name}")

        print("Done with all movies.")

# Run it
app_client.run(search_and_forward_movies())
