#!/usr/bin/env python

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebKit import *
from PyQt5.QtWebKitWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow,QPushButton
from time import sleep

# app = QApplication(sys.argv)
#
# web = QWebView()
# web.load(QUrl("http://marekmansell.sk/test/blockly/"))
# web.show()
#
# sys.exit(app.exec_())

#

def run(webview):
    webview.page().mainFrame().evaluateJavaScript("showCode();")

class EditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):




        exitAction = QAction(QIcon('editor/a.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)




        self.setMinimumSize(900, 400)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('editor/a.png'))
        self.statusBar()

        self.btn = QPushButton("Run", self)
        self.btn.resize(100, 50)
        self.btn.move(800, 0)
        self.show()


        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?",
                                     QMessageBox.Yes or QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()




class WebPage(QWebPage):
    def __init__(self, webview):
        super().__init__()
        self.webview = webview

    def javaScriptAlert(self, _x, msg):
        print ("====\n{}\n====".format(msg))


url = 'http://marekmansell.sk/test/blockly/'
app = QApplication([])
editor_window = EditorWindow()

layout = QVBoxLayout()
editor_window.resize(900, 500)
browser = QWebView(editor_window)
layout.addWidget(browser)
browser.resize(790, 490)
bt = QPushButton("s", editor_window)
layout.addWidget(bt)
page = WebPage(browser)
browser.setPage(page)
browser.load(QUrl(url))
browser.show()

editor_window.btn.clicked.connect(lambda: run(browser))
sys.exit(app.exec_())
