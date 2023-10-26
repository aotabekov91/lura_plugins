from PyQt5 import QtCore 
from plug.qt import Plug
from gizmo.utils import register
from gizmo.widget import InputList, UpDown

class SearchList(Plug):

    def __init__(self,
                 app,
                 *args,
                 position='down',
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
        self.display=self.app.display
        self.app.moder.plugsLoaded.connect(
                self.on_plugsLoaded)
        self.setUI()

    def on_plugsLoaded(self, plugs):

        self.search=plugs.get('search', None)
        if self.search:
            ear=self.search.ear
            ear.returnPressed.connect(
                    self.activate)
            self.search.endedListening.connect(
                    self.deactivate)

    def activate(self):

        self.find()
        self.uiman.activate()

    def find(self):

        if self.search.matches:
            t=self.search.text
            v=self.display.currentView()
            dlist=[]
            for f in self.search.matches:
                pn, r = f
                e=v.model().element(pn)
                dlist+=[{
                    'up': self.getLine(t, e, r)
                    }]
            self.ui.main.setList(dlist)

    def setUI(self):

        self.uiman.setUI()
        w=InputList(widget=UpDown)
        w.input.hideLabel()
        self.ui.addWidget(
                w, 'main', main=True)
        
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
        return p.find(r)
        l=f'<html>{p.find(r)}</html>'
        r=f'<strong><u>{t}</u></strong>'
        return l.replace(t, r)
