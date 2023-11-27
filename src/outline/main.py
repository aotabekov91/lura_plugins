from plug.qt import Plug
from gizmo.utils import tag

from .view import OutlineView

class Outline(Plug):

    position={'OutlineView': 'dock_left'}
    prefix_keys={'command': 'o', 'OutlineView': '<c-.>'}

    def setup(self):

        super().setup()
        view=OutlineView
        view.position=self.position
        view.prefix_keys=self.prefix_keys
        self.app.handler.addViewer(view)
        self.app.handler.typeChanged.connect(
                self.updateView)

    def updateView(self, v):

        vm=v.model()
        if self.checkProp('hasOutline', vm):
            m=vm.getOutline()
            self.app.handler.getView(m)
