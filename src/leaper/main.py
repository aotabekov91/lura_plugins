from plug.qt import Plug
from gizmo.utils import tag

class Leaper(Plug):

    def setup(self):

        self.jumps={}
        self.indices={}
        super().setup()
        self.app.handler.viewChanged.connect(
                self.resetView)

    def setDisconnect(self):

        self.display.itemChanged.disconnect(
                self.on_itemChanged)

    def resetView(self, v):

        c1=self.checkProp('canMove', v)
        c2=self.checkProp('positionChanged', v)
        if c1 and c2:
            self.reconnect('disconnect')
            self.view=v
            self.reconnect()

    def reconnect(self, kind='connect'):

        v = self.view
        if not v: return
        f=getattr(v.positionChanged, kind)
        f(self.saveState)

    def saveState(self):

        v=self.view
        if not v in self.jumps:
            self.jumps[v]={}
            self.indices[v]=0

        jumps=self.jumps.get(v)
        index=self.indices.get(v)
        idx=v.item().index()
        data=(idx, view.getPosition())

        idx_data=jumps.get(index, None)
        if idx_data and idx_data!=data:
            s=len(jumps)-1
            for i in range(s, index, -1):
                jumps.pop(i)

        jumps[index]=data
        self.indices[view]=index+1

    @tag('[', modes=['normal'])
    def jump_prev(self): 
        self.jump(delta=-1)

    @tag(']', modes=['normal'])
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
