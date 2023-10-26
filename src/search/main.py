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
        self.text=None
        self.match=None
        self.matches=[]
        self.setConnect()
        self.display=self.app.display

    def setConnect(self):

        listener=self.ear
        listener.returnPressed.connect(
                lambda: self.find(jump=True))
        listener.carriageReturnPressed.connect(
                lambda: self.find(jump=True))

    @register('j')
    def next(self, digit=1): 
        self.jump(digit)

    @register('k')
    def prev(self, digit=1): 
        self.jump(-digit)

    @register('<c-f>')
    def toggleFocus(self): 
        self.app.window.bar.edit.setFocus()

    def listen(self): 

        super().listen()
        bar=self.app.window.bar
        bar.bottom.show()
        bar.mode.setText('/')
        bar.edit.show()
        bar.edit.setFocus()

    def delisten(self):

        super().delisten()
        self.clear()
        bar=self.app.window.bar
        bar.bottom.hide()
        bar.edit.clear()
        bar.mode.clear()

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

    def search(self, text, view, found=[]):

        if view:
            elems=view.model().elements()
            for p in elems.values():
                rects=p.search(text)
                pnum=p.index()
                if rects:
                    for r in rects:
                        found+=[(pnum, r)]
        return found

    def find(self, jump=True):

        self.clear()
        self.app.window.main.setFocus()
        text=self.app.window.bar.edit.text()
        if text:
            self.text=text
            view=self.display.currentView()
            self.matches=self.search(
                    text, view)
            if self.matches and jump: 
                self.jump()

    def jump(self, digit=1, match=None):

        if self.matches:
            self.index+=digit
            if self.index>=len(self.matches):
                self.index=0
            elif self.index<0:
                self.index=len(self.matches)-1
            self.jumpToIndex()

    def jumpToIndex(self):

        if self.matches:
            p, r = self.matches[self.index]
            i=self.display.view.item(p)
            m=i.mapToItem(r)
            i.setSearched([m])
            srec=i.mapRectToScene(m)
            self.display.view.goto(p)
            self.display.view.centerOn(
                    0, srec.y())

    def checkLeader(self, event, pressed):

        if super().checkLeader(event, pressed):
            if self.ear.listening:
                return True
            current=self.app.moder.current
            if current and current.name=='normal':
                return True
        return False
