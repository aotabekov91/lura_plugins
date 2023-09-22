from PyQt5 import QtCore
from plug.qt import Plug
from plug.utils.register import register

class Search(Plug):

    special=['return', 'carriage']

    def __init__(self, 
            app, 
            *args,
            listen_leader='/',
            special=special,
            **kwargs):

        super(Search, self).__init__(
                *args,
                app=app, 
                special=special,
                listen_leader=listen_leader, 
                **kwargs,
                )

        self.index=-1
        self.match=None
        self.matches=[]
        self.setConnect()
        self.display=self.app.window.main.display

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

        self.clearItems()
        self.index=-1
        self.match=None
        self.matches=[]

    def clearItems(self):

        for m in self.matches:
            page, rect = m
            item=self.display.view.pageItem(page-1)
            item.setSearched()
        if self.matches:
            self.display.view.updateAll()

    def search(self, text, view, found=[]):

        if view:
            pages=view.model().pages()
            for p in pages.values():
                rects=p.search(text)
                pnum=p.pageNumber()
                if rects:
                    for r in rects:
                        found+=[(pnum, r)]
        return found

    def find(self, jump=True):

        self.clear()
        self.app.window.main.setFocus()
        text=self.app.window.bar.edit.text()

        if text:
            view=self.display.currentView()
            self.matches=self.search(
                    text, view)
            if self.matches and jump: 
                self.jump()

    def jump(self, increment=1, match=None):

        if self.matches:
            self.index+=increment
            self.setIndex()

    def setIndex(self):

        if self.matches:
            if self.index>=len(self.matches):
                self.index=0
            elif self.index<0:
                self.index=len(self.matches)-1
            p, r = self.matches[self.index]
            i=self.display.view.pageItem(p-1)
            m=i.mapToItem(r)
            i.setSearched([m])
            srec=i.mapRectToScene(m)
            self.display.view.goto(p)
            self.display.view.centerOn(
                    0, srec.y())

    def checkLeader(self, event, pressed):

        if super().checkLeader(event, pressed):
            if self.listening:
                return True
            current=self.app.plugman.current
            if current and current.name=='normal':
                return True
        return False
