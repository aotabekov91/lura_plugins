from PyQt5 import QtGui

from qapp.app.plug import Plug 
from qapp.utils import register

from lura.utils import getBoundaries
from tables import Annotation as Table

from .annotate import Annotate
from .annotations import Annotations

class Annotation(Plug):

    def __init__(self, app):

        super().__init__(app=app, 
                         listen_port=False,
                         mode_keys={'command': 'a'})

        self.functions={}
        self.table=Table()
        self.annotate=Annotate(app=app, annotation=self)
        self.annotations=Annotations(app=app, annotation=self)

        self.paint()
        self.app.buffer.bufferCreated.connect(self.paint)
        # self.app.main.display.mousePressOccured.connect(self.on_mousePressEvent)

    def select(self, function): return

    def on_mousePressEvent(self, event, pageItem, view): return

        # boundaries=[]
        # text, area=self.app.main.display.currentView().getCursorSelection(clear=True)
        # for rectF in area: boundaries += [pageItem.mapToPage(rectF)[1]]
        # print(text, area, boundaries, pageItem.m_boundingRect)

        # self.selected=None
        # pos=pageItem.mapToPage(event.pos())
        # for annotation in view.model().annotations(): 
        #     if annotation.page().pageItem()==pageItem:
        #         if annotation.contains(pos):
        #             self.selected=annotation
        #             break
        # # if self.selected: print('point', pos, self.selected.boundary())

    @register('r')
    def remove(self):

        if self.selected:
            annotation=self.selected
            self.selected=None
            self.remove(annotation)
        self.setFocus()

    def update(self): self.annotations.update()

    def add(self, document, annotation):

        page=document.page(annotation['page'])
        annotation['color'] = QtGui.QColor(
                self.functions.get(annotation['function'], 'cyan'))
        annotation['boundaries']=getBoundaries(
                annotation['position'])
        return page.annotate(annotation, kind='highlightAnnotation')

    def paint(self, document=None):

        if not document: 

            view=self.app.main.display.view
            if view: document=view.model()

        if document:

            dhash = document.hash()
            aData=self.table.getRow({'hash':dhash})
            for annotation in aData: self.add(document, annotation)
