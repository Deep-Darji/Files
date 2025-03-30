from pyrogram import Client
import time

# Hardcoded API details
api_id = 24541460   # Replace with your actual API ID
api_hash = "c6a1afbbdca071d53ce9bb53d4602e58"   # Replace with your actual API Hash
bot_token = "7526346918:AAEtkpqz8AkurC_Q_GKz9S-OBB0fyUCIc_Q"   # Replace with your actual bot token

# Channels
source_channel = "Ary_Movies_request_bot"  # Source bot
destination_channel = -1002610319459  # Your movie channel ID

# Pyrogram Client
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Set of forwarded file IDs to avoid duplicates
forwarded_files = set()

async def forward_movies():
    async with app:
        # Iterate through messages from the source channel
        async for message in app.search_messages(source_channel):
            if message.video or message.document:
                file_id = message.video.file_id if message.video else message.document.file_id
                
                # Check for duplicates
                if file_id in forwarded_files:
                    print(f"Skipping duplicate: {file_id}")
                    continue
                
                try:
                    # Forward the message to the destination channel
                    await message.forward(destination_channel)
                    print(f"Forwarded: {file_id}")

                    # Add to the set of forwarded files
                    forwarded_files.add(file_id)

                    # Respect rate limits
                    time.sleep(1)

                except Exception as e:
                    print(f"Error while forwarding: {e}")
                    time.sleep(5)  # Handle API limits

        print("All movies processed!")

app.run(forward_movies())