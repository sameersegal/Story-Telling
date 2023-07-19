import sys
import time
import openai
from dotenv import load_dotenv
import os
import json
import requests
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
            You are an expert in visual storytelling. Break the story provided by the user into 5 critical scenes. Respond in valid json format as follows:
             {
                "scenes": [
                    { "image_prompt": "", "narration": "" },
                    { "image_prompt": "", "narration": "" }
                ]
             }

             image_prompt: a description of the image that should be generated for the scene
             narration: a maximum of 50 words that will be the voiceover for the scene

             A few sample image_prompt are provided below:
             a switzerland landscape, cartoon style
             kitten leaping and jumping in air, garden, pixar style, 3d, depth of field
             a drawing of plants and sun, in the style of purple and yellow, emphasis on negative space, fauvist figuratism
             """},
            {"role": "user", "content": story},
        ]
    )
    data = completions.choices[0].message.content
    scenes = json.loads(data)
    return scenes


def draw_scene(prompt):
    # call midjourney api

    url = "YOUR_API_BASE_URL/imagine"

    payload = json.dumps({
        "prompt": f"{prompt} --ar 16:9"
    })

    headers = {
        'Authorization': 'YOUR_API_KEY',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

    while True:

        url = "YOUR_API_BASE_URL/result"

        payload = json.dumps({
            "resultId": "xxxxxxxxxxxxxxxxx"
        })
        headers = {
            'Authorization': 'YOUR_API_KEY',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

        time.sleep(3)


if __name__ == "__main__":
    # parse command line arguments:
    story = get_story(sys.argv[1])
    # story = get_story(path)
    # print()
    # scenes = get_scenes(story)
    scenes = [
        {'image_prompt': 'A Snow Man stands in a snowy landscape, with the setting sun in the background.',
            'narration': 'The Snow Man marvels at the cold wind and stares defiantly at the setting sun.'},
        {'image_prompt': 'The Snow Man converses with the yard-dog, both covered in snow.',
            'narration': "The yard-dog tells the Snow Man about the changing weather and the sun's power to make things run."},
        {'image_prompt': 'The Snow Man observes the beauty of the frozen landscape.',
            'narration': 'The Snow Man is captivated by the glistening trees, frozen dewdrops, and sparkling beauty of winter.'},
        {'image_prompt': 'A young girl and a young man admire the Snow Man in the garden.',
            'narration': "The young girl and man marvel at the Snow Man's beauty and express their delight in the snowy scenery."},
        {'image_prompt': 'The Snow Man yearns to be near the stove, while the yard-dog warns him of its dangers.',
            'narration': "The Snow Man becomes infatuated with the stove's warmth and dreams of being close to it, despite the yard-dog's warnings."}
    ]
    # print(scenes)

    draw_scene(scenes[0]["image_prompt"])
