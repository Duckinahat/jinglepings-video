# credit for this script goes to kelvinpnw and gpr199 on GitHub. https://github.com/kelvinpnw/IPv6TreeImageGenerator
import argparse
import re
from warnings import warn
from PIL import Image


IP_ADDRESS = "2001:4c08:2028:{X}:{Y}:{AA:x}:{BB:x}:{CC:x}"

def convert_image(input_file, x_offset=0, y_offset=0, scale=''):
    with Image.open(input_file) as img:
        addresses = []

        if scale:
            match = re.match(r'(?P<width>\d+)[xX, /](?P<height>\d+)', scale)

            if match:
                values = match.groupdict()
                scale = (int(values.get('width')), int(values.get('height')))

                img.thumbnail(scale, Image.ANTIALIAS)

        if img.height + y_offset > 120:
            warn('Image too tall')
        if img.width + x_offset > 160:
            warn('Image too wide')

        for y in range(img.height):

            for x in range(img.width):

                r, g, b = img.getpixel((x, y))
                values = {'Y': y + y_offset,
                          'X': x + x_offset,
                          'AA': r,
                          'BB': g,
                          'CC': b}
                addresses.append(IP_ADDRESS.format(**values))

        return addresses


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate IP list for IPv6 tree LED wall')
    parser.add_argument('input_file',help='an image')
    parser.add_argument('-x', '--x_offset', type=int, default=0, help='(default: 0)')
    parser.add_argument('-y', '--y_offset', type=int, default=0, help='(default: 0)')
    parser.add_argument('-s', '--scale', type=str, default='', help='Optional: rescale image (eg: 32x32)')
    args = parser.parse_args()

    convert_image(args.input_file, args.x_offset, args.y_offset, args.scale)