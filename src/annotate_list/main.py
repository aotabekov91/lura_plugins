from PyQt5 import QtGui
from plug.qt import Plug

from .widget import ListWidget

class AnnotateList(Plug):

    def setup(self):

        self.colors={}
        self.func_colors={}
        super().setup()
        self.app.moder.plugsLoaded.connect(
                self.setAnnotatePlug)

    def setAnnotatePlug(self, plugs):

        p=plugs.get('annotate', None)
        if p:
            p.startedListening.connect(
                    self.uiman.activate)
            p.endedListening.connect(
                    self.uiman.deactivate)
            self.colors=p.colors
            self.setUI()

    def setUI(self):

        self.uiman.position='overlay'
        self.uiman.setUI(ListWidget())
        for k, v in self.colors.items():
            t=f'{v["name"]} [{k}]'
            i=QtGui.QStandardItem(t)
            self.ui.model.appendRow(i)
