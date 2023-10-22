from PyQt5 import QtWidgets, QtCore, QtGui

class ListWidget(QtWidgets.QWidget):

    def __init__(
            self, *args, **kwargs):

        super().__init__(
                *args, **kwargs)
        self.setup()

    def setup(self):

        self.list=QtWidgets.QListView(
                parent=self, objectName='List')
        self.list.setVerticalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)
        self.list.setHorizontalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)
        self.m_layout=QtWidgets.QVBoxLayout(self)
        self.m_layout.setContentsMargins(0,0,0,0)
        self.m_layout.addWidget(self.list)
        self.setLayout(self.m_layout)
        self.model=QtGui.QStandardItemModel()
        self.proxy=QtCore.QSortFilterProxyModel()
        self.proxy.setSourceModel(self.model)
        self.list.setModel(self.proxy)

    def show(self):

        super().show()
        self.list.show()
        self.updatePosition()

    def sizeHint(self):

        w=self.list.width()
        if self.proxy.rowCount()==0:
            return QtCore.QSize(w, 0)
        n=self.proxy.rowCount()
        h=self.list.sizeHintForRow(0)#*n

        c=0
        for i in range(self.proxy.rowCount()):
            c=max(c, self.list.sizeHintForColumn(i))
        c+=5

        r = self.parent().rect()

        dy=self.rect().y()
        w= min(int(0.8*r.width()-dy), c)
        h = min(int(0.9*r.height()), h*n)
        return QtCore.QSize(w, h) 

    def updatePosition(self):

        x=0
        p = self.parent().rect()
        if p:
            self.adjustSize()
            w=self.width()
            h=self.height()
            y=int(p.height()/2-self.height()/2)
            self.setGeometry(x, y, w, h)
            self.list.setStyleSheet('background-color: yellow;')
