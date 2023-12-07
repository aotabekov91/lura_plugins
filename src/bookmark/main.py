from plug.qt import Plug 
from gizmo.utils import tag
from PyQt5.QtCore import pyqtSignal, Qt

class Bookmark(Plug):

    isMode=True
    name='Bookmark'
    source='kind=table;'
    props=['canLocate']
    bookmarked=pyqtSignal()

    def activate(self):

        super().activate()
        self.app.ui.bar.bottom.show()
        self.app.ui.bar.edit.setFocus()
        self.setBookmark()

    def octivate(self):

        super().octivate()
        self.app.ui.bar.bottom.hide()
        self.app.ui.bar.edit.clear()

    def setBookmark(self):

        t, tm=self.getModel()
        if not tm: return 
        l=t.getLocator(kind='position')
        e=tm.findElement(l['position'], by='position')
        if not e: return
        self.app.ui.bar.edit.setText(e.data('text'))

    @tag('<c-b>', modes=['normal'])
    def bookmark(self):

        t=self.app.handler.type()
        if self.checkProp(self.props, t):
            self.activate()

    @tag(['<enter>', '<return>'])
    def saveBookmark(self):

        text=self.app.ui.bar.edit.text()
        t, tm = self.getModel()
        ul=t.getUniqLocator({'text': text})
        pl=t.getLocator(kind='position')
        ul.update(pl)
        tm.addElement(ul)
        self.bookmarked.emit()
        self.octivate()

    def getModel(self):

        t=self.app.handler.type()
        if not t: return
        if not t.model().isType: return
        return t, self.app.handler.getModel(
                name=self.name,
                source=self.source,
                index=t.getUniqLocator())
