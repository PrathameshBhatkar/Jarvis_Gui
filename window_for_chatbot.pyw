# !/usr/bin/python3.8
"""
This is a Gui for Voice chatbot
Created on: 24:12:2021
Time: 04:34:40 PM
"""
from typing import List

import pygame
import sys
import math

import psutil
import numpy as np
import cv2

import requests
import json

from pygame.image import load
from datetime import datetime
from GUI_images.data import Button
import keyboard
import webbrowser

with open("User_data.json") as f:
    data = json.load(f)

api_key = "da2b33b4044a6c2b250c08fb8b2b1075"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
city_name = data["city_name"]
complete_url = base_url + "appid=" + api_key + "&q=" + city_name

months = {
        "01": "JANUARY",
        "02": "FEBRUARY",
        "03": "MARCH",
        "04": "APRIL",
        "05": "MAY",
        "06": "JUNE",
        "07": "JULY",
        "08": "AUGUST",
        "09": "SEPTEMBER",
        "10": "OCTOBER",
        "11": "NOVEMBER",
        "12": "DECEMBER"

}


def get_weather_info():
    response = requests.get(complete_url)
    x = response.json()
    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to
    # "404", means city is found otherwise,
    # city is not found

    # print json with formatting
    # print(json.dumps(x, indent=4, sort_keys=True))

    if x["cod"] != "404":
        current_temperature = round(x["main"]["temp"] - 273.15)
        return str(current_temperature) + "°C", x["main"]["humidity"]


class WebsiteButton:
    """A simple button class for pygame"""

    def __init__(self, rect: pygame.Rect, idle_animation_image: pygame.Surface,
                 on_hover_animation_image: pygame.Surface,
                 on_click_animation_image: pygame.Surface,
                 idle_num, on_hover_num, on_click_num,
                 width_of_one_image, height_of_one_image):

        width_of_one_image, height_of_one_image = rect.w, rect.h

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


pygame.init()
# *****************-- Normal Variables --*****************
screenHeight = 800
screenWidth = 1500
FPS = 60

# Colour
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)

COLOR_BLUE_MAIN = (28, 239, 233)
COLOR_BLUE_DARK = (0, 170, 170)
COLOR_BLUE_LIGHT = (0, 164, 164)

COLOR_GRAY = (100, 100, 100)
COLOR_LIGHT_GRAY = (200, 200, 200)
COLOR_DARK_GRAY = (50, 50, 50)

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

COLOR_YELLOW = (255, 255, 0)
COLOR_PINK = (255, 0, 255)

# ***********************************-- SystemCore Variables --*******************************************************

final_sw, final_sh = data["screen_size"]
final_sw, final_sh = int(final_sw), int(final_sh)

main_screen = pygame.display.set_mode((final_sw, final_sh))
pre_draw_screen = pygame.Surface((screenWidth, screenHeight))

pygame.display.set_caption('Gui for Voice Chatbot')
clock = pygame.time.Clock()

# ********************************************************************************************************************
background = pygame.image.load("GUI_images/background.png").convert_alpha()
side_arrow = pygame.image.load("GUI_images/side arrow.png").convert_alpha()
# Thread(target=Voice_chatbot.start).start()
hdd = psutil.disk_usage('/')

# print("Total: %d GiB" % hdd.total / (2 ** 30))
# print("Used: %d GiB" % hdd.used / (2 ** 30))
# print("Free: %d GiB" % hdd.free / (2 ** 30))

# ####################################################################################################################
temperature, humidity_percent = get_weather_info()
# url = "https://weather.com/en-IN/weather/today/l/508eff91cdf8cac0cb28b55acd509ad588089fe7665061abaf210c6505f30c06"
# r = requests.get(url)
# htmlContent = r.content

# soup = BeautifulSoup(htmlContent, 'html.parser')

# div = soup.find('span', class_='CurrentConditions--tempValue--3a50n')

# temperature = div.text
# # temperature = 27

# # ####################################################################################################################

# url = "https://weather.com/en-IN/weather/tenday/l/508eff91cdf8cac0cb28b55acd509ad588089fe7665061abaf210c6505f30c06"
# r = requests.get(url)
# htmlContent = r.content

# soup = BeautifulSoup(htmlContent, 'html.parser')

# div = soup.find('span', class_='DetailsTable--value--1q_qD')
# humidity_percent = str(div.text)[:-1]
# # humidity_percent = str(75)

# print(humidity_percent)

rad = 0

# FONT = pygame.font.Font('GUI_images/Fonts/Machine Regular.ttf', 17)
# FONT = pygame.font.Font('GUI_images/Fonts/Machine Regular.ttf', 17)
FONTS = {
        "month name"   : pygame.font.Font('GUI_images/Fonts/Machine Regular.ttf', 17),
        "day"          : pygame.font.Font('GUI_images/Fonts/Machine Regular.ttf', 17),
        "year"         : pygame.font.Font('GUI_images/Fonts/Machine Regular.ttf', 15),
        "date"         : pygame.font.Font('GUI_images/Fonts/NovaRound-Regular.ttf', 52),
        "temperature"  : pygame.font.Font('GUI_images/Fonts/Teko-Medium.ttf', 35),
        "full capacity": pygame.font.Font('GUI_images/Fonts/Teko-Medium.ttf', 25),
        "news font"    : pygame.font.Font('GUI_images/Fonts/Teko-Medium.ttf', 25)

}

s = pygame.Surface((50, 20))
s.fill((255, 255, 255))

bt_eject = Button.Button(pygame.Rect(122, 705, int(41 + 41), int(14 + 14)),
                         load('GUI_images/data/images/button_images/eject.png'),
                         load('GUI_images/data/images/button_images/eject hover.png'),
                         load('GUI_images/data/images/button_images/eject click.png'), 1, 1, 1, 82, 28)

bt_reboot = Button.Button(pygame.Rect(123, 735, int(45 + 45), int(13 + 13)),
                          load('GUI_images/data/images/button_images/reboot.png'),
                          load('GUI_images/data/images/button_images/hover.png'),
                          load('GUI_images/data/images/button_images/click.png'), 1, 1, 1, 90, 23)

temp_circle = 0
power_circle_anim = 0

url = ('https://newsapi.org/v2/top-headlines?'
       'country=in&'
       'apiKey=')

url += '127e359614c54550aa63d6bf388e1f29'

response = requests.get(url)

news = json.loads(response.text)
# 9
websites_buttons = [
        WebsiteButton(pygame.Rect(1350, 157, 42, 29),
                      pygame.image.load("GUI_images/data/images/button_images/website_button_images/google.png"),
                      pygame.image.load("GUI_images/data/images/button_images/website_button_images/google hover.png"),
                      pygame.image.load("GUI_images/data/images/button_images/website_button_images/google click.png"),
                      1,
                      1, 1, 42, 29),
        WebsiteButton(pygame.Rect(1350, 184, 51, 29),
                      pygame.image.load("GUI_images/data/images/button_images/website_button_images/Youtube.png"),
                      pygame.image.load("GUI_images/data/images/button_images/website_button_images/Youtube hover.png"),
                      pygame.image.load("GUI_images/data/images/button_images/website_button_images/Youtube click.png"),
                      1,
                      1, 1, 42, 29),
        WebsiteButton(pygame.Rect(1350, 211, 34, 29),
                      pygame.image.load("GUI_images/data/images/button_images/website_button_images/gmail.png"),
                      pygame.image.load("GUI_images/data/images/button_images/website_button_images/gmail hover.png"),
                      pygame.image.load("GUI_images/data/images/button_images/website_button_images/gmail click.png"),
                      1, 1,
                      1, 42, 29),
        WebsiteButton(pygame.Rect(1350, 211 + 27, 61, 29),
                      pygame.image.load("GUI_images/data/images/button_images/website_button_images/Whatsapp.png"),
                      pygame.image.load(
                              "GUI_images/data/images/button_images/website_button_images/Whatsapp hover.png"),
                      pygame.image.load(
                              "GUI_images/data/images/button_images/website_button_images/Whatsapp click.png"), 1,
                      1, 1, 42, 29),
        WebsiteButton(pygame.Rect(1350, 211 + 27 + 27, 90, 29),
                      pygame.image.load("GUI_images/data/images/button_images/website_button_images/stackoverflow.png"),
                      pygame.image.load(
                              "GUI_images/data/images/button_images/website_button_images/stackoverflow hover.png"),
                      pygame.image.load(
                              "GUI_images/data/images/button_images/website_button_images/stackoverflow click.png"), 1,
                      1, 1,
                      42, 29),
        WebsiteButton(pygame.Rect(1350, 211 + 27 + 27 + 27, 100, 29),
                      pygame.image.load(
                              "GUI_images/data/images/button_images/website_button_images/Geeks for geeks.png"),
                      pygame.image.load(
                              "GUI_images/data/images/button_images/website_button_images/Geeks for geeks hover.png"),
                      pygame.image.load(
                              "GUI_images/data/images/button_images/website_button_images/Geeks for geeks click.png"),
                      1, 1, 1,
                      42, 29),
        WebsiteButton(pygame.Rect(1350, 211 + 27 + 27 + 27 + 27, 55, 29),
                      pygame.image.load("GUI_images/data/images/button_images/website_button_images/flaticons.png"),
                      pygame.image.load(
                              "GUI_images/data/images/button_images/website_button_images/flaticons hover.png"),
                      pygame.image.load(
                              "GUI_images/data/images/button_images/website_button_images/flaticons click.png"),
                      1, 1, 1, 42, 29),
        WebsiteButton(pygame.Rect(1350, 211 + 27 + 27 + 27 + 27 + 27, 44, 29),
                      pygame.image.load("GUI_images/data/images/button_images/website_button_images/fontjoy.png"),
                      pygame.image.load("GUI_images/data/images/button_images/website_button_images/fontjoy hover.png"),
                      pygame.image.load("GUI_images/data/images/button_images/website_button_images/fontjoy click.png"),
                      1,
                      1, 1, 42, 29),
        WebsiteButton(pygame.Rect(1350, 211 + 27 + 27 + 27 + 27 + 27 + 27, 53, 29),
                      pygame.image.load("GUI_images/data/images/button_images/website_button_images/lowspec.png"),
                      pygame.image.load("GUI_images/data/images/button_images/website_button_images/lowspec hover.png"),
                      pygame.image.load("GUI_images/data/images/button_images/website_button_images/lowspec click.png"),
                      1,
                      1, 1, 42, 29)

]
folder_buttons = [
        WebsiteButton(pygame.Rect(1111, 62, 42, 29),
                      pygame.image.load("GUI_images/data/images/button_images/folder_button_images/images.png"),
                      pygame.image.load("GUI_images/data/images/button_images/folder_button_images/images hover.png"),
                      pygame.image.load("GUI_images/data/images/button_images/folder_button_images/images click.png"),
                      1,
                      1, 1, 42, 29),
        WebsiteButton(pygame.Rect(1090, 87, 64, 29),
                      pygame.image.load("GUI_images/data/images/button_images/folder_button_images/Documents.png"),
                      pygame.image.load(
                              "GUI_images/data/images/button_images/folder_button_images/Documents hover.png"),
                      pygame.image.load(
                              "GUI_images/data/images/button_images/folder_button_images/Documents click.png"), 1,
                      1, 1, 42, 29),
        WebsiteButton(pygame.Rect(1103, 113, 63, 29),
                      pygame.image.load("GUI_images/data/images/button_images/folder_button_images/Downloads.png"),
                      pygame.image.load(
                              "GUI_images/data/images/button_images/folder_button_images/Downloads hover.png"),
                      pygame.image.load(
                              "GUI_images/data/images/button_images/folder_button_images/Downloads click.png"), 1,
                      1,
                      1, 42, 29),
        WebsiteButton(pygame.Rect(1099, 160, 37, 29),
                      pygame.image.load("GUI_images/data/images/button_images/folder_button_images/Videos.png"),
                      pygame.image.load("GUI_images/data/images/button_images/folder_button_images/Videos hover.png"),
                      pygame.image.load("GUI_images/data/images/button_images/folder_button_images/Videos click.png"),
                      1,
                      1, 1, 42, 29),
        WebsiteButton(pygame.Rect(1092, 193, 33, 29),
                      pygame.image.load("GUI_images/data/images/button_images/folder_button_images/music.png"),
                      pygame.image.load("GUI_images/data/images/button_images/folder_button_images/music hover.png"),
                      pygame.image.load("GUI_images/data/images/button_images/folder_button_images/music click.png"),
                      1, 1, 1, 42, 29)

]

websites = {
        0: "https://www.google.com/",
        1: "https://www.youtube.com/",
        2: "https://mail.google.com/mail/u/0/#inbox",
        3: "https://web.whatsapp.com/",
        4: "https://stackoverflow.com/",
        5: "https://www.geeksforgeeks.org/",
        6: "https://www.flaticon.com/",
        7: "https://fontjoy.com/",
        8: "https://lospec.com/palette-list"

}
folder_paths = {
        0: "F:/00Downloads/Images",
        1: "C:/Users/Admin/Documents",
        2: "F:/00Downloads",
        3: "F:/0Softwares/4KDownload/4kvideodownloader/Videos",
        4: "F:/Images and stuff/Music"

}

# location(x, y)
circle_anim = 0
circle_anim2 = 0
circles = [(1453 + 1, (173 + 1), 15, 15),
           (1453 + 1, (200 + 1), 15, 15),
           (1453 + 1, (227 + 1), 15, 15),
           (1453 + 1, (227 + 1) + 27, 15, 15),
           (1453 + 1, (227 + 1) + 27 + 27, 15, 15),
           (1453 + 1, (227 + 1) + 27 + 27 + 27, 15, 15),
           (1453 + 1, (227 + 1) + 27 + 27 + 27 + 27, 15, 15),
           (1453 + 1, (227 + 1) + 27 + 27 + 27 + 27 + 27, 15, 15),
           (1453 + 1, (227 + 1) + 27 + 27 + 27 + 27 + 27 + 27, 15, 15)]


# timer = 0
# FONT2 = pygame.font.Font('GUI_images/Machine Regular.ttf', 24)
# images = [pygame.image.load(
#     f"GUI_images/hulkbuster2/{i}").convert_alpha() for i in range(1, 100)]

# index = 0
# images = []
# for i in range(1, 100):

#     i = str(i)

#     if len(i) == 1:
#         i = "000"+i
#     if len(i) == 2:
#         i = "00"+i
#     if
# Hot teen with huge tits gets fucked hard - teen porn
#
# PauseMute
# Mover settingsDownloadDouble player sizeFullscreen
# 00:28 len(i) == 3:
#         i = "0"+i
#     s = pygame.image.load(f"GUI_images/hulkbuster2/{i}.png").convert()
#     s = pygame.transform.scale(s, (int(1080/3), int(1920/3)))

#     images.append(s)
#     images.append(s)
#     images.append(s)
# c_image = images[index]
# ********************************************************


def initializeTrackbars(intialTracbarVals=0):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 750, 240)
    cv2.createTrackbar("Threshold1", "Trackbars", 1000, 1000, nothing)


def valTrackbars():
    Threshold1 = cv2.getTrackbarPos("Threshold1", "Trackbars")
    return Threshold1


def line(p1, p2, color, w):
    pygame.draw.line(pre_draw_screen, color, p1, p2, w)


def draw_text(text, color, x, y, font):
    t = font.render(str(text), True, color)
    pre_draw_screen.blit(t, (x, y))


def static_stuff():
    global rad
    pre_draw_screen.blit(side_arrow, (0, 0))

    # r2 = math.radians(rad + 90)
    # pygame.draw.arc(screen,(28,239,233),(144,175,142,142),r,r2,5)
    # line((133,166),(133,366),(8,62,48),2)


def DrawArc(surface, color, center, radius, startAngle, stopAngle, width=1):
    # width -= 2
    for i in range(0, 3):
        # (2pi rad) / (360 deg)
        deg2Rad = 0.01745329251
        rect = pygame.Rect(
                center[0] + i,
                center[1],
                radius,
                radius
        )

        pygame.draw.arc(
                surface,
                color,
                rect,
                startAngle * deg2Rad,
                stopAngle * deg2Rad,
                width
        )


def live_update():
    global rad, temp_circle, power_circle_anim, direction, circle_anim, circle_anim2

    rad += 3

    if rad > 360:
        rad = 0

    circle_anim2 += 3
    circle_anim += 3

    if circle_anim2 < 0: circle_anim2 = 360
    if circle_anim > 360: circle_anim = 0

    temp_circle += 1

    if temp_circle > 360:
        temp_circle = 0

    power_circle_anim += 2

    if power_circle_anim > 360:
        power_circle_anim = 0
        # direction *= -1

    r = (math.radians(rad), math.radians(rad + 90))
    pygame.draw.arc(pre_draw_screen, (28, 239, 233),
                    (160, 190, 112, 112), r[0], r[1], 8)

    percent = np.interp(int(humidity_percent), (0, 100), (0, 360))

    r = (math.radians(0), math.radians(percent))

    DrawArc(pre_draw_screen, COLOR_BLUE_MAIN, (171, 35), 114, 0, percent, 8)

    pygame.draw.arc(pre_draw_screen, (28, 239, 233),
                    (176, 38, 106, 106), r[0], r[1], 4)
    pygame.draw.arc(pre_draw_screen, (28, 239, 233),
                    (177 - 4, 39 - 4, 105 + 8, 105 + 8), r[0], r[1], 4)

    # r = (math.radians(0), math.radians(90))
    # pygame.draw.arc(screen, COLOR_BLUE_LIGHT,
    #                 (187 - 4, 49 - 4,
    #                  84+8, 84+8), r[0], r[1], 16)

    # pygame.draw.arc(screen, (28, 239, 233),
    #                 (178-4, 40-4, 104+4, 104+4), r[0], r[1], 4)

    r = (math.radians(0), math.radians(360))

    r2 = 0
    DrawArc(pre_draw_screen, COLOR_BLUE_LIGHT, (187, 49), 84, temp_circle, temp_circle + 90, 10)
    # DrawArc(screen, COLOR_BLUE_LIGHT, (180+r, 42+r), 98-(r*2), temp_circle, temp_circle+90, 1)
    r = (math.radians(temp_circle), math.radians(temp_circle + 90))

    pygame.draw.arc(pre_draw_screen, COLOR_BLUE_LIGHT,
                    (183, 45, 92, 92), r[0], r[1], 2)

    r = (math.radians(0), math.radians(360))

    r2 = 0
    # DrawArc(screen, COLOR_BLUE_LIGHT, (180+r, 42+r), 98-(r*2), temp_circle, temp_circle+90, 1)
    r = (math.radians(power_circle_anim), math.radians(power_circle_anim + 270))
    a, b, c, d = 178, 420, 50, 50
    DrawArc(pre_draw_screen, COLOR_BLUE_MAIN, (178, 420), 50, power_circle_anim, power_circle_anim + 270, 4)

    pygame.draw.arc(pre_draw_screen, COLOR_BLUE_MAIN,
                    (178, 420, 50, 50), r[0], r[1], 4)

    for index, bt in enumerate(websites_buttons):
        bt.update()
        bt.draw(pre_draw_screen)

        if bt.is_clicked(): webbrowser.open(websites[index])
    for index, bt in enumerate(folder_buttons):
        bt.update()
        bt.draw(pre_draw_screen)

        if bt.is_clicked(): webbrowser.open(folder_paths[index])
    for index, circle in enumerate(circles):
        if index % 2:
            r = (math.radians(circle_anim2), math.radians(circle_anim2 + 270))
        else:
            r = (math.radians(circle_anim), math.radians(circle_anim + 270))
        pygame.draw.arc(pre_draw_screen, COLOR_BLUE_MAIN,
                        circle, r[0], r[1], 2)

    # pygame.draw.arc(screen, (28, 239, 233),
    #                 (169,200,94,94), r2[0], r2[1], 2)


def startup_updates():
    global FONT
    now = datetime.now()
    month_num = str(now).split("-")[1]
    date = str(now).split("-")[2].split(" ")[0]
    day = now.strftime("%A")
    year = now.year
    month_str = months[month_num]
    # print(month_str)
    # a,b,c = valTrackbars()

    # FONTS["date"] = pygame.font.Font('GUI_images/Fonts/NovaRound-Regular.ttf',  c, bold=pygame.font.Font.bold)

    draw_text(day, COLOR_BLUE_DARK, 276, 195, FONTS["day"])
    draw_text(year, COLOR_BLUE_DARK, 263, 178, FONTS["year"])
    draw_text(month_str, COLOR_BLUE_DARK, 180, 214, FONTS["month name"])

    draw_text(date, COLOR_BLUE_MAIN, 182, 232, FONTS["date"])

    draw_text(temperature, COLOR_BLUE_MAIN, 205, 70, FONTS["temperature"])

    # a, b, c, d = valTrackbars()

    # FONTS["full capacity"] = pygame.font.Font('GUI_images/Fonts/Teko-Medium.ttf', 25)

    draw_text(str(round((int(hdd.total) / (2 ** 30)))) + " G", COLOR_BLUE_MAIN, 250, 324, FONTS["full capacity"])
    draw_text(str(round((int(hdd.free) / (2 ** 30)), 2)) + " G", COLOR_BLUE_MAIN, 255, 362, FONTS["full capacity"])
    # a, b, c, d = valTrackbars()
    FONTS["news font"] = pygame.font.Font('GUI_images/Fonts/Teko-Medium.ttf', 15)
    h = draw_news(350, 58, 132, news_num=0)
    draw_news(350, 58 + (h + 15), 132, news_num=1)

    # t = FONT.render(str("HELLO"), True, COLOR_BLUE_MAIN)
    # screen.blit(t, (50, 50))
    #
    # t2 = FONT2.render(str("HELLO"), True, COLOR_BLUE_MAIN)
    # screen.blit(t2, (t.get_width() +50, 50))


def draw_news(x, y, d, news_num=0):
    # draw_text(news["articles"][0]["title"], COLOR_BLUE_LIGHT, 500 + x, y + (1 * d), FONTS["news font"])
    x += 500
    title = news["articles"][news_num]["title"].split(" - ")[0]
    words = title.split(" ")
    words = [word + " " for word in words]
    word_surfaces: List[pygame.Surface] = [FONTS["news font"].render(str(word), True, COLOR_BLUE_LIGHT) for word in
                                           words]

    width_of_sentence = 0
    height_of_sentence = 0
    h = word_surfaces[0].get_height()

    for ws in word_surfaces:
        pre_draw_screen.blit(ws, (x + width_of_sentence, y + height_of_sentence))
        width_of_sentence += ws.get_width()
        if width_of_sentence > d:
            height_of_sentence += h
            width_of_sentence = 0

    return height_of_sentence + h


def nothing(x):
    pass


def draw_window():
    pre_draw_screen.fill((0, 0, 0))
    pre_draw_screen.blit(background, (437, 120))
    static_stuff()
    live_update()
    startup_updates()

    bt_reboot.draw(pre_draw_screen)
    bt_eject.draw(pre_draw_screen)
    tp = pygame.transform.smoothscale(pre_draw_screen, (final_sw, final_sh))
    main_screen.blit(tp, (0, 0))

    # draw_text(str(pygame.mouse.get_pos()), COLOR_WHITE, screenWidth - 250, 0, FONTS["date"])

    # pygame.draw.rect(screen,(255,255,255),bt_reboot.rect,2)
    pygame.display.flip()


reboot = False
changing_screen = False
while True:
    if keyboard.is_pressed('ctrl + shift + a') or bt_eject.is_clicked() or bt_reboot.is_clicked():
        pygame.quit()
        sys.exit()
    if keyboard.is_pressed("ctrl+shift+w"):
        # if not changing_screen:initializeTrackbars()
        # changing_screen = True

        try:
            a = valTrackbars()
            final_sw = int(screenWidth * (a / 500))
            final_sh = int(screenHeight * (a / 500))
            main_screen = pygame.display.set_mode((final_sw, final_sh))
        except cv2.error:
            initializeTrackbars()

    # index += 1
    # if index >= len(images)-1:
    #     index = 0

    # c_image = images[index]
    # a, b, c, d = valTrackbars()
    # bt_eject.rect = pygame.Rect(a, b, c, d)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                print("reloading image")
                side_arrow = pygame.image.load("GUI_images/side arrow.png").convert_alpha()

    bt_reboot.update()
    bt_eject.update()

    reboot = bt_reboot.is_clicked()

    draw_window()
    clock.tick(FPS)
