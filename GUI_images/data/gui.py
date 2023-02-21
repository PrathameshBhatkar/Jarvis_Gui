"""
This is a ParticalSystem in pygame
Created on: 13:09:2021
Time: 09:34:30
"""
from tkinter.filedialog import asksaveasfilename

import os
import json
import keyboard
from typing import Type
from PyQt5 import QtGui
import random
from threading import Thread
import pygame
import sys
from pygame.math import Vector2
from PyQt5 import QtCore, QtWidgets


class Particle:
    def __init__(self, loc: Vector2, start_vel: Vector2, color, life, life_span=.1, gravity=Type[Vector2],
                 color2=(0, 0, 0)):
        self.life = life
        self.life_span = self.life / life_span / 60
        self.life_span *= 2
        self.loc = loc
        self.color = color
        self.color_ori = self.color
        self.color2 = color2
        self.vel = start_vel
        self.gravity = gravity

    def draw(self, win):
        color2 = [self.color[0],self.color[1],self.color[2]]
        if color2[0] > 255: color2[0] = 255
        if color2[1] > 255: color2[1] = 255
        if color2[2] > 255: color2[2] = 255

        if color2[0] < 0: color2[0] = 0
        if color2[1] < 0: color2[1] = 0
        if color2[2] < 0: color2[2] = 0


        pygame.draw.circle(win, (color2[0],color2[1],color2[2]), (self.loc[0], self.loc[1]), self.life)

    def update(self):
        if not self.color2 == (0, 0, 0):
            # print(self.life)
            percent = self.life / 10
            # print(self.life,percent)
            print()

            resultRed = self.color_ori[0] + percent * (self.color2[0] - self.color_ori[0])
            resultGreen = self.color_ori[1] + percent * (self.color2[1] - self.color_ori[1])
            resultBlue = self.color_ori[2] + percent * (self.color2[2] - self.color_ori[2])
            if resultRed > 255:resultRed = 255
            if resultGreen > 255:resultGreen = 255
            if resultBlue > 255:resultBlue = 255
            self.color = (resultRed, resultGreen, resultBlue)
            print(self.color)

        self.life -= self.life_span
        self.vel += self.gravity
        self.loc += self.vel

        if self.life <= 0:
            del self


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(625, 673)
        MainWindow.setMinimumSize(QtCore.QSize(625, 438))
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(180, 50, 81, 80))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.redV = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.redV.setScaledContents(False)
        self.redV.setAlignment(QtCore.Qt.AlignCenter)
        self.redV.setObjectName("redV")
        self.verticalLayout.addWidget(self.redV)
        self.redVinput = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.redVinput.setMaxLength(3)
        self.redVinput.setAlignment(QtCore.Qt.AlignCenter)
        self.redVinput.setClearButtonEnabled(True)
        self.redVinput.setObjectName("redVinput")
        self.verticalLayout.addWidget(self.redVinput)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(270, 50, 81, 80))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.GreenV = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.GreenV.setScaledContents(False)
        self.GreenV.setAlignment(QtCore.Qt.AlignCenter)
        self.GreenV.setObjectName("GreenV")
        self.verticalLayout_2.addWidget(self.GreenV)
        self.greenVinput = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.greenVinput.setMaxLength(3)
        self.greenVinput.setAlignment(QtCore.Qt.AlignCenter)
        self.greenVinput.setClearButtonEnabled(True)
        self.greenVinput.setObjectName("greenVinput")
        self.verticalLayout_2.addWidget(self.greenVinput)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(360, 50, 81, 80))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.blueV = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.blueV.setScaledContents(False)
        self.blueV.setAlignment(QtCore.Qt.AlignCenter)
        self.blueV.setObjectName("blueV")
        self.verticalLayout_3.addWidget(self.blueV)
        self.blueVinput = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        self.blueVinput.setMaxLength(3)
        self.blueVinput.setAlignment(QtCore.Qt.AlignCenter)
        self.blueVinput.setClearButtonEnabled(True)
        self.blueVinput.setObjectName("blueVinput")
        self.verticalLayout_3.addWidget(self.blueVinput)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 289, 611, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gravityVertical = QtWidgets.QSlider(self.horizontalLayoutWidget)
        self.gravityVertical.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        self.gravityVertical.setMinimum(-25)
        self.gravityVertical.setMaximum(25)
        self.gravityVertical.setPageStep(1)
        self.gravityVertical.setOrientation(QtCore.Qt.Horizontal)
        self.gravityVertical.setObjectName("gravityVertical")
        self.horizontalLayout.addWidget(self.gravityVertical)
        self.gravityVerticalLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.gravityVerticalLabel.setObjectName("gravityVerticalLabel")
        self.horizontalLayout.addWidget(self.gravityVerticalLabel)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 490, 611, 41))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.particals_per_sec_slider = QtWidgets.QSlider(self.horizontalLayoutWidget_2)
        self.particals_per_sec_slider.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        self.particals_per_sec_slider.setMinimum(1)
        self.particals_per_sec_slider.setMaximum(60)
        self.particals_per_sec_slider.setPageStep(1)
        self.particals_per_sec_slider.setOrientation(QtCore.Qt.Horizontal)
        self.particals_per_sec_slider.setObjectName("particals_per_sec_slider")
        self.horizontalLayout_2.addWidget(self.particals_per_sec_slider)
        self.particals_per_sec_label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.particals_per_sec_label.setObjectName("particals_per_sec_label")
        self.horizontalLayout_2.addWidget(self.particals_per_sec_label)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(0, 530, 610, 40))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.life_span_slider = QtWidgets.QSlider(self.horizontalLayoutWidget_3)
        self.life_span_slider.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        self.life_span_slider.setMinimum(1)
        self.life_span_slider.setMaximum(25)
        self.life_span_slider.setPageStep(1)
        self.life_span_slider.setOrientation(QtCore.Qt.Horizontal)
        self.life_span_slider.setObjectName("life_span_slider")
        self.horizontalLayout_3.addWidget(self.life_span_slider)
        self.life_span_label = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.life_span_label.setObjectName("life_span_label")
        self.horizontalLayout_3.addWidget(self.life_span_label)
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(0, 430, 611, 41))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.Horizontalforce = QtWidgets.QSlider(self.horizontalLayoutWidget_4)
        self.Horizontalforce.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        self.Horizontalforce.setMinimum(0)
        self.Horizontalforce.setMaximum(25)
        self.Horizontalforce.setPageStep(1)
        self.Horizontalforce.setOrientation(QtCore.Qt.Horizontal)
        self.Horizontalforce.setObjectName("Horizontalforce")
        self.horizontalLayout_4.addWidget(self.Horizontalforce)
        self.HorizontalforceLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        self.HorizontalforceLabel.setObjectName("HorizontalforceLabel")
        self.horizontalLayout_4.addWidget(self.HorizontalforceLabel)
        self.horizontalLayoutWidget_5 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(0, 329, 611, 41))
        self.horizontalLayoutWidget_5.setObjectName("horizontalLayoutWidget_5")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.gravityHorizontal = QtWidgets.QSlider(self.horizontalLayoutWidget_5)
        self.gravityHorizontal.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        self.gravityHorizontal.setMinimum(-25)
        self.gravityHorizontal.setMaximum(25)
        self.gravityHorizontal.setPageStep(1)
        self.gravityHorizontal.setOrientation(QtCore.Qt.Horizontal)
        self.gravityHorizontal.setObjectName("gravityHorizontal")
        self.horizontalLayout_5.addWidget(self.gravityHorizontal)
        self.gravityHorizontalLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_5)
        self.gravityHorizontalLabel.setObjectName("gravityHorizontalLabel")
        self.horizontalLayout_5.addWidget(self.gravityHorizontalLabel)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(250, 10, 110, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayoutWidget_6 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_6.setGeometry(QtCore.QRect(0, 390, 611, 41))
        self.horizontalLayoutWidget_6.setObjectName("horizontalLayoutWidget_6")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_6)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.VerticalForce = QtWidgets.QSlider(self.horizontalLayoutWidget_6)
        self.VerticalForce.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        self.VerticalForce.setMinimum(0)
        self.VerticalForce.setMaximum(25)
        self.VerticalForce.setPageStep(1)
        self.VerticalForce.setOrientation(QtCore.Qt.Horizontal)
        self.VerticalForce.setObjectName("VerticalForce")
        self.horizontalLayout_6.addWidget(self.VerticalForce)
        self.VerticalForceLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        self.VerticalForceLabel.setObjectName("VerticalForceLabel")
        self.horizontalLayout_6.addWidget(self.VerticalForceLabel)
        self.mradioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.mradioButton.setGeometry(QtCore.QRect(240, 140, 141, 41))
        self.mradioButton.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.mradioButton.setFont(font)
        self.mradioButton.setObjectName("mradioButton")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(360, 190, 81, 80))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.blueV_2 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.blueV_2.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.blueV_2.setScaledContents(False)
        self.blueV_2.setAlignment(QtCore.Qt.AlignCenter)
        self.blueV_2.setObjectName("blueV_2")
        self.verticalLayout_4.addWidget(self.blueV_2)
        self.blueVinput_2 = QtWidgets.QLineEdit(self.verticalLayoutWidget_4)
        self.blueVinput_2.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.blueVinput_2.setMaxLength(3)
        self.blueVinput_2.setAlignment(QtCore.Qt.AlignCenter)
        self.blueVinput_2.setDragEnabled(False)
        self.blueVinput_2.setClearButtonEnabled(True)
        self.blueVinput_2.setObjectName("blueVinput_2")
        self.verticalLayout_4.addWidget(self.blueVinput_2)
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(180, 190, 81, 80))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.redV_2 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.redV_2.setScaledContents(False)
        self.redV_2.setAlignment(QtCore.Qt.AlignCenter)
        self.redV_2.setObjectName("redV_2")
        self.verticalLayout_5.addWidget(self.redV_2)
        self.redVinput_2 = QtWidgets.QLineEdit(self.verticalLayoutWidget_5)
        self.redVinput_2.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.redVinput_2.setMaxLength(3)
        self.redVinput_2.setAlignment(QtCore.Qt.AlignCenter)
        self.redVinput_2.setDragEnabled(False)
        self.redVinput_2.setClearButtonEnabled(True)
        self.redVinput_2.setObjectName("redVinput_2")
        self.verticalLayout_5.addWidget(self.redVinput_2)
        self.verticalLayoutWidget_6 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(270, 190, 81, 80))
        self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.GreenV_2 = QtWidgets.QLabel(self.verticalLayoutWidget_6)
        self.GreenV_2.setScaledContents(False)
        self.GreenV_2.setAlignment(QtCore.Qt.AlignCenter)
        self.GreenV_2.setObjectName("GreenV_2")
        self.verticalLayout_6.addWidget(self.GreenV_2)
        self.greenVinput_2 = QtWidgets.QLineEdit(self.verticalLayoutWidget_6)
        self.greenVinput_2.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.greenVinput_2.setMaxLength(3)
        self.greenVinput_2.setAlignment(QtCore.Qt.AlignCenter)
        self.greenVinput_2.setDragEnabled(False)
        self.greenVinput_2.setClearButtonEnabled(True)
        self.greenVinput_2.setObjectName("greenVinput_2")
        self.verticalLayout_6.addWidget(self.greenVinput_2)
        self.particle_name = QtWidgets.QLineEdit(self.centralwidget)
        self.particle_name.setGeometry(QtCore.QRect(210, 590, 121, 40))
        self.particle_name.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.particle_name.setText("")
        self.particle_name.setAlignment(QtCore.Qt.AlignCenter)
        self.particle_name.setDragEnabled(False)
        self.particle_name.setClearButtonEnabled(True)
        self.particle_name.setObjectName("particle_name")
        self.msize_input = QtWidgets.QLineEdit(self.centralwidget)
        self.msize_input.setGeometry(QtCore.QRect(40, 50, 79, 20))
        self.msize_input.setToolTipDuration(-1)
        self.msize_input.setMaxLength(15)
        self.msize_input.setAlignment(QtCore.Qt.AlignCenter)
        self.msize_input.setCursorMoveStyle(QtCore.Qt.VisualMoveStyle)
        self.msize_input.setClearButtonEnabled(False)
        self.msize_input.setObjectName("msize_input")
        self.m_size_label = QtWidgets.QLabel(self.centralwidget)
        self.m_size_label.setGeometry(QtCore.QRect(30, 20, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.m_size_label.setFont(font)
        self.m_size_label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.m_size_label.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.m_size_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.m_size_label.setAlignment(QtCore.Qt.AlignCenter)
        self.m_size_label.setObjectName("m_size_label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 625, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.redV.setText(_translate("MainWindow", "Red"))
        self.redVinput.setPlaceholderText(_translate("MainWindow", "255"))
        self.GreenV.setText(_translate("MainWindow", "Green"))
        self.greenVinput.setPlaceholderText(_translate("MainWindow", "255"))
        self.blueV.setText(_translate("MainWindow", "Blue"))
        self.blueVinput.setPlaceholderText(_translate("MainWindow", "255"))
        self.gravityVerticalLabel.setText(_translate("MainWindow", " Gravity Vertical   "))
        self.particals_per_sec_label.setText(_translate("MainWindow", "Particals Per Sec"))
        self.life_span_label.setText(_translate("MainWindow", "      Life Span      "))
        self.HorizontalforceLabel.setText(_translate("MainWindow", "Horizontal Force"))
        self.gravityHorizontalLabel.setText(_translate("MainWindow", "Gravity Horizontal"))
        self.label.setWhatsThis(_translate("MainWindow", "jghjghj"))
        self.label.setText(_translate("MainWindow", "Primary Colors"))
        self.VerticalForceLabel.setText(_translate("MainWindow", "Vertical Force    "))
        self.redVinput.setText('255')
        self.greenVinput.setText('255')
        self.blueVinput.setText('255')

        self.redVinput_2.setText('255')
        self.greenVinput_2.setText('255')
        self.blueVinput_2.setText('255')

        self.mradioButton.setText(_translate("MainWindow", "RadioButton"))
        # self.mlabel.setText(_translate("MainWindow", "TextLabel"))
        # self.mradioButton.setText(_translate("MainWindow", "SecondaryColors"))
        self.mradioButton.setText(_translate("MainWindow", "Secondary Colors"))
        self.blueV_2.setText(_translate("MainWindow", "Blue2"))
        self.blueVinput_2.setPlaceholderText(_translate("MainWindow", "255"))
        self.redV_2.setText(_translate("MainWindow", "Red2"))
        self.redVinput_2.setPlaceholderText(_translate("MainWindow", "255"))
        self.GreenV_2.setText(_translate("MainWindow", "Green2"))
        self.greenVinput_2.setPlaceholderText(_translate("MainWindow", "255"))
        self.particle_name.setPlaceholderText(_translate("MainWindow", "particle_1"))
        self.msize_input.setText(_translate("MainWindow", "10"))
        self.msize_input.setPlaceholderText(_translate("MainWindow", "Starting Size"))
        self.m_size_label.setText(_translate("MainWindow", "Starting Size"))


ui = Ui_MainWindow()


def start():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


def appendText(text_ui, text_to_replace):
    # before_text=text_ui.text()
    text_ui.setText(text_to_replace)


Thread(target=start).start()

pygame.init()
# *****************-- Normal Variables --*****************
screenHeight = 800
screenWidth = 1500
FPS = 60

# Colour
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)

COLOR_GRAY = (100, 100, 100)
COLOR_LIGHT_GRAY = (200, 200, 200)
COLOR_DARK_GRAY = (50, 50, 50)

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

COLOR_YELLOW = (255, 255, 0)
COLOR_PINK = (255, 0, 255)

# *****************-- SystemCore Variables --*************
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('ParticalSystem in pygame')
clock = pygame.time.Clock()
# ********************************************************
pl = []
try:
    color = (int(ui.redVinput.text()), int(ui.greenVinput.text()), int(ui.blueVinput.text()))
except:
    pass


def draw_window():
    screen.fill(COLOR_DARK_GRAY)


def updateTexts():
    appendText(ui.gravityVerticalLabel, f" Gravity Vertical :{g.y}  ")
    appendText(ui.gravityHorizontalLabel, f" Gravity Horizontal :{g.x}  ")

    appendText(ui.HorizontalforceLabel, f"Horizontal Force :{force.x}  ")
    appendText(ui.VerticalForceLabel, f"Vertical Force :{force.y}  ")

    appendText(ui.life_span_label, f"Life Span:{life_span}")
    appendText(ui.particals_per_sec_label, f"Particles Per Sec :{60 - particles_per_sec}")


counter = 0
FONT = pygame.font.SysFont("comicsans", 35)

while True:
    draw_window()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    try:
        color = (int(ui.redVinput.text()), int(ui.greenVinput.text()), int(ui.blueVinput.text()))
        # value below too big so devide it by 2
        g = Vector2(int(ui.gravityHorizontal.value()) / 2, int(ui.gravityVertical.value()) / 2)
        life_span = int(ui.life_span_slider.value()) / 2
        particles_per_sec = int(ui.particals_per_sec_slider.value())
        life = int(ui.msize_input.text())
        force = Vector2(
            int(ui.Horizontalforce.value()),
            int(ui.VerticalForce.value())
        )

        particles_per_sec = 61 - particles_per_sec
        counter += 1
        updateTexts()

        # resultRed = color1.red + percent * (color2.red - color1.red)

        # resultGreen = color1.green + percent * (color2.green - color1.green)
        # resultBlue = color1.blue + percent * (color2.blue - color1.blue)
        # print(ui.mradioButton.isChecked())

        is_visible = ui.mradioButton.isChecked()
        print(len(pl))

        if keyboard.is_pressed('ctrl + s'):
            d = { }

            savePath = asksaveasfilename()
            if not ('.json' in savePath):
                savePath = savePath + '.json'
            file_name = str(savePath).split('/')[-1]
            name = file_name.split('.')[0]

            particle_name = ui.particle_name.text()
            if os.path.isfile(savePath):
                with open(savePath) as f:
                    d = json.load(f)
                os.remove(savePath)

            d[particle_name] = {
                "gravity_horizontal": g.x,
                "gravity_vertical": g.y,
                "horizontal_force": force.x,
                "vertical_force": force.y,
                "particles_per_sec": particles_per_sec,
                "life": life,
                "life_span": life_span,
                "color1": color,
                "color2": (c1, c2, c3)

            }
            with open(savePath, 'a') as f:
                json.dump(d, f)

            print(d)

        for widget in [ui.redV_2, ui.GreenV_2, ui.blueV_2, ui.redVinput_2, ui.greenVinput_2, ui.blueVinput_2]:
            widget.setVisible(is_visible)

        if counter % particles_per_sec == 0:
            c1, c2, c3 = int(ui.redVinput_2.text()), int(ui.greenVinput_2.text()), int(ui.blueVinput_2.text())
            pl.append(
                Particle(Vector2(screenWidth / 2, screenHeight / 2), Vector2(0, 0), color, life=life,
                         life_span=life_span,
                         gravity=g, color2=(0, 0, 0) if not is_visible else (c1, c2, c3)))

        for _x, p in enumerate(pl):
            p.vel[0] = random.randint(int(-force.x), int(force.x)) / (p.life * 2) * 25
            p.vel[1] = random.randint(int(-force.y), int(force.y)) / (p.life * 2) * 25
            p.update()

            p.draw(screen)

            if p.life <= 0:
                pl.pop(_x)
    except ValueError as e:
        print(e)

    # print(len(pl))

    t = FONT.render(f"Fps: {clock.tick(FPS)}", False, COLOR_WHITE)
    screen.blit(t, (10, 10))

    t = FONT.render(f"{len(pl)} Particles", False, COLOR_WHITE)
    screen.blit(t, (10, 10 + t.get_height()))

    pygame.display.flip()
