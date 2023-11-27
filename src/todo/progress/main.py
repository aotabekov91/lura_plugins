from plug.qt import Plug
from gizmo.utils import tag
from gizmo.widget import InputList

class Progress(Plug):

    def __init__(self, app, **kwargs):

        super(Progress, self).__init__(
                app=app,
                position='window',
                prefix_keys={'command':'r'},
                **kwargs,
                )

        self.setupUI()
        # TODO: to finish

    def setupUI(self):

        self.uiman.setupUI()

        self.ui.addWidget(InputList(), 'main', main=True)
        self.ui.main.input.setLabel('Reading list')

        self.ui.hideWanted.connect(self.octivate)
        self.ui.installEventFilter(self)

    @tag('t', modes=['command']) 
    def toggle(self): super().toggle() 
