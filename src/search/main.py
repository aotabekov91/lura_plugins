from PyQt5 import QtCore
from plug.qt import Plug
from gizmo.utils import register

class Search(Plug):

    special=['return', 'carriage']

    def __init__(self, 
            *args,
            special=special,
            listen_leader='/',
            **kwargs):

        super().__init__(
                *args,
                special=special,
                listen_leader=listen_leader, 
                **kwargs,
                )

        self.index=-1
        self.view=None
        self.text=None
        self.match=None
        self.matches=[]
        self.setConnect()

    def setConnect(self):

        self.bar=self.app.window.bar
        self.ear.returnPressed.connect(
                self.startSearch)
        self.ear.carriageReturnPressed.connect(
                self.startSearch)

    @register('<c-f>')
    def toggleFocus(self): 

        if self.bar.edit.hasFocus():
            self.app.window.setFocus()
        else:
            self.bar.edit.setFocus()

    def listen(self): 

        super().listen()
        self.connectView()
        self.activateBar()

    def delisten(self):

        self.disconnectView()
        super().delisten()
        self.clear()
        self.deactivateBar()

    def clear(self):

        self.erase()
        self.index=-1
        self.text=None
        self.match=None
        self.matches=[]

    def erase(self):

        for m in self.matches:
            page, rect = m
            item=self.display.view.item(page)
            item.setSearched()
        if self.matches:
            self.display.view.updateAll()

    # def search(self, text, view, found=[]):

    #     if view:
    #         elems=view.model().elements()
    #         for p in elems.values():
    #             rects=p.search(text)
    #             pnum=p.index()
    #             if rects:
    #                 for r in rects:
    #                     found+=[(pnum, r)]
    #     return found

    def startSearch(self):

        self.clear()
        self.toggleFocus()
        t=self.bar.edit.text()
        if t: self.view.search(t)

    @register('j')
    def next(self, digit=1): 
        self.jump(digit)

    @register('k')
    def prev(self, digit=1): 
        self.jump(-digit)

    def jump(self, digit=1):

        if self.matches:
            self.index+=digit
            if self.index>=len(self.matches):
                self.index=0
            elif self.index<0:
                self.index=len(self.matches)-1
            i, r = self.matches[self.index]
            d, x, y = i.index(), r.x(), r.y()
            s=i.mapRectToScene(r)
            self.view.goto(d)
            self.view.centerOn(s.x(), s.y())

    def checkLeader(self, event, pressed):

        if super().checkLeader(event, pressed):
            if self.ear.listening:
                return True
            c=self.app.moder.current
            if c and c.name=='normal':
                v=c.getView()
                if hasattr(v, 'canSearch'):
                    self.view=v
                    return True
        return False

    def on_searchFound(self, data):

        initial=False
        if not self.matches and data:
            initial=True
        self.matches+=data
        if initial: self.jump()

    def connectView(self):

        self.view.searchFound.connect(
                self.on_searchFound)

    def disconnectView(self):

        self.view.searchFound.disconnect(
                self.on_searchFound)

    def activateBar(self):

        self.bar.bottom.show()
        self.bar.mode.setText('/')
        self.bar.edit.show()
        self.bar.edit.setFocus()

    def deactivateBar(self):

        self.bar.bottom.hide()
        self.bar.edit.clear()
        self.bar.mode.clear()
