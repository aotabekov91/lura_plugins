from plug.qt import Plug
from gizmo.utils import tag

from .widget import PagerWidget

class Pager(Plug):

    def __init__(
            self, 
            *args, 
            **kwargs
            ):

        super().__init__(
                *args,
                position='overlay', 
                **kwargs)

        self.setupUI()
        self.app.display.itemChanged.connect(
                self.on_itemChanged
                )
        self.app.display.viewChanged.connect(
                self.on_itemChanged
                )
        self.app.ui.bar.toggled.connect(
                self.on_barToggled
                )

    def on_barToggled(self, visible):

        if visible:
            self.ui.paddingBottom=35
        else:
            self.ui.paddingBottom=15
        self.ui.updatePosition()

    def on_viewChanged(self, view): 

        self.on_itemChanged(view) 

    def on_itemChanged(self, view, item=None): 

        count=view.count()
        cpage=view.current()
        self.ui.setText(f'{cpage}/{count}')

    def setupUI(self):

        self.ui=PagerWidget(self.app.ui.main)
        self.ui.hide()

    @tag('p', modes=['normal', 'command'])
    def toggle(self): 

        self.ui.updatePosition()
        super().toggle()
