
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
import scipy
import pyttsx3
import pygame

#paths to sprites
neutral_sprite = "Sprites/Neutral.png"
happy_sprite = "Sprites/Happy.png"
excited_sprite = "Sprites/Excited.png"
sad_sprite = "Sprites/Sad.png"
angry_sprite = "Sprites/Angry.png"
sprite_key = 0

window_width = 800
window_heigth = 800
background_color = (255, 255, 255) #color white

#initialize pygame
pygame.init()
screen = pygame.display.set_mode((window_width, window_heigth))
pygame.display.set_caption("Image Display")
image = pygame.image.load(neutral_sprite)
#image = image.convert()
image_width, image_height = image.get_size()
# Calculate center coordinates for image placement
center_x = (window_width - image_width) // 2
center_y = (window_heigth - image_height) // 2

#playback speed of pygame
playback_speed = 44100
   # Code to use Edge-tts to speak
def speak(data):
    voice = 'en-US-MichelleNeural'
    command = f'edge-tts --voice "{voice}" --text "{data}" --write-media "data.mp3"'
    os.system(command)

   #pygame.init()
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
  
    #get emotion string from get_emotion() and set proper image
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
    # Update the display after loading the image
    # Draw image on screen at calculated center coordinates
     #display image and bg
    screen.fill(background_color)        
    screen.blit(image, (center_x, center_y))
    # Update the display
    pygame.display.update()    
    return
    



def get_emotion(json_string):
    data = json.loads(json_string)
    print(data['emotion'])
    return data['emotion']
    

def get_response(json_string):
    data = json.loads(json_string)
    print(data['response'])
    return data['response']

    

safety_settings2 : list[str] = [{"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}]


load_dotenv()
API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(
    api_key=API_KEY
    )

model = genai.GenerativeModel('gemini-pro', safety_settings=safety_settings2)
chat = model.start_chat(history=[])
instruction =  """In this chat, roleplay as a aloof and goofy vtuber streamer named Tae. You are spunky and passionate, but can also get toxic. 
Your likes include anime, video games, cute anime girls. 
Your dislikes include: spicy food, hot weather, and public speaking. You are to only respond only as Tae. 
You have these emotions available to you: neutral, happy, excited, sad, angry
Your response should be in the form of a JSON string in this format: '{"emotion": "neutral", "response": "Hello, I'm Prisma. Nice to meet you"}'
"""

response = chat.send_message(instruction)

input_1 = "Hello there"
input_2 = "You looking cute today"
input_3 = "You sound weird, this is not fun"
input_4 = "You're ugly, unsubscribed"

# Key mappings for user inputs (modify key codes if needed)
key_map = {
    pygame.K_1: input_1,
    pygame.K_2: input_2,
    pygame.K_3: input_3,
    pygame.K_4: input_4,
}

clock = pygame.time.Clock()
running = True
display_image("neutral")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Check for key presses in the key map
            if event.key in key_map:
                question = key_map[event.key]

                # Process the question
                response = chat.send_message(question)
                print('\n')
                print(f"JSON: {response.text}")
                print('\n')
                emotion_got = get_emotion(response.text)
                display_image(emotion_got)  # Update display with new image
                print('\n')
                output_response = get_response(response.text)
                print('\n')
                speak(output_response)        



    clock.tick(60)  # Update screen 60 times per second
    
pygame.quit()

 


