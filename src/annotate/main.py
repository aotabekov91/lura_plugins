from plug.qt import Plug
from functools import partial
from PyQt5 import QtGui, QtCore
from tables import Annotation as Table

class Annotate(Plug):

    colors={}
    fcolors={}
    isMode=True
    dcolor='cyan'
    kind='highlight'
    listen_leader='<c-a>'

    chosen=QtCore.pyqtSignal(object)
    removed=QtCore.pyqtSignal(object)
    annotated=QtCore.pyqtSignal(object)

    def setup(self):

        super().setup()
        self.setColors()
        self.app.buffer.modelLoaded.connect(
                self.annotateModel)
        self.dcolor=QtGui.QColor(self.dcolor)

    def annotateModel(self, m):

        if self.checkProp('canAnnotate', m):
            l=m.getUniqLocator(kind='annotation')
            # rs=self.table.getRow(l)
            # for r in rs: 
            #     self.updateAnnData(r, model=m)
            #     m.setLocator(r, 'annotation')

    def setColors(self):

        for k, v in self.colors.items():
            n, c=v['name'], v['color']
            f=partial(self.annotate, func=n)
            f.key, f.modes=f'{k}', []
            self.fcolors[n]=QtGui.QColor(c)
            setattr(self, f'annotateIn{n}', f)
            # self.actions[(self.name, n)]=f
        # self.app.moder.save(self, self.actions)

    def annotate(self, func, sel=None):

        v=self.app.handler.type()
        sel = sel or v.selection()
        if sel:
            sel['function']=func
            sel['akind']=self.kind
            c=self.fcolors.get(
                    func, self.dcolor)
            sel['color']=c
            i=sel['item']
            i.annotate(sel)
            self.write(sel)
            self.annotated.emit(sel)
        self.delistenWanted.emit()

    def write(self, sel):

        v=self.app.handler.type()
        l=v.getLocator(
                data=sel, kind='annotation')
        self.table.writeRow(l)

    def checkLeader(self, e, p):

        t=self.app.handler.type()
        return self.checkProp('canAnnotate', t)
