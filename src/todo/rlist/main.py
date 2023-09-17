from plug.qt import Plug
from plug.qt.utils import register
from gizmo.widget import InputList

class ReadingList(Plug):

    def __init__(self, app, **kwargs):

        super(ReadingList, self).__init__(
                app=app,
                position='window',
                mode_keys={'command':'r'},
                **kwargs,
                )

        self.setUI()
        # TODO: to finish

    def setUI(self):

        super().setUI()

        self.ui.addWidget(InputList(), 'main', main=True)
        self.ui.main.input.setLabel('Reading list')

        self.ui.hideWanted.connect(self.deactivate)
        self.ui.installEventFilter(self)

    @register('t', modes=['command']) 
    def toggle(self): super().toggle() 