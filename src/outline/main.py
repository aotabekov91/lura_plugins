from PyQt5 import QtCore, QtWidgets

from gizmo.utils import register
from plug.qt.plugs import TreePlug

class Outline(TreePlug):

    def __init__(
            self, 
            app,
            position='dock_left',
            leader_keys={'command':'o'},
            **kwargs): 

        super().__init__(
                app=app, 
                position=position,
                leader_keys=leader_keys,
                **kwargs,
                )
        self.cache={}

    def setup(self):

        super().setup()
        self.display=self.app.display
        self.setConnect()

    def setConnect(self):

        self.display.viewChanged.connect(
                self.on_viewChanged)
        self.display.itemChanged.connect(
                self.on_viewItemChanged)

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

    def on_outlineClicked(self, index=None):

        if index is None: 
            index=self.ui.main.tree.currentIndex()
        if index:
            page=index.data(QtCore.Qt.UserRole+1)
            left=index.data(QtCore.Qt.UserRole+2)
            top=index.data(QtCore.Qt.UserRole+3)

            self.display.itemChanged.disconnect(
                    self.on_viewItemChanged)
            self.display.currentView().goto(
                    page, left, top)
            self.display.itemChanged.connect(
                    self.on_viewItemChanged)

    def on_viewChanged(self, view):

        able=getattr(view, 'canOutline', False)
        if able:
            d=self.getData(view)
            self.ui.main.tree.setModel(d)

    def on_viewItemChanged(self, view, item):

        outline=self.getData(view)
        if outline:
            idx=item.element().index()
            found=self.find(idx)
            if found: 
                self.ui.main.tree.setCurrentIndex(found)

    def find(self, page): 

        return False
        # TODO
        # return super().find(page, self.outline)

    def open(self, how='reset', focus=True):

        self.display.viewChanged.disconnect(
                self.on_viewChanged)
        self.display.itemChanged.disconnect(
                self.on_viewItemChanged)
        index=self.ui.main.tree.currentIndex()
        if index:
            page=index.data(QtCore.Qt.UserRole+1)
            left=index.data(QtCore.Qt.UserRole+2)
            top=index.data(QtCore.Qt.UserRole+3)
            if how!='reset':
                model=self.display.view.model()
                self.display.open(model=model,
                             how=how,
                             focus=focus)
            self.display.currentView().goto(
                    page, left, top)
            super().open(how, focus)
        self.display.viewChanged.connect(self.on_viewChanged)
        self.display.itemChanged.connect(self.on_viewItemChanged)

    def getData(self, view):

        if view:
            m=view.model()
            mid=m.id()
            f=getattr(m, 'loadOutlines', None)
            if f and not mid in self.cache:
                self.cache[mid]=f()
            return self.cache.get(mid, None)
