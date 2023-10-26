from plug.qt import Plug
from gizmo.utils import register

class Leaper(Plug):

    def setup(self):

        super().setup()
        self.jumps={}
        self.indices={}
        self.setConnect()

    def setConnect(self):

        self.display=self.app.display
        self.display.itemChanged.connect(
                self.on_itemChanged)

    def setDisconnect(self):

        self.display.itemChanged.disconnect(
                self.on_itemChanged)

    def on_itemChanged(self, view, item):

        if not view in self.jumps:
            self.jumps[view]={}
            self.indices[view]=0

        jumps=self.jumps.get(view)
        index=self.indices.get(view)
        idx=view.item().index()
        data=(idx, view.getPosition())

        idx_data=jumps.get(index, None)
        if idx_data and idx_data!=data:
            s=len(jumps)-1
            for i in range(s, index, -1):
                jumps.pop(i)

        jumps[index]=data
        self.indices[view]=index+1

    @register('[', modes=['normal'])
    def jump_prev(self): 
        self.jump(delta=-1)

    @register(']', modes=['normal'])
    def jump_next(self): 
        self.jump(delta=1)

    def jump(self, delta=1):

        view=self.display.currentView()
        jumps=self.jumps.get(view, None)
        if jumps:
            current=self.indices.get(view)
            if current>len(jumps)-1:
                current-=1
            current+=delta
            data=jumps.get(current)
            if data:
                page, (top, left)= data 
                self.indices[view]=current

                self.setDisconnect()
                view.goto(page, left, top) 
                self.setConnect()
