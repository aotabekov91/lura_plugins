from PyQt5 import QtCore 

from plug.qt import Plug
from plug.utils.register import register
from gizmo.widget import ListWidget, Item

class SearchList(Plug):

    def __init__(self,
                 app,
                 *args,
                 position='bottom',
                 **kwargs):

        self.follow_move=False 

        super().__init__(
                *args,
                app=app,
                position=position,
                **kwargs
                )

    def setup(self):

        super().setup()
        self.display=self.app.window.main.display
        self.app.plugman.plugsLoaded.connect(
                self.on_plugsLoaded)
        self.setUI()

    def on_plugsLoaded(self, plugs):

        self.search=plugs.get('Search', None)
        if self.search:
            ear=self.search.ear
            ear.returnPressed.connect(
                    self.find)
            self.search.endedListening.connect(
                    self.deactivate)

    def find(self):

        if self.search.matches:
            dlist=[]
            v=self.display.currentView()
            t=self.app.window.bar.edit.text()
            for f in self.search.matches:
                pn, r = f
                p=v.model().page(pn)
                dlist+=[{'up': self.getLine(t, p, r)}]
            self.ui.main.setList(dlist)
            self.ui.main.adjustSize()
            self.activateUI()

    def setUI(self):

        wlist=ListWidget(
                item_widget=Item,
                objectName='List'
                )
        super().setUI()
        self.ui.addWidget(
                wlist, 'main', main=True)
        
    @register('<c-j>', modes=['Search'])
    def next(self): 
        self.ui.main.moveDown()

    @register('<c-k>', modes=['Search'])
    def prev(self): 
        self.ui.main.moveUp()

    @register('<c-l>', modes=['Search'])
    def jump(self, increment=1):
        crow=self.ui.main.currentRow()
        self.search.index=crow
        self.search.setIndex()

    def getLine(self, t, p, r):

        w=p.size().width()
        x, y, w, h = 0, r.y(), w, r.height()
        r=QtCore.QRectF(x, y, w, h)
        l=f'<html>{p.find(r)}</html>'
        r=f'<strong><u>{t}</u></strong>'
        return l.replace(t, r)
