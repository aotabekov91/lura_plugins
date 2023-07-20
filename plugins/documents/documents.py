from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from plugin.app import register
from plugin.app.plugin import Plugin 
from plugin.widget import UpDown, InputList

class Documents(Plugin):

    def __init__(self, app):

        super().__init__(app, position='right', mode_keys={'command': 'd'})

        self.setUI()

    def setUI(self):

        super().setUI()

        main=InputList(item_widget=UpDown)
        self.ui.addWidget(main, 'main', main=True)

        self.ui.main.input.hideLabel()
        self.ui.main.returnPressed.connect(self.on_returnPressed)
        self.ui.hideWanted.connect(self.deactivate)
        self.ui.installEventFilter(self)

    def activate(self):

        if not hasattr(self, 'dlist'): 
            self.dlist=self.getList()
            self.ui.main.setList(self.dlist)

        super().activate()

    @register('t', modes=['command'])
    def toggle(self): super().toggle()

    def getList(self):

        data=self.app.tables.hash.getAll()
        for d in data:
            d['up']=d['path'].split('/')[-1]
            meta=self.app.tables.metadata.getRow({'hash':d['hash']})
            if meta and meta[0]['title']:
                d['down']=meta[0]['title']
                d['up']=d['path'].split('/')[-1]
                d['up_color']='green'
        return data

    def on_returnPressed(self): 

        self.open(focus=False)
        self.ui.show()

    def open(self, focus=True, how='reset', hide=False):

        if self.activated:

            if hide: self.deactivate()
            if not focus or hide: self.deactivateCommandMode()

            item=self.ui.main.list.currentItem()
            if item:
                path=self.app.tables.hash.getPath(item.itemData['hash'])
                if path: self.app.main.open(path, how=how)

    def openAndHide(self): 

        if self.activated: self.open(focus=True, hide=True)

    def openBelow(self): 

        if self.activated: self.open(focus=True, how='below')

    def openBelowAndHide(self): 

        if self.activated: self.open(how='below', hide=True)
