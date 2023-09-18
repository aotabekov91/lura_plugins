from tables import Bookmark as Table

from plug.qt import Plug 
from plug.qt.utils import register
from gizmo.widget import UpDownEdit, InputList

class BookmarkDisplay(Plug):

    def __init__(self, app, **kwargs):

        super().__init__(
                app=app, 
                position='right', 
                mode_keys={'command':'b'},
                **kwargs) 

        self.table=Table()
        self.setUI()

    def setUI(self):

        super().setUI()
        main=InputList(item_widget=UpDownEdit)
        self.ui.addWidget(main, 'main', main=True)
        self.ui.main.input.hideLabel()
        self.ui.main.returnPressed.connect(self.open)
        self.ui.main.list.widgetDataChanged.connect(self.on_contentChanged)
        self.ui.hideWanted.connect(self.deactivateDisplay)
        self.ui.installEventFilter(self)

    @register('o')
    def open(self):

        item=self.ui.main.list.currentItem()
        if item: self.app.window.main.openBy('bookmark', item.itemData['id'])

    def on_contentChanged(self, widget):

        bid=widget.data['id']
        text=widget.data['down']
        self.table.updateRow({'id':bid}, {'text':text})

    @register('O')
    def openAndHide(self): 

        self.open()
        self.deactivateDisplay()

    @register('D')
    def delete(self):

        item=self.ui.main.list.currentItem()
        nrow=self.ui.main.list.currentRow()-1
        bid=item.itemData['id']
        self.table.removeRow({'id':bid})
        self.updateData()
        self.ui.main.list.setCurrentRow(nrow)
        self.ui.show()

    @register('u')
    def updateData(self, view=None):

        if not view: view=self.app.window.main.display.currentView()

        if view:
            criteria={'hash': view.model().hash()}
            self.tables = self.table.getRow(criteria)
            if self.tables:
                for a in self.tables:
                    a['up']=f'# {a.get("id")}'
                    a['down']=a['text']
            self.tables=sorted(self.tables, key=lambda x: (x['page'], x['position']))
            self.ui.main.setList(self.tables)

    def activateDisplay(self):

        self.activated=True
        self.updateData()
        self.ui.activate()

    def deactivateDisplay(self):

        self.activated=False
        self.ui.deactivate()

    @register('t', modes=['command'])
    def toggle(self): 

        if self.activated:
            self.deactivateDisplay()
        else:
            self.activateDisplay()

    @register('b', modes=['normal', 'command'])
    def bookmark(self):

        view=self.app.window.main.display.currentView()
        if view:
            self.activated=True
            bar=self.app.window.bar
            bar.show()
            bar.edit.show()
            bar.edit.setFocus()
            bar.edit.returnPressed.connect(
                    self.writeBookmark)
            bar.hideWanted.connect(
                    self.deactivate)
            data=self.getBookmark()
            if data: 
                bar.edit.setText(data[0]['text'])

    def deactivate(self):

        self.activated=False
        self.app.window.bar.hide()
        self.app.window.bar.edit.hide()
        self.app.window.bar.edit.returnPressed.disconnect(
                self.writeBookmark)
        self.app.window.bar.hideWanted.disconnect(
                self.deactivate)

    def getBookmark(self):

        view=self.app.window.main.display.currentView()
        if view:
            data={}
            data['hash']=view.model().hash()
            data['page']=view.pageItem().page().pageNumber()
            data['position']=':'.join([str(f) for f in view.saveLeftAndTop()])
            return self.table.getRow(data)

    def writeBookmark(self):

        text=self.app.window.bar.edit.text()
        self.deactivate()
        view=self.app.window.main.display.currentView()
        if view:
            data=self.getBookmark()
            if data:
                bid=data[0]['id']
                self.table.updateRow(
                        {'id':bid}, {'text':text})
            else:
                data={}
                data['title']=text
                data['text']=text
                data['kind']='document'
                data['hash']=view.model().hash()
                data['page']=view.pageItem().page().pageNumber()
                data['position']=':'.join([str(f) for f in view.saveLeftAndTop()])
                self.table.writeRow(data)
