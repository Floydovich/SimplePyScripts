#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, 'Error', text)
    quit()


import sys
sys.excepthook = log_uncaught_exceptions


def get_feeds_by_manga_chapters(url_rss: str) -> list:
    import requests
    rss_text = requests.get(url_rss).text

    import feedparser
    feed = feedparser.parse(rss_text)

    return [(entry.title, entry.link) for entry in feed.entries]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('show_user_grouple_rss__qt')

        self.line_edit_url_user = QLineEdit()
        self.line_edit_id_user = QLineEdit()
        self.line_edit_rss_user = QLineEdit()

        self.line_edit_url_user.textChanged.connect(self._on_line_edit_url_user_text_changed)
        self.line_edit_id_user.textChanged.connect(self._on_line_edit_id_user_text_changed)

        self.push_button_start = QPushButton('Start')
        self.push_button_start.clicked.connect(self._start)

        self.list_widget_feeds = QListWidget()
        self.list_widget_feeds.itemDoubleClicked.connect(self._on_item_double_clicked)

        layout_url_user = QHBoxLayout()
        layout_url_user.addWidget(QLabel('Url user:'))
        layout_url_user.addWidget(self.line_edit_url_user)
        layout_url_user.addWidget(QLabel('ID user:'))
        layout_url_user.addWidget(self.line_edit_id_user)

        layout_rss_user = QHBoxLayout()
        layout_rss_user.addWidget(QLabel('Rss user:'))
        layout_rss_user.addWidget(self.line_edit_rss_user)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout_url_user)
        main_layout.addLayout(layout_rss_user)
        main_layout.addWidget(self.push_button_start)
        main_layout.addWidget(self.list_widget_feeds)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)

        # Set default url
        self.line_edit_url_user.setText('https://grouple.co/user/315828')

    def _on_line_edit_url_user_text_changed(self, text):
        id_user = text.replace(' ', '').split('/')[-1]
        self.line_edit_id_user.setText(id_user)

    def _on_line_edit_id_user_text_changed(self, text):
        id_user = text.strip()
        self.line_edit_rss_user.setText('https://grouple.co/user/rss/{}?filter='.format(id_user))

    def _start(self):
        self.list_widget_feeds.clear()

        url_rss = self.line_edit_rss_user.text()

        for title, url in get_feeds_by_manga_chapters(url_rss):
            item = QListWidgetItem(title)
            item.setData(Qt.UserRole, url)
            item.setToolTip(url)

            self.list_widget_feeds.addItem(item)

    @staticmethod
    def _on_item_double_clicked(item):
        url = item.data(Qt.UserRole)

        import webbrowser
        webbrowser.open_new_tab(url)


if __name__ == '__main__':
    app = QApplication([])

    mw = MainWindow()
    mw.resize(600, 460)
    mw.show()

    app.exec()
