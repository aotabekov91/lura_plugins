import functools
from plug.qt import Plug
from PyQt5 import QtGui, QtCore
from gizmo.utils import register
from tables import Annotation as Table
from lura.utils import getPosition, getBoundaries

class Annotate(Plug):

    chosen=QtCore.pyqtSignal()
    annotated=QtCore.pyqtSignal()

    def __init__(
            self, 
            app, 
            *args, 
            listen_leader='<c-a>', 
            **kwargs
            ):

        self.colors={}
        self.table=Table()
        self.selected=None
        self.func_colors={}
        self.default_color='cyan'
        super().__init__(
                *args, 
                app=app, 
                listen_leader=listen_leader,
                **kwargs,
                )
        self.setColors()
        self.setConnect()

    def setConnect(self):

        self.display=self.app.display
        self.app.buffer.bufferCreated.connect(
                self.paint)
        self.display.itemMousePressOccured.connect(
                self.on_mousePressEvent)

    def setColors(self):

        for k, v in self.colors.items():
            f=functools.partial(
                    self.annotate, 
                    function=v['name'])
            f.key=f'{k}'
            f.modes=[]
            self.func_colors[v['name']]=v['color']
            self.actions[(self.name, v['name'])]=f
        self.app.moder.save(
                self, self.actions)

    def on_mousePressEvent(
            self, 
            view, 
            item, 
            event,
            ):

        self.selected=None
        page=item.page().pageNumber()
        point=item.mapToPage(
                event.pos(), unify=False)
        pos=item.mapToPage(
                point, unify=True)
        annotations=view.model().annotations()
        for a in annotations: 
            if page!=a['page']: 
                continue
            for b in a['boundaries']:
                if not b.contains(pos): 
                    continue
                a['box']=[]
                for b in a['boundaries']:
                    self.selected=a
                    box = item.mapToItem(
                            b, isUnified=True)
                    box = item.mapToPage(
                            box, unify=False)
                    a['box'] += [box]
                a['item'] = item
                a['aid']=a.get('id', None)
                view.select([a])
                item.update()
                self.chosen.emit()
                break

    def annotate(self, function):

        view=self.display.view
        selections=view.selected()
        if selections:
            selection=selections[0]
            text=selection['text']
            pageItem=selection['item']
            area=selection['area_unified']
            page=pageItem.page()
            pageNumber = page.pageNumber()
            dhash = page.document().id()
            aData=self.write(
                    dhash, 
                    pageNumber, 
                    text, 
                    area, 
                    function)
            self.add(page.document(), aData)
            pageItem.select()
            pageItem.refresh(
                    dropCachedPixmap=True)
        self.annotated.emit()
        self.delistenWanted.emit()

    def write(
            self, 
            dhash, 
            pageNumber, 
            text, 
            boundaries, 
            function
            ):

        position=getPosition(boundaries)
        data = {'hash': dhash,
                'page': pageNumber,
                'position': position,
                'kind':'document',
                'content':text,
                'function':function,
                }
        self.table.writeRow(data)
        fld=['function', 'kind', 'content']
        for f in fld:
            data.pop(f)
        return self.table.getRow(data)[0]

    @register('.d')
    def remove(self):

        if self.selected:
            page=self.selected['pAnn'].page()
            self.table.removeRow(
                    {'id': self.selected['id']}) 
            page.removeAnnotation(self.selected)
            page.pageItem().refresh(dropCachedPixmap=True)
            self.selected=None

    def add(self, document, annotation):

        page=document.page(annotation['page'])
        color=self.func_colors.get(
                annotation['function'],
                self.default_color)
        annotation['color'] = QtGui.QColor(color)
        annotation['boundaries']=getBoundaries(
                annotation['position'])

        return page.annotate(
                annotation, 
                kind='highlightAnnotation')

    def paint(self, document=None):

        if not document: 
            view=self.display.view
            if view: document=view.model()
        if document:
            dhash = document.id()
            aData=self.table.getRow({'hash':dhash})
            for annotation in aData: 
                self.add(document, annotation)

    def checkLeader(self, event, pressed):

        if super().checkLeader(event, pressed):
            if self.ear.listening: 
                return True
            view=self.display.view
            current=self.app.moder.current
            if view and current:
                if current.name=='normal':
                    return True
                elif current.name=='visual':
                    return True 
        return False
