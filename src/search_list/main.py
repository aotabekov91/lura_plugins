from PyQt5 import QtCore 

from plug.qt import Plug
from gizmo.widget import ListWidget, Item

class SearchList(Plug):

    def setup(self):

        self.text_color='green'
        super().setup()
        self.display=self.app.window.main.display
        self.app.plugman.plugsLoaded.connect(
                self.on_plugsLoaded)
        self.setUI()

    def on_plugsLoaded(self, plugs):

        self.search=plugs.get('Search', None)
        if self.search:
            ear=self.search.event_listener
            ear.returnPressed.connect(self.find)

    def find(self):

        if self.search.matches:
            dlist=[]
            v=self.display.currentView()
            t=self.app.window.bar.edit.text()
            for f in self.search.matches:
                pn, r = f
                p=v.model().page(pn)
                dlist+=[{'up': self.getLine(t, p, r)}]
            self.ui.setList(dlist)
            self.updateUIPosition()
            self.ui.show()

    def updateUIPosition(self):

        p = self.ui.parent().rect()
        if p:
            self.ui.adjustSize()
            hint=self.ui.sizeHint()
            # w=self.ui.width()
            # h=self.ui.height()
            w=hint.width()
            h=hint.height()
            y=int(p.height()/2-h/2)
            print(0,y,w,h)
            self.ui.setGeometry(0, y, w, h)

    def setUI(self):

        wlist=ListWidget(
                item_widget=Item,
                parent=self.app.window)
        super().setUI(ui=wlist)
        self.ui.hide()
        
    def getLine(self, t, p, r):

        c=self.text_color
        w=p.size().width()
        x, y, w, h = 0, r.y(), w, r.height()
        r=QtCore.QRectF(x, y, w, h)
        line=f'<html>{p.find(r)}</html>'
        rep=f'<font color="{c}">{t}</font>'
        return line.replace(t, rep)
