from gizmo.vimo.model import STableModel
from gizmo.vimo.item.mixin import StandardItem

class QuickmarkModel(STableModel):

    def addItem(self, e):

        d=e.data()
        m=d['mark']
        i=StandardItem(m)
        i.setElement(e)
        self.appendRow(i)
