from plug.qt import Plug 
from gizmo.utils import tag
from PyQt5.QtCore import pyqtSignal, Qt

class Bookmark(Plug):

    isMode=True
    special=['return']
    name='Bookmark'
    source='kind=table;'
    check_props=['canLocate']
    bookmarked=pyqtSignal()

    def event_functor(self, e, ear):

        m=[Qt.Key_Return, Qt.Key_Enter]
        if e.key() in m:
            self.saveBookmark()
            self.octivate()
            return True

    def octivateBar(self):

        self.app.ui.bar.bottom.hide()
        self.app.ui.bar.edit.clear()

    def activateBar(self):

        self.app.ui.bar.bottom.show()
        self.app.ui.bar.edit.setFocus()

    def activate(self):

        super().activate()
        self.activateBar()
        self.setBookmark()

    def octivate(self):

        super().octivate()
        self.octivateBar()

    def setBookmark(self):

        t, tm=self.getModel()
        if not tm: return 
        l=t.getLocator(kind='position')
        p=l['position']
        e=tm.findElement(p, by='position')
        if e:
            self.app.ui.bar.edit.setText(
                    e.data('text'))

    @tag('<c-b>', modes=['normal'])
    def bookmark(self):

        if self.checkType():
            self.activate()

    def saveBookmark(self):

        text=self.app.ui.bar.edit.text()
        t, tm = self.getModel()
        ul=t.getUniqLocator({'text': text})
        pl=t.getLocator(kind='position')
        ul.update(pl)
        tm.addElement(ul)
        self.bookmarked.emit()
        self.octivate()

    def getModel(self, t=None):

        t=t or self.app.handler.type()
        if not t: return
        if not t.model().isType: return
        return t, self.app.handler.getModel(
                name=self.name,
                source=self.source,
                index=t.getUniqLocator())

    def checkType(self):

        p=self.check_props
        t=self.app.handler.type()
        return self.checkProp(p, t)
