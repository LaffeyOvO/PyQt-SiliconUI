#from PySide6.Qt import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6 import QtCore, QtGui, QtWidgets

from . import SiFont
from . import SiStyle
from . import SiGlobal
from . import SiAnimationObject

from .SiGlobal import *


class LabelTextUpdateAnimation(SiAnimationObject.SiAnimation):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def stepLength(self, dis):
        return 2 if dis > 0 else -2

    def distance(self):
        return self.target - self.current

    def isCompleted(self):
        return self.distance() == 0


class SiLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.hint = ''
        self.autoAdjustSize = True
        self.setFont(SiFont.font_L1)
        self.setStyleSheet('color:{}'.format(colorset.TEXT_GRAD_HEX[0]))

    def setAutoAdjustSize(self, b):
        self.autoAdjustSize = b

    def setHint(self, hint):
        self.hint = hint

    def setText(self, text):
        super().setText(str(text))
        if self.autoAdjustSize == True:
            self.adjustSize()

    def enterEvent(self, event):
        super().enterEvent(event)
        if self.hint != '':
            SiGlobal.floating_window.show_animation()
            SiGlobal.floating_window.setText(self.hint)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        if self.hint != '':
            SiGlobal.floating_window.hide_animation()


class SiLabelHasUpdateAnimation(SiLabel):
    def __init__(self, parent):
        super().__init__(parent)

        self.animation = LabelTextUpdateAnimation(self)
        self.animation.ticked.connect(self._changedAnimationHandler)

    def setAlpha(self, alpha):
        self.setStyleSheet(self.show_stylesheet + ''';
            border-radius: 4px;
            background-color:rgba(255, 255, 255, {});
            '''.format(alpha / 255))

    def _changedAnimationHandler(self, delta):
        alpha = self.animation.current + delta
        self.animation.setCurrent(alpha)
        self.setAlpha(alpha)

    def activate(self, *any_args):
        self.animation.setCurrent(40)
        self.animation.setTarget(0)
        self.animation.try_to_start()

    def setText(self, text, ani = False):
        super().setText(text)
        if ani == True:
            self.activate()

    def showEvent(self, event):
        super().showEvent(event)
        self.show_stylesheet = self.styleSheet()


class SiPixLabel(SiLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.radius = 32
        self.path = None

    def setRadius(self, r):
        self.radius = r

    def load(self, path):
        self.path = path
        self.draw()

    def draw(self):
        if self.path is None:
            return

        w, h = self.width(), self.height()
        self.setMaximumSize(w, h)
        self.setMinimumSize(w, h)

        self.target = QPixmap(self.size())
        self.target.fill(Qt.transparent)

        p = QPixmap(self.path).scaled(
            w, h, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        painter = QPainter(self.target)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        path = QPainterPath()
        path.addRoundedRect(0, 0,
                            self.width(), self.height(),
                            self.radius, self.radius)

        painter.setClipPath(path)
        painter.drawPixmap(0, 0, p)
        self.setPixmap(self.target)
