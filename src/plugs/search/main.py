from PyQt5 import QtCore
from plug.qt import PlugObj
from plug.qt.utils import register
from gizmo.widget import ListWidget, Item

class Search(PlugObj):

    def __init__(self, app, **kwargs):

        super(Search, self).__init__(
                app=app, 
                position='bottom',
                listen_leader='/', 
                show_statusbar=True, 
                delisten_on_exec=False,
                **kwargs,
                )
        self.index=-1
        self.match=None
        self.matches=[]
        self.setUI()

    def setUI(self):
        
        super().setUI()
        l=ListWidget(item_widget=Item, 
                     set_base_style=False,
                     check_fields=['up'])
        self.ui.addWidget(l, 'main', main=True)

    @register('<c-l>')
    def toggleList(self):

        if self.ui.isVisible():
            self.deactivateUI()
        else:
            self.activateUI()

    @register('<c-j>')
    def next(self, digit=1): 

        self.jump(digit)

    @register('<c-k>')
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
        bar.edit.returnPressed.connect(self.find)
        bar.hideWanted.connect(self.delistenWanted)

    def delisten(self):

        super().delisten()
        self.clear()
        self.deactivateUI()
        bar=self.app.window.bar
        bar.hideWanted.disconnect()
        bar.edit.returnPressed.disconnect(self.find)
        self.app.window.main.display.cleanUp()
        bar.bottom.hide()
        bar.mode.setText(':')
        bar.edit.setText('')

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

        text=self.app.window.bar.edit.text()
        self.clear()
        self.app.window.main.setFocus()

        if text:
            self.matches=search(text, self.app.window.main.display.view)
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

        pageItem=self.app.window.main.display.view.pageItem(page-1)
        matchMapped=pageItem.mapToItem(rect)
        pageItem.setSearched([matchMapped])
        sceneRect=pageItem.mapRectToScene(matchMapped)

        self.app.window.main.display.view.goto(page)
        self.app.window.main.display.view.centerOn(0, sceneRect.y())

    def getLine(self, text, page, rectF):

        width=page.size().width()
        lineRectF=QtCore.QRectF(0, rectF.y(), width, rectF.height())
        line=f'<html>{page.find(lineRectF)}</html>'
        replacement=f'<font color="red">{text}</font>'
        return line.replace(text, replacement)

    def checkLeader(self, event, pressed):

        if super().checkLeader(event, pressed):
            normal=getattr(self.app.plugman.plugs, 'normal', False)
            return normal and normal.listening
