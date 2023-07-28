import sys
import openai
from dotenv import load_dotenv
import os
import json
from image import generate_image, get_image_prompt
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_story(path):

    # check if file exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found at {path}")

    # check if extension is .txt
    if not path.endswith(".txt"):
        raise TypeError(f"File must be a .txt file")

    with open(path) as f:
        story = f.readlines()
        story = "\n".join(story)
        if len(story) > 15000:
            raise ValueError(
                f"File {path} must be less than 15,000 characters")

        return story

    return None


def get_scenes(story):
    completions = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=[
            {"role": "system", "content": """
            You are an expert in visual storytelling. Break the story provided by the user into 5 critical scenes with at max 3 characters. Respond in valid json format as follows:
             {
                "characters":[
                    {"key":"","description":""},
                ]
                "scenes": [
                    { 
                        "characters": [
                            {"key": "", orientation": "", "position":""},
                        ]
                        "background_description": "", 
                        "narration": "" 
                    }
                ]
             }

            key: a unique identifier for the character 
            description: a detailed visual description. Do not reference other objects.
            orientation: a short key phrase that describes orientation or pose of the character in the scene e.g. looking at the camera, walking away, etc.            
            position: which part of the scene the character is in e.g. left, right, center, etc.
            background_description: a description of the background in the scene
            narration: a maximum of 50 words that will be the voiceover for the scene

             A few sample prompts for images are provided below:
             a switzerland landscape, cartoon style
             kitten leaping and jumping in air, garden, pixar style, 3d, depth of field
             a drawing of plants and sun, in the style of purple and yellow, emphasis on negative space, fauvist figuratism
             """},
            {"role": "user", "content": story},
        ]
    )
    data = completions.choices[0].message.content
    print(data)
    scenes = json.loads(data)
    return scenes



if __name__ == "__main__":
    # parse command line arguments:
    story = get_story(sys.argv[1])
    # story = get_story(path)
    # print()
    data = get_scenes(story)
    # data = {'characters': [{'key': 'Snow Man', 'image_prompt': 'A tall snowman with tile eyes and a rake mouth'}, {'key': 'Sun', 'image_prompt': 'A large red sun setting in the sky'}, {'key': 'Yard Dog', 'image_prompt': 'A hoarse yard dog, chained up and wearing a collar'}], 'scenes': [{'characters': [{'key': 'Snow Man', 'orientation': 'looking up at the Sun'}], 'background_image_prompt': 'A winter landscape with a setting sun', 'narration': 'The Snow Man marvels at the cold wind and stares at the setting sun.'}, {'characters': [{'key': 'Snow Man', 'orientation': 'looking curious'}, {'key': 'Yard Dog', 'orientation': 'barking'}], 'background_image_prompt': 'A snowy yard with a chained-up dog', 'narration': 'The Snow Man asks the Yard Dog about the sun and the possibility of moving.'}, {'characters': [{'key': 'Snow Man', 'orientation': 'confused'}, {'key': 'Yard Dog', 'orientation': 'barking'}], 'background_image_prompt': 'A foggy landscape with a rising moon', 'narration': 'The Yard Dog explains the moon to the Snow Man and predicts a weather change.'}, {'characters': [{'key': 'Snow Man', 'orientation': 'looking in awe'}, {'key': 'Young Girl', 'orientation': 'excited'}, {'key': 'Young Man', 'orientation': 'admiring'}], 'background_image_prompt': 'A glittering winter garden with hoarfrost on the trees', 'narration': 'A young couple admires the sparkling winter scenery, including the Snow Man.'}, {'characters': [{'key': 'Snow Man', 'orientation': 'longing'}, {'key': 'Yard Dog', 'orientation': 'barking'}], 'background_image_prompt': "A window view of the housekeeper's room with a stove", 'narration': "The Snow Man becomes infatuated with the warmth and glow of the stove, much to the Yard Dog's warning."}]}
    scenes = data['scenes']
    characters = data['characters']
    # print(characters)

    # draw_scene(scenes[0]["image_prompt"])
    prompt = get_image_prompt(characters[0]["description"])
    # print(prompt)
    image = generate_image(prompt)

    # save image to file
    image.save("character.png")
