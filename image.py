from diffusers import DiffusionPipeline, StableDiffusionImg2ImgPipeline
import openai
import torch
from huggingface_hub import HfFolder
from PIL import Image

# token = HfFolder.get_token()

pipe = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
pipe.to("cuda")

refiner = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-refiner-1.0", 
    text_encoder_2=pipe.text_encoder_2,
    vae=pipe.vae,
    torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
refiner.to("cuda")


def generate_image(prompt: str):
    image = pipe(prompt=prompt).images[0]
    return image


def get_image_prompt(description: str):
    completions = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=[
            {"role": "system", "content": """
            Create an image prompt for the description provided by the user.
             
             A few sample prompts for images are provided below:
             Cute and adorable cartoon goku baby, fantasy, dreamlike, surrealism, super cute, trending on artstation
             An Arab female doctor wearing a hijab, a realistic picture
             Portrait of a young technician dressed business casual, look at to you
             """},
            {"role": "user", "content": description},
        ]
    )
    data = completions.choices[0].message.content
    print("Image Prompt:", data)
    return data


def generate_image_from_image(prompt: str, image: Image.Image):
    image = refiner(prompt=prompt, image=image).images[0]
    return image
