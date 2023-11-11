from plug.qt import Plug
from functools import partial
from PyQt5 import QtGui, QtCore
from gizmo.utils import register
from tables import Annotation as Table

from fitz import Quad, Point

class Annotate(Plug):

    chosen=QtCore.pyqtSignal(object)
    removed=QtCore.pyqtSignal(object)
    annotated=QtCore.pyqtSignal(object)

    def __init__(
            self, 
            listen_leader='<c-a>', 
            **kwargs
            ):

        self.view=None
        self.colors={}
        self.table=Table()
        self.func_colors={}
        self.kind='highlight'
        self.default_color='cyan'
        super().__init__(
                listen_leader=listen_leader,
                **kwargs,
                )
        self.setColors()

    def setColors(self):

        c=self.colors
        for k, v in c.items():
            n, c=v['name'], v['color']
            f=partial(self.annotate, func=n)
            f.key, f.modes=f'{k}', []
            self.func_colors[n]=QtGui.QColor(c)
            self.actions[(self.name, n)]=f
        self.app.moder.save(
                self, self.actions)
        self.default_color=QtGui.QColor(
                self.default_color)

    def getColor(self, func):

        return self.func_colors.get(
                func, self.default_color)

    def annotate(self, func, sel=None):

        if not sel:
            sel=self.view.selection()
        if sel:
            sel['function']=func
            sel['akind']=self.kind
            sel['color']=self.getColor(func)
            item=sel['item']
            item.annotate(sel)
            self.write(sel)
            self.annotated.emit(sel)
        self.delistenWanted.emit()

    def write(self, sel):

        loc=self.view.getLocator(
                data=sel, kind='annotation')
        self.table.writeRow(loc)

    def checkLeader(self, event, pressed):

        if super().checkLeader(event, pressed):
            if self.ear.listening: 
                return True
            c=self.app.moder.current
            if c and hasattr(c, 'getView'):
                v=c.getView()
                if v.check('canAnnotate'):
                    self.view=v
                    return True
        return False
