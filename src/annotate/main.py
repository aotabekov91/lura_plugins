from plug.qt import Plug
from functools import partial
from PyQt5 import QtGui, QtCore
from tables import Annotation as Table

class Annotate(Plug):

    view=None
    colors={}
    table=Table()
    func_colors={}
    kind='highlight'
    default_color='cyan'
    listen_leader='<c-a>'

    chosen=QtCore.pyqtSignal(object)
    removed=QtCore.pyqtSignal(object)
    annotated=QtCore.pyqtSignal(object)

    def setup(self):

        super().setup()
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
            i=sel['item']
            i.annotate(sel)
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
