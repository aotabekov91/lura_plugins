import functools

from PyQt5 import QtGui

from plug.qt import Plug
from plug.qt.utils import register
from tables import Annotation as Table
from lura.utils import getPosition, getBoundaries

class Annotate(Plug):

    def __init__(self, 
                 app, 
                 *args, 
                 listen_leader='<c-a>', 
                 **kwargs):

        self.colors={}
        self.func_colors={}
        self.default_color='cyan'

        super().__init__(
                *args, 
                app=app, 
                listen_leader=listen_leader,
                **kwargs,
                )
        self.table=Table()

    def setup(self):

        super().setup()
        self.setColors()
        self.setConnect()

    def setConnect(self):

        self.display=self.app.window.main.display
        self.app.buffer.bufferCreated.connect(self.paint)
        self.display.itemMousePressOccured.connect(
                self.on_mousePressEvent)

    def setColors(self):

        for k, v in self.colors.items():
            func=functools.partial(
                    self.annotate, 
                    function=v['name'])
            func.key=f'{k}'
            func.modes=[]
            self.commandKeys[k]=func
            self.func_colors[v['name']]=v['color']
            self.actions[(self.name, v['name'])]=func
        self.app.plugman.register(self, self.actions)

    def on_mousePressEvent(self, v, i, e):

        self.selected=None
        page=i.page().pageNumber()
        point=i.mapToPage(e.pos(), unify=False)
        pos=i.mapToPage(point, unify=True)
        for a in v.model().annotations(): 
            if page==a['page']:
                for b in a['boundaries']:
                    if b.contains(pos):
                        a['box']=[]
                        for b in a['boundaries']:
                            self.selected=a
                            box = i.mapToItem(b, isUnified=True)
                            box = i.mapToPage(box, unify=False)
                            a['box'] += [box]
                            a['item'] = i
                            v.select([a])
                            i.update()
                            break

    def annotate(self, function):

        self.delistenWanted.emit()
        selections=self.display.view.selected()
        if selections:
            selection=selections[0]
            text=selection['text']
            pageItem=selection['item']
            area=selection['area_unified']
            page=pageItem.page()
            pageNumber = page.pageNumber()
            dhash = page.document().hash()
            aData=self.write(
                    dhash, 
                    pageNumber, 
                    text, 
                    area, 
                    function)
            self.add(page.document(), aData)
            pageItem.select()
            pageItem.refresh(dropCachedPixmap=True)

    def write(self, 
              dhash, 
              pageNumber, 
              text, 
              boundaries, 
              function):

        position=getPosition(boundaries)
        data = {'hash': dhash,
                'page': pageNumber,
                'position': position,
                'kind':'document',
                'content':text,
                'function':function,
                }
        self.table.writeRow(data)
        for f in ['function', 'kind', 'content']: 
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
            dhash = document.hash()
            aData=self.table.getRow({'hash':dhash})
            for annotation in aData: 
                self.add(document, annotation)

    def checkLeader(self, event, pressed):

        if super().checkLeader(event, pressed):
            if self.listening: return True
            view=self.display.view
            current=self.app.plugman.current
            if view and current:
                if current.name=='normal':
                    return True
                elif current.name=='visual':
                    return current.hinting
        return False
