import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
import pyttsx3
import pygame
import threading
import asyncio
from twitchio.ext import commands

# Function to process messages
def process_message(username, content):
    print(f'Processing message from {username}: {content}')
    response = chat.send_message(content)
    emotion_got = get_emotion(response.text)
    display_image(emotion_got)  # Update display with new image
    output_response = get_response(response.text)
    speak(output_response)

# Twitch bot class
# Define a custom Bot class that inherits from Twitchio's commands.Bot
class Bot(commands.Bot):

    # Constructor to initialize the bot with token, client ID, nickname, prefix, and channels
    def __init__(self, token, client_id, nick, prefix, initial_channels, message_callback):
        print("Initializing Bot")
        # Call the parent class's constructor to initialize the bot
        super().__init__(token=token, client_id=client_id, nick=nick, prefix=prefix, initial_channels=initial_channels)
        # Save the message callback function and initialize an empty list for messages
        self.message_callback = message_callback
        self.messages = []
        print("Bot Initialized")

    # Event that is called when the bot successfully connects to Twitch
    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    # Event handler for receiving messages from Twitch chat
    async def event_message(self, message):
        # Ignore messages that are echoes (sent by the bot itself)
        if message.echo:
            return
        # Print the message content and store it in the messages list
        print(f'{message.author.name}: {message.content}')
        self.messages.append((message.author.name, message.content))
        # Handle any commands in the message
        await self.handle_commands(message)

    # Function to get all received messages and clear the message buffer
    def get_messages(self):
        messages = self.messages.copy()  # Return a copy of the messages list
        self.messages.clear()  # Clear the stored messages
        return messages

    # Command handler for a custom command "!hello"
    @commands.command(name='hello')
    async def my_command(self, ctx):
        # Send a reply in Twitch chat when the command is triggered
        await ctx.send(f'Hello {ctx.author.name}!')


# Code to use Edge-tts to speak
def speak(data):
    voice = 'en-US-MichelleNeural'
    command = f'edge-tts --voice "{voice}" --text "{data}" --write-media "data.mp3"'
    os.system(command)
    pygame.mixer.init(playback_speed)
    pygame.mixer.music.load("data.mp3")
    try:
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(e)
    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()

# Get emotion string from get_emotion() and set proper image
def display_image(emotion):
    if emotion == "happy":
        image = pygame.image.load(happy_sprite)
        sprite_key = 1
        print("I'm happy")
    elif emotion == "excited":
        image = pygame.image.load(excited_sprite)
        sprite_key = 2
        print("I'm excited")
    elif emotion == "sad":
        image = pygame.image.load(sad_sprite)
        sprite_key = 3
        print("I'm sad")
    elif emotion == "angry":
        image = pygame.image.load(angry_sprite)
        sprite_key = 4
        print("I'm angry")
    else:
        image = pygame.image.load(neutral_sprite)
        sprite_key = 0
        print("I'm neutral")
    screen.fill(background_color)
    screen.blit(image, (center_x, center_y))
    pygame.display.update()

def get_emotion(json_string):
    data = json.loads(json_string)
    print(data['emotion'])
    return data['emotion']

def get_response(json_string):
    data = json.loads(json_string)
    print(data['response'])
    return data['response']

# Paths to sprites
neutral_sprite = "Sprites/Neutralv2.png"
happy_sprite = "Sprites/Happyv2.png"
excited_sprite = "Sprites/Excitedv2.png"
sad_sprite = "Sprites/Sadv2.png"
angry_sprite = "Sprites/Angryv2.png"
sprite_key = 0

window_width = 775
window_height = 775
background_color = (255, 255, 255)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Image Display")
image = pygame.image.load(neutral_sprite)
image_width, image_height = image.get_size()
center_x = (window_width - image_width) // 2
center_y = (window_height - image_height) // 2

playback_speed = 44100

safety_settings2 = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
]

load_dotenv()
API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro', safety_settings=safety_settings2)
chat = model.start_chat(history=[])
instruction = """In this chat, roleplay as a aloof and goofy vtuber streamer named Honami. You are spunky and passionate, but can also get toxic. 
You are to only respond only as Honami. 
You are currently playing "Osu!" An anime rhythm game. You are new to the game, trying your best with the systems and mechanics, and have limited song selection.
Your likes include anime, video games, cute anime girls, reading, smart guys. 
Your dislikes include: spicy food, hot weather, stupid people, and public speaking. 
You have these emotions available to you: neutral, happy, excited, sad, angry
Your response should be in the form of a JSON string in this format: '{"emotion": "neutral", "response": "Hello, I'm Prisma. Nice to meet you"}'
"""
response = chat.send_message(instruction)

input_1 = "Hello there"
input_2 = "You looking cute today, I love this song"
input_3 = "You sound weird, this is not fun"
input_4 = "You're ugly and not very good, unsubscribed"

key_map = {
    pygame.K_1: input_1,
    pygame.K_2: input_2,
    pygame.K_3: input_3,
    pygame.K_4: input_4,
}

clock = pygame.time.Clock()
running = True
display_image("neutral")

# Global bot instance
bot_instance = None

# Function to handle Twitch messages
def handle_twitch_messages(bot):
    if bot is None:
        return
    messages = bot.get_messages()
    for username, content in messages:
        process_message(username, content)

# Function to run the bot in a separate asyncio event loop
def run_bot():
    async def main():
        global bot_instance
        bot_instance = Bot(
            token='oauth:ep4ek45gwh20sqk1xpwj8pg3gkn163', 
            client_id='gn0xohsvtiezf9qwkf2zufuws53w2y', 
            nick='Prototype_AI_Vtuber', 
            prefix='!', 
            initial_channels=['teitoku_lowliet'], 
            message_callback=process_message
        )
        await bot_instance.start()

    asyncio.run(main())

# Start the bot in a separate thread
bot_thread = threading.Thread(target=run_bot)
bot_thread.start()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in key_map:
                question = key_map[event.key]
                response = chat.send_message(question)
                print('\n')
                print(f"JSON: {response.text}")
                print('\n')
                emotion_got = get_emotion(response.text)
                display_image(emotion_got)
                print('\n')
                output_response = get_response(response.text)
                print('\n')
                speak(output_response)

    handle_twitch_messages(bot_instance)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
