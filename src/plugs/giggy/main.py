from qapp.plug import PlugObj
from qapp.utils import register
from qapp.widget import InputList

class Giggy(PlugObj):

    def __init__(self, app):

        super(Giggy, self).__init__(
                app=app,
                position='left',
                mode_keys={'command':'p'})

        # self.setUI()
        # TODO: to finish

    def setUI(self):

        super().setUI()

        self.ui.addWidget(InputList(), 'main', main=True)
        self.ui.main.input.setLabel('Reading list')

        self.ui.hideWanted.connect(self.deactivate)
        self.ui.installEventFilter(self)

    @register('t', modes=['command']) 
    def toggle(self): super().toggle() 

    @register(modes=['exec']) 
    def plugInstall(self): print('here')

    @register(modes=['exec']) 
    def plugCleanup(self): print('here')
