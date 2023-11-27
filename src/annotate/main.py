from plug.qt import Plug
from functools import partial
from PyQt5 import QtGui, QtCore
from tables import Annotation as Table

class Annotate(Plug):

    colors={}
    isMode=True
    func_colors={}
    kind='highlight'
    default_color='cyan'
    listen_leader='<c-a>'

    def setup(self):

        super().setup()
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
            m, t = self.getTable(m)
            if not t: return
            t.elementRemoved.connect(self.remove)
            for e in t.elements().values():
                d=e.data()
                f=d.get('function', 'Default')
                d['color']=self.func_colors[f]
                m.setLocator(d, 'annotation')

    def setColors(self):

        for k, v in self.colors.items():
            n, c=v['name'], v['color']
            f=partial(self.annotate, func=n)
            f.key, f.modes=f'{k}', []
            self.func_colors[n]=QtGui.QColor(c)
            setattr(self, f'annotateIn{n}', f)

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
