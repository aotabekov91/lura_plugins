from PyQt5 import QtGui
from plug.qt import Plug

from .widget import ListWidget

class AnnotateList(Plug):

    def setup(self):

        self.colors={}
        self.func_colors={}
        super().setup()
        self.app.moder.plugsLoaded.connect(
                self.on_plugsLoaded)

    def on_plugsLoaded(self, plugs):

        self.annotate=plugs.get('annotate', None)
        if self.annotate:
            self.setUI()
            self.annotate.startedListening.connect(
                    self.on_startedListening)
            self.annotate.endedListening.connect(
                    self.on_endedListening)

    def on_startedListening(self):
        self.uiman.activate()

    def on_endedListening(self):
        self.uiman.deactivate()

    def setUI(self):

        self.uiman.position='overlay'
        self.uiman.setUI(ListWidget())
        self.setColors()

    def setColors(self):

        clrs=self.annotate.colors
        for k, v in clrs.items():
            t=f'{v["name"]} [{k}]'
            i=QtGui.QStandardItem(t)
            self.ui.model.appendRow(i)
