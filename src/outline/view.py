from gizmo.utils import tag
from gizmo.vimo.view import TreeView

class OutlineView(TreeView):

    @tag('t', modes=['command'])
    def toggle(self):
        super().toggle()

    @tag('o', modes=['normal|^own'])
    def open(self, *args, **kwargs):

        i=self.currentItem()
        if i:
            p=i.data()
            t=self.app.handler.type()
            t.openLocator(p, 'position')

    def updateTree(self, v, idx):

        i=self.view.item(idx)
        idx=self.view.findInOutline(i)
        self.tree.setCurrentIndex(idx)

    def findInOutline(self, item):

        if item:
            m=self.m_outline
            idx=item.element().index()
            goto=0
            for r in range(m.rowCount()):
                if idx<m.item(r).data():
                    return m.index(goto, 0)
                goto=r
