from tables import Part as Table

from plug.qt import Plug 
from gizmo.utils import register
from gizmo.widget import ItemWidget, InputList

from .widget import PartTree

class Parts(Plug):

    def __init__(
            self, 
            app, 
            *args,
            position='left',
            prefix_keys={'command': 'p'},
            **kwargs):

        self.follow=False

        super(Parts, self).__init__(
                *args,
                app=app, 
                position=position, 
                prefix_keys=prefix_keys,
                **kwargs)

        self.table=Table()
        self.setUI()

    def setup(self):

        super().setup()
        self.display=self.app.display

    @register('f')
    def toggleFollow(self): 
        self.follow=not self.follow

    def setUI(self):

        self.uiman.setUI()
        tree=PartTree()
        tree.returnPressed.connect(
                self.open)
        tree.itemChanged.connect(
                self.on_itemChanged)
        self.ui.addWidget(tree, 'tree')
        main=InputList(
                widget=ItemWidget)
        main.input.hideLabel()
        main.returnPressed.connect(
                self.open)
        self.ui.addWidget(
                main, 'main', main=True)
        self.ui.hideWanted.connect(
                self.deactivate)

    def on_itemChanged(self, item): 

        if self.follow: 
            self.open(item=item)

    @register('tr')
    def toggleTree(self):

        if self.ui.tree.isVisible():
            self.ui.show()
        else:
            self.ui.show(self.ui.tree)

    @register('r')
    def refresh(self):

        view=self.display.view
        if view:
            dhash=view.model().id()
            data=self.table.getTreeDict(dhash)
            if data: 
                self.ui.tree.installData({'root': data})

    @register('t', modes=['command'])
    def toggle(self): super().toggle()

    def activate(self):

        self.refresh()
        self.toggleTree()
        super().activate()

    @register('sr')
    def showReference(self): 
        self.setData('reference')

    @register('sa')
    def showAbstract(self): 
        self.setData('abstract')

    @register('so')
    def showOutline(self): 
        self.setData('section')

    @register('sk')
    def showKeyword(self): 
        self.setData('keyword')

    @register('ss')
    def showSummary(self): 
        self.setData('summary')

    @register('sp')
    def showParagraph(self): 
        self.setData('paragraph')

    @register('sb')
    def showBibliography(self): 
        self.setData('bibliography')

    def setData(self, kind):

        if not self.activated: 
            self.activate()
        view=self.display.currentView()
        if view: 
            dhash=view.model().id() 
            data=self.table.search(f'hash:{dhash} kind:{kind}')
            for d in data:
                d['up']=d['text']
                d['up_color']='green'
            data=sorted(data, key=lambda x: (x['page'], x['y1']))
            self.ui.main.setList(data)

    @register('p')
    def parse(self):

        if self.display.view:
            p=self.display.view.model().filePath()
            self.app.tables.hash.hash(
                    p, force_parse=True)

    @register('o')
    def openAndFocus(self): 
        self.open(focus=True)

    @register('O')
    def open(self, item=None, focus=False):

        if item is None:
            if self.ui.main.isVisible():
                item=self.ui.main.list.currentItem()
            elif self.ui.tree.isVisible():
                item=self.ui.tree.currentItem()
        if item:
            page=item.itemData['page']+1
            y=item.itemData['y1']-0.05
            view=self.display.currentView()
            if view: 
                view.goto(page, 0, y)
                if focus: self.app.modes.setMode('normal')
