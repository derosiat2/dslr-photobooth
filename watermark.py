from PIL import Image
from PIL import ImageFilter
from PIL import ImageFont, ImageDraw, ImageEnhance 

#This is the function that turns all of the white space into clear space
#It opens an image, converts it to RGBA (Red, Green, Blue, Alpha) then
#I think it's loading the data from the image into temporary array
#and making all the white space clear, Alpha 0,
#(red = 255, green = 255, blue = 255, alpha 0).
#Originally this function output an image file, but instead I had it return the new image.

def white_clear(image):
    img = Image.open(image)
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    #img.save("rgba_logo.png", "PNG")
    #img = Image.open("rgba_logo.png")
    if img.mode != 'RGBA':
        im = im.convert('RGBA')
    return img

#

def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def watermark(im, mark, position, scale, opacity=1):
    #if you enter a position less than 1 it will use it as a relative position
    #.8, .8 will put the water mark 80% down and 80% over on the image
    if position[0]<1 and position[1]<1:
        #print "positon", position
        #print "position(0)", position[0]
        #print "position(1)", position[1]
        position = (int(position[0]*im.size[0]), int(position[1]*im.size[1]))
        #print "position", position
    """Adds a watermark to an image."""
    if opacity < 1:
        mark = reduce_opacity(mark, opacity)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    layer = Image.new('RGBA', im.size, (0,0,0,0))
	# scale, but preserve the aspect ratio
    ratio = min(float(im.size[0]) / mark.size[0], float(im.size[1]) / mark.size[1])
    w = int(mark.size[0] * ratio * scale)
    h = int(mark.size[1] * ratio * scale)
    mark = mark.resize((w, h))
    layer.paste(mark, position)    
    # composite the watermark with the layer
    return Image.composite(layer, im, layer)

def test():
    #set the logo to my logo with whitespace made clear
    logo = white_clear('logo.png')
    #set background image to image3.jpg
    im = Image.open("image3.jpg")
    #set the water 'mark' image to logo
    mark = logo
    #watermark(im, mark, 'tile', 0.5).show()
    #watermark(im, mark, 'scale', 1.0).show()
    #pass the background image, water 'mark' image, location to
    #place 'mark' and opacity to the watermark function
    #watermark(im, mark, (int(im.size[0]*.70), int(im.size[1]*.70)), 0.99).show()
    watermark(im, mark, (.60, .60), .40, 1.0).show()
    print "im.size[0]", im.size[0]
    print "im.size[1]", im.size[1]
    #watermark(im, mark, (0, 0), 0.99).show()

if __name__ == '__main__':
    test()
