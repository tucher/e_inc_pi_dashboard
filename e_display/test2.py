import logging
from waveshare_epd import epd4in01f
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

def picture_from_file():
    return Image.open('4in01f1.bmp')

def test_drawing():
    font24 = ImageFont.truetype('Font.ttc', 24)
    font30 = ImageFont.truetype('Font.ttc', 40)

    Himage = Image.new('RGB', (epd.height, epd.width), 0xffffff)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    draw.text((10, 0), 'hello world', font = font24, fill = 0)
    draw.text((10, 20), '4.01inch e-Paper', font = font24, fill = 0)
    draw.text((10, 160), u'微雪电子', font = font30, fill = epd.BLACK)
    draw.text((10, 200), u'微雪电子', font = font30, fill = epd.ORANGE)
    draw.text((10, 240), u'微雪电子', font = font30, fill = epd.GREEN)
    draw.text((10, 280), u'微雪电子', font = font30, fill = epd.BLUE)
    draw.text((10, 320), u'微雪电子', font = font30, fill = epd.RED)
    draw.text((10, 360), u'微雪电子', font = font30, fill = epd.YELLOW)  
    draw.line((20, 50, 70, 100), fill = 0)
    draw.line((70, 50, 20, 100), fill = 0)
    draw.rectangle((20, 50, 70, 100), outline = 0)
    draw.line((165, 50, 165, 100), fill = 0)
    draw.line((140, 75, 190, 75), fill = 0)
    draw.arc((140, 50, 190, 100), 0, 360, fill = 0)
    draw.rectangle((80, 50, 130, 100), fill = 0)
    draw.chord((200, 50, 250, 100), 0, 360, fill = 0)
    return Himage.rotate(180, expand=True)

try:
    logging.info("epd4in01f Demo")
    epd = epd4in01f.EPD()

    epd.init()
    epd.Clear()

    # im = picture_from_file()
    im = test_drawing()
    epd.display(epd.getbuffer(im))
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd4in01f.epdconfig.module_exit()
    exit()

