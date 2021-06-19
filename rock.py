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

class Rock:
    def __init__(self, radius, n_verts, variation, texture):
        self.radius = radius
        self.points = gen_points((radius, radius), radius - variation, radius, n_verts)
        # width and height of our image
        imsize = 2 * radius

        # crop out a bit of the texture
        crop_x = int(random.random() * (texture.width - imsize))
        crop_y = int(random.random() * (texture.height - imsize))
        rock_img = texture.crop((crop_x, crop_y, crop_x + imsize, crop_y + imsize))

        alpha_img = Image.new("L", (imsize, imsize), 0)
        draw = ImageDraw.Draw(alpha_img)

        # draw rock in the alpha channel
        draw.polygon(self.points, 255, 255)
        rock_img.putalpha(alpha_img)

        shadow_img = Image.new("RGBA", (imsize, imsize), (0, 0, 0, 127))
        shadow_base = Image.new("RGBA", (imsize, imsize), (0, 0, 0, 0))
        shadow_img = Image.composite(shadow_img, shadow_base, alpha_img)

        self.image = Image.new("RGBA", (imsize+2, imsize+2))
        self.image.alpha_composite(shadow_img, (2, 2))
        self.image.alpha_composite(rock_img, (0, 0))

        # draw a border
        # border_img = Image.new("RGBA", (imsize, imsize), (0, 0, 0, 0))
        # draw = ImageDraw.Draw(border_img)
        # draw.polygon(self.points, (0, 0, 0, 0), (64, 64, 64, 127))
        # self.image.alpha_composite(border_img)
        # self.image = border_img

    def save(self):
        self.image.save("rock_indiv.png")

def main():
    tex = Image.open("rock_texture.png")
    r = 24
    rock = Rock(r, 10, r//2, tex)
    rock.save()

if __name__ == '__main__':
    main()
