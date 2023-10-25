from plug.qt import Plug
from gizmo.utils import register
from tables import Quickmark as Table

class Quickmark(Plug):

    def __init__(
            self,
            app,
            *args,
            listen_leader=['m', 't'],
            **kwargs,
            ):

        self.kind=None
        self.pressed=None
        self.table = Table() 
        super(Quickmark, self).__init__(
                *args,
                app=app,
                listen_leader=listen_leader,
                **kwargs,
                )

    def setup(self):

        super().setup()
        self.keys=self.ear.listen_leader
        self.ear.keyRegistered.connect(
                self.on_keyRegistered)

    def listen(self):
        
        super().listen()
        if self.pressed==self.keys[0]:
            self.kind='marker'
        else:
            self.kind='jumper'

    def mark(self, mark):

        if mark: 
            view = self.app.display.currentView()
            dhash= view.model().id()
            page = view.currentPage()
            left, top = view.getPosition()
            position=f'{page}:{left}:{top}'
            data={'hash':dhash, 
                  'position': position, 
                  'mark':mark}
            self.table.writeRow(data)
        self.delistenWanted.emit()

    def jump(self, mark):

        if mark:
            rows=self.table.getRow(
                    {'mark':mark})
            if rows:
                mark=rows[0]
                d = mark['position'].split(':')
                p, l, t = tuple(d)
                p, l, t = int(p), float(l), float(t)
                self.app.display.currentView().goto(
                        p, l, t)
        self.delistenWanted.emit()

    def on_keyRegistered(self, event):

        if self.kind=='jumper':
            self.jump(event.text())
        elif self.kind=='marker':
            self.mark(event.text())

    def checkLeader(self, event, pressed):

        if super().checkLeader(event, pressed):
            current=self.app.moder.current
            if current and current.name=='normal':
                self.pressed=pressed
                return True
        return False
