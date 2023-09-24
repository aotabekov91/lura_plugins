from PyQt5 import QtGui
from plug.qt import Plug
from gizmo.utils import register
from gizmo.widget import InputList, UpDownEdit

from lura.utils import getBoundaries

class Annotations(Plug):

    def __init__(self, 
                 app, 
                 *args, 
                 position='right',
                 **kwargs):

        super().__init__(
                app=app, 
                position=position,
                **kwargs)

        self.setUI()
        self.connect()

    @register('<c-A>', modes=['normal'])
    def toggle(self): super().toggle()

    def connect(self):

        self.display=self.app.display
        self.display.viewChanged.connect(
                self.update)
        self.display.viewSelection.connect(
                self.on_viewSelection)

    def setUI(self):

        self.uiman.setUI()
        self.ui.addWidget(
                InputList(
                    item_widget=UpDownEdit,
                    objectName='Annotations',
                    ), 
                'main', 
                main=True)

        self.ui.main.input.hideLabel()
        self.ui.main.returnPressed.connect(
                self.open)
        self.ui.main.list.widgetDataChanged.connect(
                self.on_contentChanged)
        self.ui.main.list.itemChanged.connect(
                self.on_itemChanged)

    def update(self):

        view=self.display.currentView()
        annotations=[]
        if view:
            dhash=view.model().hash()
            annotations=view.model().annotations()
            native=view.model().nativeAnnotations()

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
                      'color': QtGui.QColor(n.color()),
                      'page': n.page().pageNumber(),
                      }
                annotations+=[data]
            self.ui.main.setList(annotations)
        return annotations

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
        self.modeWanted.emit('normal')

    @register('O')
    def open(self, item=None):

        if not item: 
            item=self.ui.main.list.currentItem()

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
        view=self.display.currentView()
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
            view=self.display.currentView()
            if view: view.goto(page, x, y-0.05)

    def on_contentChanged(self, widget):

        data=widget.data
        aid=data['id']
        text=widget.textDown()
        self.app.tables.annotation.updateRow({'id':aid}, {'content':text})

    @register('O')
    def openAndHide(self):

        self.open()
        self.delistenWanted.emit()

    @register('D')
    def delete(self):

        item=self.ui.main.list.currentItem()
        nrow=max(self.ui.main.list.currentRow()-1, 0)

        if item:

            self.app.tables.annotation.removeRow(
                    {'id': item.itemData.get('id', None)})

            page=self.display.view.model().page(
                item.itemData['page'])

            page.removeAnnotation(item.itemData)
            page.pageItem().refresh(dropCachedPixmap=True)

            self.update()
            self.ui.main.list.setCurrentRow(nrow)
            self.ui.main.setFocus()
