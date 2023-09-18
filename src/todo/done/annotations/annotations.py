import functools

from plug.qt import Plug
from plug.qt.utils import register
from gizmo.widget import InputList, ListWidget, UpDownEdit

from lura.utils import getPosition, getBoundaries

class Annotations(Plug):

    def __init__(self, 
                 app, 
                 annotation, 
                 mode_keys={'command': 'a'},
                 **kwargs):

        self.sort_by='id'
        self.sort_order='descending'

        self.annotation=annotation

        super().__init__(
                app=app, 
                position='right', 
                mode_keys=mode_keys,
                **kwargs)

        self.app.window.main.display.viewSelection.connect(
                self.on_viewSelection)

        self.setUI()

    def setActions(self):

        super().setActions()
        self.functions={}
        self.annotateActions={(self.__class__.__name__, 'toggle'): self.toggle}

        if self.config.get('Colors', None):
            self.colors = self.config.get('Colors')
            for key, col in self.colors.items():

                color, function= col[0], col[1]
                func=functools.partial(self.update, function=function)
                func.key=f'{key.title()}'
                func.info=None
                func.command=True
                func.name=function
                func.modes=[]

                self.commandKeys[key]=func
                self.functions[function]=color
                self.actions[(self.__class__.__name__, function)]=func

        self.app.plugman.register(self, self.actions)

    @register('st')
    def selectTerm(self): self.update(function='Term')

    @register('sm')
    def selectMain(self): self.update(function='Main')

    @register('sd')
    def selectData(self): self.update(function='Data')

    @register('sq')
    def selectQuestion(self): self.update(function='Question')

    @register('sm')
    def selectMethodology(self): self.update(function='methodology')

    @register('f', modes=['command'])
    def focusOnField(self, digit=1):

        digit-=1
        if hasattr(self.ui.current, 'list'):
            widget=self.ui.current.list.getWidget(digit)
            self.actOnFocus()
            widget.setFocus()
            widget.down.moveCursor(QTextCursor.End)

    @register('sid')
    def sortByIdDescending(self): 

        self.sort_by='id'
        self.sort_order='descending'
        self.update()

    @register('sia')
    def sortByIdAscending(self): 
        self.sort_by='id'
        self.sort_order='ascending'
        self.update()

    @register('spd')
    def sortByPageDescending(self): 

        self.sort_by='page'
        self.sort_order='descending'
        self.update()

    @register('spa')
    def sortByPageAscending(self): 

        self.sort_by='page'
        self.sort_order='ascending'
        self.update()

    def sort(self, annotations):

        if self.sort_by=='page':
            func=lambda x: (x.get('page', -1), x.get('position', 0))
        else:
            func=lambda x: x.get('id', -1)

        if self.sort_order=='descending':
            annotations=sorted(
                    annotations, 
                    key=lambda x: x.get('id', -1), 
                    reverse=True)
        else:
            annotations=sorted(
                    annotations, 
                    key=func,
                    reverse=False)

        return annotations

    def setUI(self):

        super().setUI()

        self.ui.addWidget(InputList(item_widget=UpDownEdit), 'main', main=True)

        self.ui.main.input.hideLabel()
        self.ui.main.returnPressed.connect(self.open)
        self.ui.main.list.widgetDataChanged.connect(self.on_contentChanged)
        self.ui.main.list.itemChanged.connect(self.on_itemChanged)

        self.ui.hideWanted.connect(self.deactivate)
        self.ui.installEventFilter(self)

    def update(self, function=None):

        view=self.app.window.main.display.currentView()
        annotations=view.model().annotations()
        native=view.model().nativeAnnotations()

        dhash=view.model().hash()

        for a in annotations:

            a['up']=f'# {a.get("id")}'
            a['down']=a['content']
            a['up_color']=a['color'].name()

        for n in native:
            data={
                  'pAnn':n,
                  'up': 'Native',
                  'hash': dhash,
                  'up_color':n.color(),
                  'down':n.contents(),
                  'kind': 'document',
                  'text': n.contents(),
                  'content': n.contents(),
                  'color': QColor(n.color()),
                  'page': n.page().pageNumber(),
                  }
            annotations+=[data]

        if annotations:
            annotations=self.sort(annotations)
            if function: 
                tmp=[]
                for a in annotations:
                    if a.get('function', None)==function:
                        tmp+=[a]
                annotations=tmp
            self.ui.main.setList(annotations)
        else:
            self.ui.main.setList([])

    def on_viewSelection(self, view, selections):

        if selections:
            s=selections[0]
            for j, i in enumerate(self.ui.main.list.filterList()):
                page=s['item'].page().pageNumber()#+1
                if page==i['page']:
                    for ss in selections[0]['area_unified']:
                        for b in i['boundaries']:
                            if b.intersects(ss) or ss.intersects(b):
                                self.ui.main.list.setCurrentRow(j)
                                return

    def on_itemChanged(self, item): 

        if self.ui.main.list.hasFocus(): self.open(item)

    @register('o')
    def openAndFocus(self):

        self.open()
        self.app.modes.setMode('normal')

    @register('O')
    def open(self, item=None):

        if not item: item=self.ui.main.list.currentItem()

        if item:
            aid=item.itemData.get('id', None)
            pAnn=item.itemData.get('pAnn', None)
            if aid:
                self.openById(aid)
            elif pAnn:
                self.openByData(pAnn)

    def openByData(self, pAnn):

        boundary=pAnn.boundary()
        topLeft=boundary.topLeft() 
        x, y = topLeft.x(), topLeft.y()
        page=pAnn.page().pageNumber()
        view=self.app.window.main.display.currentView()
        if view: view.goto(page, x, y-0.05)

    def openById(self, aid):

        data=self.app.tables.annotation.getRow({'id':aid})
        if data:
            data=data[0]
            dhash=data['hash']
            page=data['page']
            boundaries=getBoundaries(data['position'])
            boundary=boundaries[0]
            topLeft=boundary.topLeft() 
            x, y = topLeft.x(), topLeft.y()
            view=self.app.window.main.display.currentView()
            if view: view.goto(page, x, y-0.05)

    def on_contentChanged(self, widget):

        data=widget.data
        aid=data['id']
        text=widget.textDown()
        self.app.tables.annotation.updateRow({'id':aid}, {'content':text})

    @register('O')
    def openAndHide(self):

        self.open()
        self.deactivateUI()

    @register('D')
    def delete(self):

        item=self.ui.main.list.currentItem()
        nrow=max(self.ui.main.list.currentRow()-1, 0)

        if item:

            self.app.tables.annotation.removeRow(
                    {'id': item.itemData.get('id', None)})

            page=self.app.window.main.display.view.model().page(
                item.itemData['page'])

            page.removeAnnotation(item.itemData)
            page.pageItem().refresh(dropCachedPixmap=True)

            self.update()
            self.ui.main.list.setCurrentRow(nrow)
            self.ui.main.setFocus()

    @register('t', modes=['command'])
    def toggle(self): super().toggle()

    def activate(self):

        self.update()
        self.app.window.main.display.viewChanged.connect(self.update)

        super().activate()

    def deactivate(self):

        self.app.window.main.display.viewChanged.disconnect(self.update)
        super().deactivate()
