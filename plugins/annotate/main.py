import os
import functools

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from plugin.app import register
from plugin.app.plugin import Plugin 

from lura.utils import getBoundaries

from .annotate import Annotate
from .annotations import Annotations

class Annotation(Plugin):

    def __init__(self, app):

        super().__init__(app, mode_keys={'command': 'a'})

        self.functions={}
        self.annotate=Annotate(app, self)
        self.annotations=Annotations(app, self)

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

        dhash = document.hash()
        page=document.page(annotation['page'])
        annotation['color'] = QColor(
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
            aData=self.app.tables.annotation.getRow({'hash':dhash})
            for annotation in aData: self.add(document, annotation)
