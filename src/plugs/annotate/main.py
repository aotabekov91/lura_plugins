import functools

from PyQt5 import QtGui

from plug.qt import Plug
from tables import Annotation as Table
from lura.utils import getPosition, getBoundaries

class Annotate(Plug):

    def __init__(self, app, *args, **kwargs):

        self.colors={}

        super().__init__(
                *args, 
                app=app, 
                listen_leader='<c-a>', 
                **kwargs,
                )
        self.table=Table()
        self.app.buffer.bufferCreated.connect(self.paint)

    def setup(self):

        super().setup()
        self.setColors()

    def setColors(self):

        for k, v in self.colors.items():
            function=v['name']
            func=functools.partial(
                    self.annotate, 
                    function=function)
            func.key=f'{k}'
            func.modes=[]
            self.commandKeys[k]=func
            self.actions[(self.name, function)]=func
        self.app.plugman.register(self, self.actions)

    def annotate(self, function):

        self.deactivate()
        selections=self.app.window.main.display.view.selected()
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
        self.delistenWanted.emit()

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

    def remove(self):

        if self.selected:
            annotation=self.selected
            self.selected=None
            self.remove(annotation)
        self.setFocus()

    def add(self, document, annotation):

        page=document.page(annotation['page'])
        annotation['color'] = QtGui.QColor(
                self.colors.get(
                    annotation['function'], 'cyan'))
        annotation['boundaries']=getBoundaries(
                annotation['position'])
        return page.annotate(
                annotation, 
                kind='highlightAnnotation')

    def paint(self, document=None):

        if not document: 
            view=self.app.window.main.display.view
            if view: document=view.model()
        if document:
            dhash = document.hash()
            aData=self.table.getRow({'hash':dhash})
            for annotation in aData: 
                self.add(document, annotation)

    def checkLeader(self, event, pressed):

        if super().checkLeader(event, pressed):
            view=self.app.window.main.display.view
            current=self.app.plugman.current
            if view and current:
                if current.name=='normal':
                    return True
                elif current.name=='visual':
                    return current.hinting
        return False
