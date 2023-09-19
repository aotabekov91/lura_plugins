from PyQt5 import QtCore
from plug.qt import Plug
from plug.qt.utils import register

class Search(Plug):

    special=['return', 'carriage']

    def __init__(self, 
            app, 
            *args,
            listen_leader='/',
            special=special,
            **kwargs):

        self.box_color='green'
        self.text_color='yellow'

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

    def setup(self):

        super().setup()
        self.display=self.app.window.main.display
        self.setConnect()

    def setConnect(self):

        self.event_listener.returnPressed.connect(
                self.find)
        self.event_listener.carriageReturnPressed.connect(
                self.find)

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
        self.clearItems()
        self.clear()
        bar=self.app.window.bar
        bar.bottom.hide()
        bar.edit.clear()
        bar.mode.clear()

    def clear(self):

        self.index=-1
        self.match=None
        self.matches=[]

    def clearItems(self):

        for m in self.matches:
            page, rect = m['page'], m['rect']
            item=self.display.view.pageItem(page-1)
            item.setSearched()
        self.display.view.updateAll()

    def find(self):

        self.listen_widget=[]
        self.exclude_widget=[]

        def search(text, view, found=[]):

            if not view: return found
            document=view.model()
            for page in document.pages().values():
                rects=page.search(text)
                if not rects: continue
                for rect in rects:
                    line=self.getLine(text, page, rect)
                    data={'page': page.pageNumber(), 
                          'rect': rect, 
                          'up': line}
                    found+=[data]
            return found

        self.clear()
        self.app.window.main.setFocus()
        text=self.app.window.bar.edit.text()

        if text:
            view=self.display.currentView()
            self.matches=search(text, view)
            if len(self.matches) > 0: 
                self.jump()

    def jump(self, increment=1, m=None):

        if len(self.matches)==0: 
            return
        if not m:
            self.index+=increment
            if self.index>=len(self.matches):
                self.index=0
            elif self.index<0:
                self.index=len(self.matches)-1
            m=self.matches[self.index]
        page, rect = m['page'], m['rect']
        item=self.display.view.pageItem(page-1)
        mapped=item.mapToItem(rect)
        item.setSearched([mapped])
        sceneRect=item.mapRectToScene(mapped)
        self.display.view.goto(page)
        self.display.view.centerOn(0, sceneRect.y())

    def getLine(self, text, page, rectF):

        width=page.size().width()
        lineRectF=QtCore.QRectF(0, rectF.y(), width, rectF.height())
        line=f'<html>{page.find(lineRectF)}</html>'
        replacement=f'<font color="{self.text_color}">{text}</font>'
        return line.replace(text, replacement)

    def checkLeader(self, event, pressed):

        if super().checkLeader(event, pressed):
            if self.listening:
                return True
            current=self.app.plugman.current
            if current and current.name=='normal':
                return True
        return False
