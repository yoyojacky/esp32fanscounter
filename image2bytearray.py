import sys
from io import BytesIO
from PIL import Image

# command: python3 image_to_bytearrary.py /path/to/image.jpg  width height

if len(sys.argv) > 1:
    path_to_image = str(sys.argv[1])
    x = int(sys.argv[2])
    y = int(sys.argv[3])

    img = Image.open(path_to_image).convert('1')
    resized_img = img.resize((x, y))
    buffer = BytesIO()
    resized_img.save(buffer, 'ppm')
    img_ba= buffer.getvalue()
    temp = len(str(x) + ' ' + str(y)) + 4
    print(img_ba[temp::])
else:
    print("Usage: image_to_bytearrary.py /path/to/image.jpg  width height ")
