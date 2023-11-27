from PyQt5.QtCore import QSize
from gizmo.widget import ListView

class AList(ListView):

    def setModel(self, model):
        
        self.m_model=model
        super().setModel(model)

    def sizeHint(self):

        w=self.width()
        n=self.m_model.rowCount()
        if n==0: return QSize(w, 0)
        c=0
        h=self.sizeHintForRow(0)
        for i in range(n):
            ih=self.sizeHintForColumn(i)
            c=max(c, ih)
        c+=10
        r = self.parent().rect()
        dy=self.rect().y()
        w= min(int(0.8*r.width()-dy), c)
        h = min(int(0.9*r.height()), h*n)
        return QSize(w, h) 

    def updatePosition(self):

        p = self.parent().rect()
        if not p: return
        self.adjustSize()
        w, h=self.width(), self.height()
        y=int(p.height()/2-self.height()/2)
        self.setGeometry(0, y, w, h)
