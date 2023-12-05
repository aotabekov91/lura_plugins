from plug.qt import Plug
from gizmo.utils import tag

from .utils import Node

class Leaper(Plug):

    def setup(self):

        super().setup()
        self.m_jumps={}
        self.app.handler.viewCreated.connect(
                self.setView)

    def setView(self, v):

        x=['canJump', 'canLocate']
        c=self.checkProp(x, v)
        if not c: return
        self.m_jumps[v]=Node()
        v.positionJumped.connect(
                self.save)

    def save(self):

        v=self.app.handler.view()
        c=self.m_jumps.get(v)
        x=['canJump', 'canLocate']
        if self.checkProp(x, v):
            d=v.getLocator(kind='position')
            c.n=Node(p=c, d=d)
            self.m_jumps[v]=c.n

    @tag('[', modes=['normal'])
    def prev(self): 

        v=self.app.handler.view()
        c=self.m_jumps.get(v, None)
        c1=v.check(['canJump', 'canLocate'])
        if not (c or c1): return
        v.positionJumped.disconnect(
                self.save)
        if c.p and c.p.d:
            self.m_jumps[v]=c.p
            v.openLocator(
                    data=c.p.d,
                    kind='position')
        v.positionJumped.connect(
                self.save)

    @tag(']', modes=['normal'])
    def next(self): 

        v=self.app.handler.view()
        c=self.m_jumps.get(v, None)
        c1=v.check(['canJump', 'canLocate'])
        if not (c or c1): return
        v.positionJumped.disconnect(
                self.save)
        if c.n:
            self.m_jumps[v]=c.n
            v.openLocator(
                    data=c.n.d,
                    kind='position')
        v.positionJumped.connect(
                self.save)
