from qapp.core.modes import Mode
from qapp.utils import register
from qapp.widget import ListWidget, Item

class Search(Mode):

    def __init__(self, app):

        super(Search, self).__init__(
                app=app, 
                listen_leader='/', 
                show_statusbar=True, 
                delisten_on_exec=False
                )

        self.index=-1
        self.matches=[]
        self.match=None

        self.setUI()

    def setUI(self):
        
        super().setUI()
        self.ui.addWidget(
                ListWidget(item_widget=Item, check_fields=['up']), 
                'main', 
                main=True)

        self.ui.installEventFilter(self)

    @register('l')
    def toggleList(self):

        if self.ui.isVisible():
            self.ui.deactivate()
        else:
            self.ui.activate()
            self.app.main.setFocus()

    @register('j')
    def next(self): self.jump(+1)

    @register('k')
    def prev(self): self.jump(-1)

    @register('f')
    def focusSearch(self): 

        self.listen_widget=[self.app.main.display]
        self.exclude_widget=[self.app.main.bar.edit]

        self.app.main.bar.edit.setFocus()

    def listen(self): 

        super().listen()

        self.listen_widget=[self.app.main.display]
        self.exclude_widget=[self.app.main.bar.edit]

        self.app.main.bar.edit.show()
        self.app.main.bar.edit.setFocus()
        self.app.main.bar.edit.returnPressed.connect(self.find)
        self.app.main.bar.hideWanted.connect(self.delistenWanted)

    def delisten(self, *args, **kwargs):

        if self.listening:

            self.clear()
            self.ui.deactivate()
            self.app.main.bar.hideWanted.disconnect()
            self.app.main.bar.edit.returnPressed.disconnect(self.find)
            self.app.main.display.cleanUp()

        super().delisten(*args, **kwargs)

    def clear(self):

        self.index=-1
        self.match=None
        self.matches=[]

    def find(self):

        self.listen_widget=[]
        self.exclude_widget=[]

        def search(text, view, found=[]):
            if view:
                document=view.model()
                for page in document.pages().values():
                    rects=page.search(text)
                    if rects:
                        for rect in rects:
                            line=self.getLine(text, page, rect)
                            found+=[{'page': page.pageNumber(), 'rect': rect, 'up': line}]
            return found

        text=self.app.main.bar.edit.text()

        self.clear()
        self.app.main.setFocus()

        if text:
            self.matches=search(text, self.app.main.display.view)
            if len(self.matches) > 0: 
                self.ui.main.setList(self.matches)
                self.jump()
            else:
                self.ui.main.setList([{'up': f'No match found for {text}'}])

    def jump(self, increment=1, match=None):

        if len(self.matches)==0: return

        if not match:

            self.index+=increment
            if self.index>=len(self.matches):
                self.index=0
            elif self.index<0:
                self.index=len(self.matches)-1

            match=self.matches[self.index]
            self.ui.main.setCurrentRow(self.index)
        
        page=match['page']
        rect=match['rect']

        pageItem=self.app.main.display.view.pageItem(page-1)
        matchMapped=pageItem.mapToItem(rect)
        pageItem.setSearched([matchMapped])
        sceneRect=pageItem.mapRectToScene(matchMapped)

        self.app.main.display.view.goto(page)
        self.app.main.display.view.centerOn(0, sceneRect.y())

    def getLine(self, text, page, rectF):

        width=page.size().width()
        lineRectF=QRectF(0, rectF.y(), width, rectF.height())
        line=f'<html>{page.find(lineRectF)}</html>'
        replacement=f'<font color="red">{text}</font>'
        return line.replace(text, replacement)

    def checkListen(self, event): 
        if super().checkListen(event):
            return self.app.modes.normal.listening
