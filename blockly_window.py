#!/usr/bin/env python3




import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QVBoxLayout
from PyQt5.QtWebKitWidgets import QWebPage, QWebView
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow,QPushButton
import threading 


def get_code(webview):
    webview.page().mainFrame().evaluateJavaScript("showCode();")

x_size = 900
y_size = 560
class EditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(x_size, y_size)
        self.setup_ui()


    def setup_ui(self):

        exitAction = QAction(QIcon('editor/a.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)




        self.setMinimumSize(x_size-50, y_size)
        self.setWindowTitle('MicroPython Blockly')

        self.btn = QPushButton("Run", self)
        self.btn.resize(50, 50)
        self.btn.move(x_size-50, 0)
        self.show()

        self.show()

class WebPage(QWebPage):
    def __init__(self, webview, _event=None):
        super().__init__()
        self.webview = webview
        self._event = _event

    def javaScriptAlert(self, _x, msg):
        self._event(msg)

class BlocklyThread(threading.Thread):
    def __init__(self, event):
        super().__init__()
        self.name = "BlocklyThread"
        self.event = event
        self.start()

    def run(self):
        url = 'http://marekmansell.sk/test/blockly/'
        app = QApplication([])
        editor_window = EditorWindow()

        layout = QVBoxLayout()

        browser = QWebView(editor_window)
        layout.addWidget(browser)
        browser.resize(x_size-50, y_size)
        page = WebPage(browser, self.event)
        browser.setPage(page)

        browser.load(QUrl(url))
        browser.show()

        editor_window.btn.clicked.connect(lambda: get_code(browser))
        sys.exit(app.exec_())


if __name__ == "__main__":
    def print_code(text):
        print("====\n{}\n====".format(text))
    blockly_thread = BlocklyThread(print_code)


