from tables import Quickmark as Table

from plug.qt import PlugObj
from plug.qt.utils import register
from gizmo.widget import Item, InputList 

class Quickmark(PlugObj):

    def __init__(self, app, **kwargs):

        super().__init__(
                app=app, 
                position='right', 
                mode_keys={'command': 't'},
                **kwargs)

        self.marks = Table() 

        self.setUI()

        self.app.window.main.display.viewChanged.connect(self.setData)

    def setUI(self):

        super().setUI()

        main=InputList(item_widget=Item)

        self.ui.addWidget(main, 'main', main=True)
        self.ui.main.input.hideLabel()
        self.ui.main.returnPressed.connect(self.on_returnPressed)
        self.ui.main.inputTextChanged.connect(self.on_inputTextChanged)

        self.ui.hideWanted.connect(self.deactivateDisplay)
        self.ui.installEventFilter(self)

    def on_inputTextChanged(self):

        if self.ui.main.list.count()==1: self.on_returnPressed()

    def on_returnPressed(self):

        item=self.ui.main.list.currentItem()
        if item and 'position' in item.itemData:
            self.jump(item.itemData)
            self.ui.main.input.clear()
            self.deactivateDisplay()

    @register('dD')
    def deactivateDisplay(self):

        self.activated=False
        self.ui.deactivate()

    def deactivate(self):

        self.activated=False

        self.app.window.bar.hide()
        self.app.window.bar.edit.hide()
        self.app.window.bar.edit.textChanged.disconnect(self.write)
        self.app.window.bar.hideWanted.disconnect(self.deactivate)

    @register('m', modes=['normal', 'command'])
    def mark(self):

        view=self.app.window.main.display.currentView()

        if view:

            self.activated=True

            self.app.window.bar.show()
            self.app.window.bar.edit.show()
            self.app.window.bar.edit.setFocus()

            self.app.window.bar.hideWanted.connect(self.deactivate)
            self.app.window.bar.edit.textChanged.connect(self.write)

    @register('t', modes=['normal', 'command'])
    def goto(self): 

        self.activated=True
        self.ui.activate()

    def setData(self):

        document= self.app.window.main.display.view.model()
        if document:
            dhash = document.hash()
            rows=self.marks.getRow({'hash': dhash})
            for row in rows: row['up']=row['mark']
            if not rows: rows=[{'up': 'No quickmark is found'}]
            self.ui.main.setList(rows)

    @register('D')
    def delete(self):

        item=self.ui.main.list.currentItem()
        if self.activated and item: 
            self.marks.removeRow({'id': item.itemData['id']})
            self.setData()

    def write(self):

        mark=self.app.window.bar.edit.text()
        self.deactivate()

        if mark: 
            view = self.app.window.main.display.currentView()
            dhash= self.app.window.main.display.currentView().document().hash()
            page = self.app.window.main.display.currentView().currentPage()
            left, top = self.app.window.main.display.currentView().saveLeftAndTop()
            position=f'{page}:{left}:{top}'
            data={'hash':dhash, 'position': position, 'mark':mark}
            self.marks.writeRow(data)
            self.setData()

    def jump(self, mark):

        page, left, top = tuple(mark['position'].split(':'))
        self.app.window.main.display.currentView().goto(
                int(page), float(left), float(top))
        self.app.window.main.display.currentView().setFocus()
