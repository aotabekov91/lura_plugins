from PyQt5 import QtGui
from plug.qt import Plug

from .widget import ListWidget

class AnnotateList(Plug):

    position='overlay'

    def setup(self):

        self.colors={}
        self.func_colors={}
        super().setup()
        self.app.moder.plugsLoaded.connect(
                self.setAnnotatePlug)

    def setAnnotatePlug(self, plugs):

        p=plugs.get('annotate', None)
        if p:
            u=self.app.uiman
            self.colors=p.colors
            p.startedListening.connect(
                    lambda: u.activate(self))
            p.endedListening.connect(
                    lambda: u.deactivate(self))
            self.setupUI()

    def setupUI(self):

        l=ListWidget()
        self.app.uiman.setupUI(self, l)
        for k, v in self.colors.items():
            t=f'{v["name"]} [{k}]'
            i=QtGui.QStandardItem(t)
            self.ui.model.appendRow(i)
