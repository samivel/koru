import secrets
import os
from PIL import Image
from koru import app

# Function courtesy of note.nkmk.me to crop photos to square
def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))




# Function containing logic to save users new photo for the route below
def save_photo(form_photo, userid):
    # Create random string to save photos name as
    random_hex = secrets.token_hex(4)
    # Split the file extention so that we can save the new image with the same extention
    _, f_ext = os.path.splitext(form_photo.filename)
    # Create new name for photo using the random hex, and keeping the extention
    photo_fn = userid + random_hex + f_ext
    # Create path for new image. Start with the path to our koru directory, then joining the path within our directory, then joining the new photo name
    photo_path = os.path.join(app.root_path, 'static/images/profile_pics', photo_fn)
    
    # Resize image
    output_size = (600, 600)
    i = Image.open(form_photo)
    i.thumbnail(output_size)

    i = crop_center(i, 300, 300)

    i.save(photo_path)
    return photo_fn