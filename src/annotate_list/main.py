from PyQt5 import QtGui
from plug.qt import Plug

from .widget import ListWidget

class AnnotateList(Plug):

    def __init__(self, app, *args, **kwargs):

        self.colors={}
        self.func_colors={}

        super().__init__(
                *args, 
                app=app, 
                **kwargs,
                )
        self.app.moder.plugsLoaded.connect(
                self.on_plugsLoaded)

    def on_plugsLoaded(self, plugs):

        self.annotate=plugs.get('Annotate', None)
        if self.annotate:
            self.setUI()
            self.annotate.startedListening.connect(
                    self.on_startedListening)
            self.annotate.endedListening.connect(
                    self.on_endedListening)

    def on_startedListening(self):

        self.ui.show()
        self.ui.updatePosition()

    def on_endedListening(self):

        self.ui.hide()

    def setUI(self):

        self.ui=ListWidget(
                    objectName='Annotate',
                    parent=self.app.window,
                )
        for k, v in self.annotate.colors.items():
            name=v['name']
            text=f'{name} [{k}]'
            item=QtGui.QStandardItem(text)
            self.ui.model.appendRow(item)
        self.ui.hide()
