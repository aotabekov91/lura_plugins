from PyQt5 import QtCore, QtWidgets

from gizmo.utils import tag
from plug.qt.plugs import TreePlug

class Outline(TreePlug):

    def __init__(
            self, 
            position='dock_left',
            prefix_keys={
                'command': 'o',
                'Outline': '<c-.>',
                },
            **kwargs): 

        super().__init__(
                position=position,
                prefix_keys=prefix_keys,
                **kwargs,
                )
        self.app.moder.modeChanged.connect(
                self.updateView)

    def updateView(self, mode):

        if not hasattr(mode, 'getView'):
            return
        view=mode.getView()
        if not hasattr(view, 'check'):
            return
        if not view.check('hasOutline'):
            return 
        self.view=view
        outline=view.getOutline()
        self.tree.setModel(outline)
        view.indexChanged.connect(
                self.updateTree)

    def updateTree(self, v, idx):

        i=self.view.item(idx)
        idx=self.view.findInOutline(i)
        self.tree.setCurrentIndex(idx)

    def setupUI(self):

        super().setupUI()
        self.tree=self.ui.main.tree

    @tag('o')
    def open(self, *args, **kwargs):

        item=self.tree.currentItem()
        self.view.openOutlineItem(item)
