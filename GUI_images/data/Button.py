"""
This is a Button system for Pygame 72hrs challenge
Created on: 27:09:2021
Time: 11:06:51
"""

import pygame
import sys
from pygame.image import load

from GUI_images.data.Colors import *


class Button:
    """A simple button class for pygame"""

    def __init__(self, rect: pygame.Rect, idle_animation_image: pygame.Surface,
                 on_hover_animation_image: pygame.Surface,
                 on_click_animation_image: pygame.Surface,
                 idle_num, on_hover_num, on_click_num,
                 width_of_one_image, height_of_one_image):

        # animation_images, timer, original_timer, index
        self.idle_animation_data = [[], 7, 7, 0]
        self.on_hover_animation_data = [[], 7, 7, 0]
        self.on_click_animation_data = [[], 7, 7, 0]

        self.name = ""

        for x in range(idle_num):
            x *= width_of_one_image
            cropped = (x, 0, x + width_of_one_image, height_of_one_image)
            s = pygame.Surface((width_of_one_image, height_of_one_image))
            print(cropped)

            s.blit(idle_animation_image, (0, 0), cropped)
            s.set_colorkey((0, 0, 0))
            s = pygame.transform.scale(s, (rect.w, rect.h))

            self.idle_animation_data[0].append(s)
        for x in range(on_hover_num):
            x *= width_of_one_image
            cropped = (x, 0, x + width_of_one_image, height_of_one_image)
            s = pygame.Surface((width_of_one_image, height_of_one_image))

            s.blit(on_hover_animation_image, (0, 0), cropped)
            s.set_colorkey((0, 0, 0))
            s = pygame.transform.scale(s, (rect.w, rect.h))

            self.on_hover_animation_data[0].append(s)

        for x in range(on_click_num):
            x *= width_of_one_image
            cropped = (x, 0, x + width_of_one_image, height_of_one_image)
            s = pygame.Surface((width_of_one_image, height_of_one_image))

            s.blit(on_click_animation_image, (0, 0), cropped)
            s.set_colorkey((0, 0, 0))
            s = pygame.transform.scale(s, (rect.w, rect.h))

            self.on_click_animation_data[0].append(s)

        self.current_image = self.idle_animation_data[0][0]

        self.range = 0

        self.rect = rect
        self.is_hovering_ = False
        self.is_clicked_ = False
        self.idle_hover = False

        self.anim_imgs = 0
        self.timer = 1
        self.original_timer = 2
        self.index = 3

    def draw(self, win):
        win.blit(self.current_image, self.rect)

    def in_range(self, x2, y2, range):
        x, y, w, h = self.rect
        if x - range < x2 and x + w + range > x2 and y - range < y2 and y + h + range > y2:
            return True
        return False

    def set_center(self, pos):
        self.rect.center = pos

    def get_center(self):
        return self.rect.center

    def set_x(self, x):
        self.rect.x = x

    def get_x(self):
        return self.rect.x

    def set_y(self, y):
        self.rect.y = y

    def get_y(self):
        return self.rect.y

    def is_hovering(self):
        return self.is_hovering_

    def is_clicked(self):
        return self.is_clicked_

    def update(self):
        coor = pygame.mouse.get_pos()
        is_click = pygame.mouse.get_pressed(3)[0]

        self.is_hovering_ = False
        self.is_clicked_ = False
        self.idle_hover = False


        if self.in_range(coor[0], coor[1], self.range):
            if not is_click:
                self.on_hover_animation_data[self.timer] -= 1
                self.is_hovering_ = True

                if self.on_hover_animation_data[self.timer] <= 0:
                    self.on_hover_animation_data[self.index] += 1
                    self.on_hover_animation_data[self.timer] = self.on_hover_animation_data[self.original_timer]
                    if not self.on_hover_animation_data[self.index] <= len(
                            self.on_hover_animation_data[self.anim_imgs]):
                        self.on_hover_animation_data[self.index] = 0

                    self.current_image = self.on_hover_animation_data[self.anim_imgs][
                        self.on_hover_animation_data[self.index] - 1]

                    self.idle_animation_data[self.timer] = 0
                    self.on_click_animation_data[self.timer] = 0

            else:
                self.on_click_animation_data[self.timer] -= 1
                self.is_clicked_ = True

                if self.on_click_animation_data[self.timer] <= 0:
                    self.on_click_animation_data[self.index] += 1
                    self.on_click_animation_data[self.timer] = self.on_click_animation_data[self.original_timer]
                    if not self.on_click_animation_data[self.index] <= len(
                            self.on_click_animation_data[self.anim_imgs]):
                        self.on_click_animation_data[self.index] = 0

                    self.current_image = self.on_click_animation_data[self.anim_imgs][
                        self.on_click_animation_data[self.index] - 1]

                    self.on_hover_animation_data[self.timer] = 0
                    self.idle_animation_data[self.timer] = 0

        else:
            self.idle_animation_data[self.timer] -= 1
            self.idle_hover = True

            if self.idle_animation_data[self.timer] <= 0:
                self.idle_animation_data[self.index] += 1
                self.idle_animation_data[self.timer] = self.idle_animation_data[self.original_timer]
                if not self.idle_animation_data[self.index] <= len(self.idle_animation_data[self.anim_imgs]):
                    self.idle_animation_data[self.index] = 0

                self.current_image = self.idle_animation_data[self.anim_imgs][self.idle_animation_data[self.index] - 1]

                self.on_hover_animation_data[self.timer] = 0
                self.on_click_animation_data[self.timer] = 0


# pygame.init()
# # *****************-- Normal Variables --*****************
# screenHeight = 600
# screenWidth = 1000
# FPS = 60

# # ********************************************************

# # *****************-- SystemCore Variables --*************
# screen = pygame.display.set_mode((screenWidth, screenHeight))
# pygame.display.set_caption('Button system for Pygame')
# clock = pygame.time.Clock()

# # ********************************************************
# bt = Button(pygame.Rect(50, 50, 100, 100), load('data/images/button_images/idle.png'),
#             load('data/images/button_images/hover.png'), load('data/images/button_images/click.png'), 11, 11, 3, 32, 32)
# bt2 = Button(pygame.Rect(500, 500, 100, 100), load('data/images/button_images/idle.png'),
#             load('data/images/button_images/hover.png'), load('data/images/button_images/click.png'), 11, 11, 3, 32, 32)
# g = pygame.image.load('data/images/button_images/ani,.png')


# def draw_window():
#     screen.fill(COLOR_DARK_GRAY)
#     bt.draw(screen)
#     bt2.draw(screen)


# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#     bt.update()
#     bt2.update()
#     print(bt.is_clicked(), bt2.is_hovering())

#     draw_window()

#     pygame.display.flip()

#     clock.tick(FPS)
