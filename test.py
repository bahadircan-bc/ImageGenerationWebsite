from torch import autocast
from diffusers import StableDiffusionPipeline

pipe = StableDiffusionPipeline.from_pretrained(
	"./stable-diffusion-v1-5", 
	use_auth_token=True,
)

prompt = "dog, centered"
result = pipe(prompt)
print(result)
image = result["images"][0]  
    
image.save("dog.png")