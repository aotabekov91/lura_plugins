from plug.qt import Plug
from gizmo.utils import tag
from functools import partial
from tables import Annotation as Table
from PyQt5 import QtGui, QtCore, QtWidgets

from .widget import AList

class Annotate(Plug):

    colors={}
    isMode=True
    func_colors={}
    kind='highlight'
    default_color='cyan'
    listen_leader='<c-a>'
    position={'AList' : 'overlay'}

    def setupUI(self):

        self.ui=AList(
                parent=self.app.display)
        self.app.uiman.setupUI(
                self, self.ui, 'AList')
        m=QtGui.QStandardItemModel()
        for k, v in self.colors.items():
            t=f'{v["name"]} [{k}]'
            i=QtGui.QStandardItem(t)
            m.appendRow(i)
        self.ui.setModel(m)

    def event_functor(self, e, ear):

        t=e.text()
        f=self.actions.get(t, None)
        if f: f()

    def setColors(self):

        for k, v in self.colors.items():
            n, c=v['name'], v['color']
            f=partial(self.annotate, func=n)
            self.actions[k]=f
            self.func_colors[n]=QtGui.QColor(c)

    def setup(self):

        super().setup()
        self.setupUI()
        self.actions={}
        self.setColors()
        self.app.buffer.modelLoaded.connect(
                self.annotateModel)
        self.default_color=QtGui.QColor(
                self.default_color)

    def remove(self, e):

        d=e.data()
        v=self.app.handler.type()
        v.delLocator(data=d, kind='annotation')

    def getTable(self, o=None):

        n='Annotation'
        s='kind=table;'
        o=o or self.app.handler.type()
        u=o.getUniqLocator()
        return o, self.app.buffer.getModel((u,n,s))

    def annotateModel(self, m):

        if self.checkProp('canAnnotate', m):
            if self.checkProp('isAnnotated', m):
                return
            m, t = self.getTable(m)
            if not t: return
            t.elementRemoved.connect(self.remove)
            for e in t.elements().values():
                d=e.data()
                f=d.get('function', 'Default')
                d['color']=self.func_colors[f]
                m.setLocator(d, 'annotation')
                m.isAnnotated=True

    def annotate(self, func, s=None):

        v=self.app.handler.type()
        s = s or v.selection()
        if not s: self.octivate()
        s['function']=func
        s['akind']=self.kind
        c=self.func_colors.get(
                func, self.default_color)
        s['color']=c
        i=s['item']
        i.annotate(s)
        self.write(s)
        self.octivate()

    def write(self, s):

        v, t = self.getTable()
        l=v.getLocator(s, 'annotation')
        t.addElement(l)

    def checkLeader(self, e, p):

        v=self.app.handler.type()
        return self.checkProp('canAnnotate', v)
