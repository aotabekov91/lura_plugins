from plug.qt import Plug
from gizmo.utils import tag
from gizmo.widget import InputList

class Progress(Plug):

    def __init__(self, app, **kwargs):

        super(Progress, self).__init__(
                app=app,
                position='window',
                leader_keys={'command':'r'},
                **kwargs,
                )

        self.setUI()
        # TODO: to finish

    def setUI(self):

        self.uiman.setUI()

        self.ui.addWidget(InputList(), 'main', main=True)
        self.ui.main.input.setLabel('Reading list')

        self.ui.hideWanted.connect(self.deactivate)
        self.ui.installEventFilter(self)

    @tag('t', modes=['command']) 
    def toggle(self): super().toggle() 
