import os
import random
import json
import urllib.request
from datetime import datetime
from PIL import Image
from atproto import Client, client_utils


def resize_image(image_data):
    image = Image.open(io.BytesIO(image_data))
    # if image is larger than 900kb, make 80% smaller
    if len(image_data) > 900 * 1024:
        # Resize image to 80%
        new_size = (int(image.width * 0.8), int(image.height * 0.8))
        image = image.resize(new_size)
    resized_image_data = io.BytesIO()
    image.save(resized_image_data, format='JPEG')
    return resized_image_data.getvalue()


def main():
  client = Client()
  client.login(os.environ['BSKY_HANDLE'], os.environ['BSKY_APP_PASSWORD'])

  with open('meta/salvador-dali.json', 'r') as file:
    json_data = json.load(file)

  # pick a random painting
  random_painting = random.choice(json_data)

  # get the necessary metadata
  title = random_painting['title']
  image_url = random_painting['image']
  year = random_painting['completitionYear']
  artist_url = random_painting['artistUrl']
  painting_url = random_painting['url']
  print(image_url)
  req = urllib.request.Request(
      image_url, 
      data=None, 
      headers={
          'User-Agent': '' # urllib user agent gets a 403
      }
  )

  response = urllib.request.urlopen(req)
  img_data = response.read()

  if len(img_data) > 900 * 1024:
       resized_image = resize_image(image_data)

  text_builder = client_utils.TextBuilder()
  text_builder.text(f'{title}, {year}, ')
  text_builder.link(f'https://wikiart.org/en/{artist_url}/{painting_url}', f'https://wikiart.org/en/{artist_url}/{painting_url}'),

  client.send_image(
     text=text_builder, image=img_data, image_alt=''
  )
 
if __name__ == '__main__':
    main()
