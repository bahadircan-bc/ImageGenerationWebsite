from django.shortcuts import render
import io, os, random
from PIL import Image
from django.http import HttpResponse, HttpRequest, FileResponse


# stable diffusion part

from diffusers import StableDiffusionPipeline

pipe = StableDiffusionPipeline.from_pretrained(
	"./stable-diffusion-v1-5", 
	use_auth_token=True,
)


# Create your views here.

def index(request:HttpRequest):
    context = {
        "fruits": ['apple', 'orange'],
    }
    return render(request, 'imagegeneration/index.html', context)

def generate_any_image(request:HttpRequest, height:int, width:int):
    img_folder_path = 'imagegeneration/images/'
    img_path = os.listdir(img_folder_path)
    img = Image.open(f'{img_folder_path}{img_path[random.randint(0, len(img_path)-1)]}')

    img_width, img_height = img.size

    # Resize the image
    aspect_ratio = float(img_width) / float(img_height)
    new_width = width
    new_height = int(width / aspect_ratio)

    if new_height < height:
        new_height = height
        new_width = int(height * aspect_ratio)

    resized_image = img.resize((new_width, new_height), Image.ANTIALIAS)

    left = (resized_image.width - width) / 2
    top = (resized_image.height - height) / 2
    right = (resized_image.width + width) / 2
    bottom = (resized_image.height + height) / 2

    img = resized_image.crop((left, top, right, bottom))

    # Save the resized image to a buffer
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='JPEG', quality=90)
    img_buffer.seek(0)
    
    return FileResponse(img_buffer, content_type='image/jpeg')


def generate_with_prompt(request:HttpRequest, height:int, width:int, prompt:str):
    result = pipe(prompt)
    img = result["images"][0]  

    img_width, img_height = img.size

    # Resize the image
    aspect_ratio = float(img_width) / float(img_height)
    new_width = width
    new_height = int(width / aspect_ratio)

    if new_height < height:
        new_height = height
        new_width = int(height * aspect_ratio)

    resized_image = img.resize((new_width, new_height), Image.ANTIALIAS)

    left = (resized_image.width - width) / 2
    top = (resized_image.height - height) / 2
    right = (resized_image.width + width) / 2
    bottom = (resized_image.height + height) / 2

    img = resized_image.crop((left, top, right, bottom))

    img_buffer = io.BytesIO()
    img.save(img_buffer, format='JPEG', quality=90)
    img_buffer.seek(0)
    
    return FileResponse(img_buffer, content_type='image/jpeg')