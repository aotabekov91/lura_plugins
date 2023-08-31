from PyQt5 import QtCore, QtWidgets

from plug.qt.utils import register
from plug.qt.plugs import TreePlug

class Outline(TreePlug):

    def __init__(self, 
            app,
            position='left',
            mode_keys={'command':'o'},
            **kwargs): 

        super().__init__(
                app=app, 
                position=position,
                mode_keys=mode_keys,
                **kwargs,
                )

    def setUI(self):

        super().setUI()
        self.ui.main.tree.m_expansionRole=QtCore.Qt.UserRole+4
        self.ui.main.tree.m_expansionIDRole=QtCore.Qt.UserRole+5
        self.ui.main.tree.setEditTriggers(
                QtWidgets.QAbstractItemView.NoEditTriggers)
        self.ui.main.tree.setVerticalScrollMode(
                QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.ui.main.tree.header().setSectionResizeMode(
                QtWidgets.QHeaderView.Interactive)

        # tree=self.ui.main.tree
        # tree.m_expansionRole=QtCore.Qt.UserRole+4
        # tree.m_expansionIDRole=QtCore.Qt.UserRole+5
        # tree.setEditTriggers(
        #         QtWidgets.QAbstractItemView.NoEditTriggers)
        # tree.setVerticalScrollMode(
        #         QtWidgets.QAbstractItemView.ScrollPerPixel)
        # tree.header().setSectionResizeMode(
        #         QtWidgets.QHeaderView.Interactive)

    def on_outlineClicked(self, index=None):

        if index is None: index=self.ui.main.tree.currentIndex()
        if index:
            page=index.data(QtCore.Qt.UserRole+1)
            left=index.data(QtCore.Qt.UserRole+2)
            top=index.data(QtCore.Qt.UserRole+3)

            display=self.app.window.main.display
            display.itemChanged.disconnect(
                    self.on_viewItemChanged)
            display.currentView().goto(page, left, top)
            display.itemChanged.connect(
                    self.on_viewItemChanged)

    def on_viewItemChanged(self, model, pageItem):

        if self.outline:
            page=pageItem.page().pageNumber()
            found=self.find(page)
            if found: 
                self.ui.main.tree.setCurrentIndex(found)

    def find(self, page): 

        return False
        # TODO
        # return super().find(page, self.outline)

    def open(self, how='reset', focus=True):

        display=self.app.window.main.display
        display.viewChanged.disconnect(self.on_viewChanged)
        display.itemChanged.disconnect(self.on_viewItemChanged)
        index=self.ui.main.tree.currentIndex()
        if index:
            page=index.data(QtCore.Qt.UserRole+1)
            left=index.data(QtCore.Qt.UserRole+2)
            top=index.data(QtCore.Qt.UserRole+3)
            if how!='reset':
                model=display.view.model()
                display.open(model=model,
                             how=how,
                             focus=focus)
            display.currentView().goto(
                    page, left, top)
            super().open(how, focus)
        display.viewChanged.connect(self.on_viewChanged)
        display.itemChanged.connect(self.on_viewItemChanged)

    def setData(self):

        self.outline=None
        view=self.app.window.main.display.view
        if view:
            document=view.model()
            self.outline=document.loadOutline()
            self.ui.main.tree.setModel(self.outline)

    def activate(self):

        self.setData()
        display=self.app.window.main.display
        display.viewChanged.connect(self.on_viewChanged)
        display.itemChanged.connect(self.on_viewItemChanged)
        super().activate()

    def deactivate(self):

        display=self.app.window.main.display
        display.viewChanged.disconnect(self.on_viewChanged)
        display.itemChanged.disconnect(self.on_viewItemChanged)
        super().deactivate()
