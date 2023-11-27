from plug.qt import Plug
from gizmo.utils import tag

from .utils import Node

class Leaper(Plug):

    def setup(self):

        self.jumps={}
        super().setup()
        self.app.buffer.viewCreated.connect(
                self.setView)

    def setView(self, v):

        c=self.checkProp('canJump', v)
        if c:
            v.positionJumped.connect(
                    self.save)
            self.jumps[v]=Node()

    def save(self):

        v=self.app.handler.view()
        c=self.jumps.get(v)
        d=v.getLocator(kind='position')
        c.n=Node(p=c, d=d)
        self.jumps[v]=c.n

    @tag('[', modes=['normal'])
    def prev(self): 

        v=self.app.handler.view()
        c=self.jumps.get(v, None)
        v.positionJumped.disconnect(
                self.save)
        if c.p and c.p.d:
            self.jumps[v]=c.p
            v.openLocator(
                    data=c.p.d,
                    kind='position')
        v.positionJumped.connect(
                self.save)

    @tag(']', modes=['normal'])
    def next(self): 

        v=self.app.handler.view()
        c=self.jumps.get(v, None)
        v.positionJumped.disconnect(
                self.save)
        if c.n:
            self.jumps[v]=c.n
            v.openLocator(
                    data=c.n.d,
                    kind='position')
        v.positionJumped.connect(
                self.save)
