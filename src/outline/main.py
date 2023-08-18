from PyQt5 import QtCore, QtWidgets

from plug.qt.plugs import TreePlug

class Outline(TreePlug):

    def __init__(self, app): 

        super().__init__(app=app, 
                         position='left', 
                         mode_keys={'command':'o'})

    def setUI(self):

        super().setUI()

        self.ui.main.tree.m_expansionRole=QtCore.Qt.UserRole+4
        self.ui.main.tree.m_expansionIDRole=QtCore.Qt.UserRole+5

        self.ui.main.tree.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.ui.main.tree.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.ui.main.tree.header().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)

    def on_outlineClicked(self, index=None):

        if index is None: index=self.ui.main.tree.currentIndex()
        if index:
            page=index.data(QtCore.Qt.UserRole+1)
            left=index.data(QtCore.Qt.UserRole+2)
            top=index.data(QtCore.Qt.UserRole+3)

            self.app.main.display.itemChanged.disconnect(self.on_viewItemChanged)
            self.app.main.display.currentView().goto(page, left, top)
            self.app.main.display.itemChanged.connect(self.on_viewItemChanged)

    def on_viewItemChanged(self, model, pageItem):

        if self.outline:
            return
            page=pageItem.page().pageNumber()
            found=self.find(page)
            if found: self.ui.main.tree.setCurrentIndex(found)

    def find(self, page): return super().find(page, self.outline)

    def open(self, how='reset', focus=True):

        self.app.main.display.viewChanged.disconnect(self.on_viewChanged)
        self.app.main.display.itemChanged.disconnect(self.on_viewItemChanged)

        index=self.ui.main.tree.currentIndex()
        if index:
            page=index.data(QtCore.Qt.UserRole+1)
            left=index.data(QtCore.Qt.UserRole+2)
            top=index.data(QtCore.Qt.UserRole+3)
            self.app.main.display.currentView().goto(page, left, top)
            super().open(how, focus)

        self.app.main.display.viewChanged.connect(self.on_viewChanged)
        self.app.main.display.itemChanged.connect(self.on_viewItemChanged)

    def setData(self):

        self.outline=None
        view=self.app.main.display.view
        if view:
            document=view.model()
            self.outline=document.loadOutline()
            self.ui.main.tree.setModel(self.outline)

    def activate(self):

        self.setData()

        self.app.main.display.viewChanged.connect(self.on_viewChanged)
        self.app.main.display.itemChanged.connect(self.on_viewItemChanged)

        super().activate()

    def deactivate(self):

        self.app.main.display.viewChanged.disconnect(self.on_viewChanged)
        self.app.main.display.itemChanged.disconnect(self.on_viewItemChanged)

        super().deactivate()
