from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class BrowserTab(QWidget):
    def __init__(self, parent=None):
        super(BrowserTab, self).__init__(parent)

        self.browser = QWebEngineView(self)
        self.browser.setUrl(QUrl('http://google.com'))

        self.navbar = QToolBar(self)
        self.navbar.setMovable(False)

        layout = QVBoxLayout(self)
        layout.addWidget(self.navbar)
        layout.addWidget(self.browser)

    def navigate_home(self):
        self.browser.setUrl(QUrl('https://google.com'))

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(BrowserTab, self).__init__(parent)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        self.setCentralWidget(self.tabs)
        self.showMaximized()
        self.browser.titleChanged.connect(self.update_tab_title)

        # Barra de herramientas principal
        navbar = QToolBar()
        self.addToolBar(navbar)

        add_tab_btn = QAction('Nueva Pestaña', self)
        add_tab_btn.triggered.connect(self.add_new_tab)
        navbar.addAction(add_tab_btn)

        back_btn = QAction('Back', self)
        back_btn.triggered.connect(self.current_tab_back)
        navbar.addAction(back_btn)

        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(self.current_tab_forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(self.current_tab_reload)
        navbar.addAction(reload_btn)

        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.current_tab_home)
        navbar.addAction(home_btn)

        # Barra de herramientas para la URL
        url_input_toolbar = QToolBar()
        self.addToolBar(url_input_toolbar)

        self.url_input = QLineEdit()
        self.url_input.returnPressed.connect(self.navigate_to_url)
        url_input_toolbar.addWidget(self.url_input)

        self.add_new_tab()

    def add_new_tab(self):
        tab = BrowserTab(self)
        self.tabs.addTab(tab, "Nueva Pestaña")

    def close_tab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    def current_tab_back(self):
        current_tab = self.tabs.currentWidget()
        current_tab.browser.back()

    def current_tab_forward(self):
        current_tab = self.tabs.currentWidget()
        current_tab.browser.forward()

    def current_tab_reload(self):
        current_tab = self.tabs.currentWidget()
        current_tab.browser.reload()

    def current_tab_home(self):
        current_tab = self.tabs.currentWidget()
        current_tab.navigate_home()

    def navigate_to_url(self):
        current_tab = self.tabs.currentWidget()
        url = self.url_input.text()

        # Agregar un esquema predeterminado si no está presente
        if not url.startswith(('http://', 'https://', 'file://')):
            url = 'http://' + url

        current_tab.browser.setUrl(QUrl(url))

app = QApplication([])
QApplication.setApplicationName('Pixel Browser')
window = MainWindow()
window.show()
app.exec_()
