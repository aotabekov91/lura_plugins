from PyQt5 import QtGui
from plug.qt import Plug
from gizmo.utils import register
from tables import Annotation as Table
from gizmo.widget import InputList, UpDownEdit

class Annotations(Plug):

    def __init__(
            self, 
            app, 
            position='right',
            prefix_keys={
                'command': 'A',
                'Annotations': '<c-.>'
                },
            **kwargs
            ):

        self.table=Table()
        super().__init__(
                app=app, 
                position=position,
                prefix_keys=prefix_keys,
                **kwargs)
        self.setUI()
        self.connect()

    def connect(self):

        self.display=self.app.display
        self.display.viewChanged.connect(
                self.update)
        self.display.viewSelection.connect(
                self.on_viewSelection)
        self.app.moder.plugsLoaded.connect(
                self.on_plugsLoaded)

    def on_plugsLoaded(self, plugs):

        self.annotate=plugs.get(
                'annotate', None)
        if self.annotate:
            self.annotate.annotated.connect(
                    self.update)

    def setUI(self):

        w=InputList(widget=UpDownEdit)
        w.returnPressed.connect(self.open)
        w.list.widgetDataChanged.connect(
                self.on_contentChanged)
        self.uiman.setUI(w)

    def setColorStyle(self, ann):

        color=ann['color'].name()
        style=f'background-color: {color}'
        ann['up_style']=style

    def update(self):

        view=self.display.currentView()
        if view:
            dhash=view.model().id()
            annotations=view.model().annotations()
            native=view.model().nativeAnnotations()
            for a in annotations:
                a['view']=view
                a['down']=a['content']
                a['up']=f'# {a.get("id")}'
                self.setColorStyle(a)
            for n in native:
                data={
                      'pAnn':n,
                      'view': view,
                      'up': 'Native',
                      'hash': dhash,
                      'up_color':n.color(),
                      'down':n.contents(),
                      'kind': 'document',
                      'text': n.contents(),
                      'content': n.contents(),
                      'page': n.page().pageNumber(),
                      'color': QtGui.QColor(n.color()),
                      }
                annotations+=[data]
            self.ui.setList(annotations)

    def on_viewSelection(self, view, selections):

        if selections:
            s=selections[0]
            aid=s.get('aid', None)
            if aid:
                d=enumerate(self.ui.list.flist)
                for j, i in d:
                    if i.get('id', None)!=aid:
                        continue
                    self.ui.list.setCurrentRow(j)
                    return

    def openByData(self, pAnn, data):

        view=data.get('view', None)
        if pAnn and view:
            boundary=pAnn.boundary()
            topLeft=boundary.topLeft() 
            x, y = topLeft.x(), topLeft.y()
            page=pAnn.page().pageNumber()
            view.goto(page, x, y-0.05)

    def openById(self, aid, data):

        view=data.get('view', None)
        data=self.table.getRow({'id':aid})
        if data and view:
            data=data[0]
            page=data['page']
            boundaries=view.model().getBoundaries(
                    data['position'])
            boundary=boundaries[0]
            topLeft=boundary.topLeft() 
            x, y = topLeft.x(), topLeft.y()
            if view: 
                view.goto(page, x, y-0.05)

    def on_contentChanged(self, widget):

        data=widget.data
        aid=data['id']
        text=widget.textDown()
        self.table.updateRow(
                {'id':aid}, {'content':text})

    @register('d')
    def delete(self):

        item=self.ui.list.currentItem()
        nrow=max(self.ui.list.currentRow()-1, 0)
        if item:
            view=self.display.view
            aid=item.itemData.get(
                    'id', None)
            apage=item.itemData.get(
                    'page', None)
            self.table.removeRow(
                    {'id': aid})
            page=view.model().page(
                    apage)
            page.removeAnnotation(
                    item.itemData)
            page.pageItem().refresh(
                    dropCachedPixmap=True)
            self.update()
            self.ui.list.setCurrentRow(
                    nrow)

    @register('O')
    def openAndFocus(self):

        self.open()
        self.delistenWanted.emit()

    @register('o')
    def open(self, item=None):

        if not item: 
            item=self.ui.list.currentItem()
        if item:
            aid=item.itemData.get('id', None)
            pAnn=item.itemData.get('pAnn', None)
            if aid:
                self.openById(aid, item.itemData)
            elif pAnn:
                self.openByData(pAnn, item.itemData)
