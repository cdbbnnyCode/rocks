# Written in 2021 by Aidan Yaklin
# To the extent possible under law, the author(s) have dedicated all copyright
# and related and neighboring rights to this software to the public domain
# worldwide. This software is distributed without any warranty.
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.

from PIL import Image, ImageDraw
import random
from math import *

def gen_points(center, min_radius, max_radius, n):
    pts = []

    for i in range(n):
        height = min_radius + random.random() * (max_radius - min_radius)
        theta = (i / n) * (2*pi)
        x = int(center[0] + height * cos(theta))
        y = int(center[1] + height * sin(theta))
        pts.append((x, y))

    return pts

def main():
    w = 720
    h = 720
    # image = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    image = Image.open("grass.png")

    draw = ImageDraw.Draw(image)

    sizes = [8, 12, 16]
    n_segments = 10

    existing_rocks = []

    bounding_boxes = [
    #              left top right bottom
    # for example, (50,  50, 500,   500)

    ]

    for i in range(24):
        rad = sizes[int(random.random() * 3)]
        while True:
            print("choosing position for #%d" % i)
            center_x = rad + int(random.random() * (w - 2*rad))
            center_y = rad + int(random.random() * (h - 2*rad))

            collision = False
            for rock in existing_rocks:
                # each rock is a tuple of (x, y, r)
                dist = sqrt((center_x - rock[0])**2 + (center_y - rock[1])**2)
                min_dist = rad + rock[2]
                if dist <= min_dist + 3:
                    collision = True
                    break

            for box in bounding_boxes:
                # bounding box for the circle
                rock_box = (center_x - rad, center_y - rad, center_x + rad, center_y + rad)
                LEFT = 0
                TOP = 1
                RIGHT = 2
                BOT = 3

                if box[LEFT] < rock_box[RIGHT] \
                        and box[RIGHT] > rock_box[LEFT] \
                        and box[TOP] < rock_box[BOT] \
                        and box[BOT] > rock_box[TOP]:
                    collision = True
                    break


            if not collision:
                break

        # we now have good rock coordinates
        pts = gen_points((center_x, center_y), rad * 0.5, rad, n_segments)
        draw.polygon(pts, (0x7f, 0x7f, 0x7f, 0x00), (0x00, 0x00, 0x00, 0x7f))
        existing_rocks.append((center_x, center_y, rad))

    base = Image.open("rock_texture.png")
    base = base.rotate(int(random.random() * 360))
    base = base.crop((152, 152, 872, 872))
    base.alpha_composite(image)

    base.save("rocks.png")

if __name__ == '__main__':
    main()
