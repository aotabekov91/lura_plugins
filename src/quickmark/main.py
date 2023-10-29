from PyQt5 import QtCore
from plug.qt import Plug
from gizmo.utils import register
from tables import Quickmark as Table

class Quickmark(Plug):

    jumped=QtCore.pyqtSignal()
    marked=QtCore.pyqtSignal()
    unmarked=QtCore.pyqtSignal()

    def __init__(
            self,
            app,
            *args,
            listen_leader='<c-m>',
            **kwargs,
            ):

        self.mode=None
        self.actor=None
        self.table = Table() 
        super().__init__(
                *args,
                app=app,
                listen_leader=listen_leader,
                **kwargs,
                )

    def setup(self):

        super().setup()
        self.ear.suffix_functor=self.set

    def set(self, event):

        key=event.text()
        if key and self.actor: 
            self.actor(key)
            return True
        return False

    def listen(self):

        self.actor=None
        super().listen()

    @register('m')
    def mark(self):
        self.actor=self._mark

    @register('u')
    def unmark(self):
        self.actor=self._unmark

    @register('U')
    def unmarkGlobal(self):

        f=lambda x: self._unmark(x, True)
        self.actor=f

    @register('g')
    def goto(self):
        self.actor=self._goto

    @register('G')
    def gotoGlobal(self):

        f=lambda x: self._goto(x, True)
        self.actor=f

    def _unmark(self, m, globally=False):

        if m: 
            v = self.mode.getView()
            cond={'mark': m}
            if not globally:
                cond['kind']=v.kind()
                cond['page']=v.itemId()
                cond['hash']=v.modelId(),
            self.table.removeRow(cond)
        self.unmarked.emit()
        self.modeWanted.emit(self.mode)

    def _mark(self, m):

        if m: 
            v = self.mode.getView()
            data={
                  'mark':m,
                  'kind': v.kind(),
                  'page': v.itemId(),
                  'hash': v.modelId(), 
                  'position': v.getLocation(),
                  }
            self.table.writeRow(data)
        self.marked.emit()
        self.modeWanted.emit(self.mode)

    def _goto(self, m, globally=False):

        if m:
            v=self.mode.getView()
            cond={
                  'mark': m,
                  'hash': v.modelId()
                 }
            if not globally:
                cond['kind']=v.kind()
            rs=self.table.getRow(cond)
            if rs: v.open(**rs[0])
        self.jumped.emit()
        self.modeWanted.emit(self.mode)

    def checkLeader(self, event, pressed):

        if super().checkLeader(event, pressed):
            if self.ear.listening:
                return True
            m=self.app.moder.current
            if getattr(m, 'getView', False): 
                self.mode=m
                return True
        return False
