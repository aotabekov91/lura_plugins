from tables import Part as Table

from plug.qt import Plug 
from gizmo.utils import tag
from gizmo.widget import ItemWidget, InputList

from .widget import PartTree

class Parts(Plug):

    def __init__(
            self, 
            app, 
            *args,
            position='dock_left',
            leader_keys={'command': 'p'},
            **kwargs):

        self.follow=False

        super(Parts, self).__init__(
                *args,
                app=app, 
                position=position, 
                leader_keys=leader_keys,
                **kwargs)

        self.table=Table()
        self.setUI()

    def setup(self):

        super().setup()
        self.display=self.app.display

    @tag('f')
    def toggleFollow(self): 
        self.follow=not self.follow

    def setUI(self):

        self.app.uiman.setUI(self)
        t=PartTree()
        t.returnPressed.connect(self.open)
        t.itemChanged.connect(self.on_itemChanged)
        self.ui.addWidget(t, 'tree')
        m=InputList(widget=ItemWidget)
        m.returnPressed.connect(self.open)
        self.ui.addWidget(m, 'main', main=True)

    def on_itemChanged(self, item): 

        if self.follow: 
            self.open(item=item)

    @tag('tr')
    def toggleTree(self):

        if self.ui.tree.isVisible():
            self.ui.show()
        else:
            self.ui.show(self.ui.tree)

    @tag('r')
    def refresh(self):

        view=self.display.view
        if view:
            dhash=view.model().id()
            data=self.table.getTreeDict(dhash)
            if data: 
                self.ui.tree.installData({'root': data})

    @tag('t', modes=['command'])
    def toggle(self): super().toggle()

    def activate(self):

        self.refresh()
        self.toggleTree()
        super().activate()

    @tag('sr')
    def showReference(self): 
        self.setData('reference')

    @tag('sa')
    def showAbstract(self): 
        self.setData('abstract')

    @tag('so')
    def showOutline(self): 
        self.setData('section')

    @tag('sk')
    def showKeyword(self): 
        self.setData('keyword')

    @tag('ss')
    def showSummary(self): 
        self.setData('summary')

    @tag('sp')
    def showParagraph(self): 
        self.setData('paragraph')

    @tag('sb')
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

    @tag('p')
    def parse(self):

        if self.display.view:
            p=self.display.view.model().filePath()
            self.app.tables.hash.hash(
                    p, force_parse=True)

    @tag('o')
    def openAndFocus(self): 
        self.open(focus=True)

    @tag('O')
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
