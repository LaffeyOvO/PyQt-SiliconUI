#from PySide6.Qt import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import *
#from PySide6.Qt import *
from PySide6.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit
import numpy
import time
import os

import silicon
from silicon.SiHint import *
from silicon.SiOverlay import *
from silicon.SiGlobal import *
import silicon.SiGlobal as SiGlobal

import components as Components

# 加载图标
import icons
SiGlobal.icons = icons.ICON_DICT('./icons/icons.dat', SiGlobal.colorset.SVG_HEX)

class UserInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置最小宽度
        self.setMinimumWidth(860)

        # 初始化 Hint 提示条
        self.floating_window = FloatingWindow()
        self.floating_window.setWindowOpacity(0)  # 初始隐藏小窗口
        self.floating_window.show()
        SiGlobal.floating_window = self.floating_window

        # 初始化二级界面叠加层
        self.overlay = SiOverlay(self)
        SiGlobal.overlay = self.overlay

        # 构建界面
        self.initUI()

        # 叠加层置顶
        self.overlay.raise_()

    def showEvent(self, event):
        self.overlay.showup_animation.setCurrent(self.geometry().height())
        self.overlay.moveFrame(self.geometry().height())
        self.overlay.hide()

    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()
        self.stackarea.setGeometry(0, 0, w, h)
        self.overlay.setGeometry(0, 0, w, h)

    def initUI(self):

        # 对象从属关系
        # silicon.SiTabArea
        #     silicon.SiTab （里面包含一个标题和一个silicon.SiScrollArea）
        #         silicon.SiFrame
        #             silicon.SiStack
        #                 silicon.SiOptionButton
        #                 silicon.SiOptionSwitch
        #                 silicon.SiOptionComboBox
        #                 ......

        # 初始化窗口

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, 1200, 700)
        self.setWindowTitle("Silicon Gallery")

        self.stackarea = silicon.SiTabArea(self)
        self.stackarea.setGeometry(0, 0, 1200, 600)

        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap('./img/logo.png'))
        self.logo.setGeometry(64+4, 16+4, 24, 24)

        self.window_title = QLabel(self)
        self.window_title.setStyleSheet('color: {}'.format(colorset.TEXT_GRAD_HEX[1]))
        self.window_title.setGeometry(104, 0, 500, 64)
        self.window_title.setText('Silicon Gallery')
        self.window_title.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.window_title.setFont(silicon.SiFont.font_L1_bold)

        # 初始化各个界面
        self.homepage = silicon.SiTab(self)
        self.homepage.setTitleHeight(0)
        self.homepage.scrollarea.rightside_interval = 0
        self.homepage.attachFrame(Components.Homepage.SiHomePage(self.homepage))
        self.homepage.scrollarea.scrollbar.raise_()

        self.glaze_example = silicon.SiTab(self)
        self.glaze_example.setTitle('Silicon Glaze 示例')
        self.glaze_example.attachFrame(Components.Glaze.GlazeExample(self.glaze_example))
        self.glaze_example.scrollarea.scrollbar.raise_()

        self.widgets_example = silicon.SiTab(self)
        self.widgets_example.setTitle('控件')
        self.widgets_example.attachFrame(Components.Widgets.WidgetsExample(self.widgets_example))
        self.widgets_example.scrollarea.scrollbar.raise_()

        self.experiment_field = silicon.SiTab(self)
        self.experiment_field.setTitle('实验场')
        self.experiment_field.attachFrame(Components.ExperimentField.ExperimentField(self.experiment_field))
        self.experiment_field.scrollarea.scrollbar.raise_()

        self.options = silicon.SiTab(self)
        self.options.setTitle('设置')
        self.options.attachFrame(Components.Options.Options(self.options))
        self.options.scrollarea.scrollbar.raise_()

        # 添加到 stackarea
        self.stackarea.addTab(self.homepage, SiGlobal.icons.get('fi-rr-home'), '主页面')
        self.stackarea.addTab(self.widgets_example, SiGlobal.icons.get('fi-rr-layout-fluid'), '控件')
        self.stackarea.addTab(self.glaze_example, SiGlobal.icons.get('fi-rr-list'), 'Silicon Glaze 示例')
        self.stackarea.addTab(self.experiment_field, SiGlobal.icons.get('fi-rr-bulb'), '实验场')
        self.stackarea.addTab(self.options, SiGlobal.icons.get('fi-rr-settings'), '设置', 'bottom')
