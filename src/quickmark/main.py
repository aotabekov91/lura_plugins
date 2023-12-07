from PyQt5 import QtCore
from plug.qt import Plug
from gizmo.utils import tag

class Quickmark(Plug):

    isMode=True
    functor=None
    name='Quickmark'
    source='kind=table;'
    model_name='Quickmark'
    check_props=['canLocate']
    jumped=QtCore.pyqtSignal()
    marked=QtCore.pyqtSignal()
    unmarked=QtCore.pyqtSignal()

    def event_functor(self, e, ear):

        if e.text() and self.functor: 
            self.functor(e.text())
            self.octivate()
            return True

    def activate(self, functor):

        self.functor=functor
        super().activate()

    def octivate(self):

        self.functor=None
        super().octivate()

    @tag('m', modes=['normal'])
    def setMark(self):

        if self.checkType():
            self.activate(self.mark)

    @tag('M', modes=['normal'])
    def gotoMark(self):

        if self.checkType():
            self.activate(self.goTo)

    def mark(self, m):

        t, tm=self.getModel()
        print(t, tm)
        if tm:
            ul=t.getUniqLocator()
            pl=t.getLocator(kind='position')
            ul.update(pl)
            ul['mark']=m
            tm.addElement(ul)
            self.marked.emit()

    def goTo(self, m):

        t, tm=self.getModel()
        if not tm: return
        e=tm.findElement(m, by='mark')
        if not e: return
        d=e.data()
        t.openLocator(d, kind='position')
        self.jumped.emit()

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
