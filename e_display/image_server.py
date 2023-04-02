from flask import Flask, request, jsonify
from PIL import Image as PILImage
from io import BytesIO
from wand.image import Image as WandImage
from wand.api import library
from wand.color import Color
from waveshare_epd import epd4in01f

app = Flask(__name__)

def show_image(pil_image):
    epd = epd4in01f.EPD()
    epd.init()
    epd.Clear()
    pil_image = pil_image.rotate(180, expand=True)
    epd.display(epd.getbuffer(pil_image))
    epd.sleep()

def convert_image(input_image_data, palette=None):
    if palette is None:
        palette = [(0, 0, 0), (255, 255, 255), (0, 255, 0), (0, 0, 255), (255, 0, 0), (255, 255, 0), (255, 128, 0)]

    with WandImage(blob=input_image_data) as img:
        # Resize the input image while preserving the aspect ratio
        img.transform(resize='400x640^')

        # Crop the image to the desired size, maintaining the aspect ratio
        img.crop(width=400, height=640, gravity='center')
        with WandImage(width=len(palette), height=1, background=Color('transparent')) as palette_image:
            for idx, color in enumerate(palette):
                palette_image[idx, 0] = Color('rgb({},{},{})'.format(*color))

            library.MagickSetOption(img.wand, b'dither', b'FloydSteinberg')
            # library.MagickSetOption(img.wand, b'dither:diffusion-amount', b'100%')
            img.remap(affinity=palette_image, method='floyd_steinberg')
        

            img.type = 'truecolor'
            img.format = 'bmp3'

            # Convert the WandImage to a PIL.Image
            with BytesIO() as f:
                img.save(file=f)
                f.seek(0)
                pil_image = PILImage.open(f).copy()

    return pil_image

@app.route('/show_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    input_image_data = request.files['image'].read()

    try:
        converted_image = convert_image(input_image_data)
        show_image(converted_image)
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
   
    app.run(host='0.0.0.0', port=8080)
