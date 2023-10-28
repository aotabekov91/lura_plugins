from plug.qt import Plug
from gizmo.utils import register

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

        self.setUI()
        self.app.display.itemChanged.connect(
                self.on_itemChanged
                )
        self.app.display.viewChanged.connect(
                self.on_itemChanged
                )
        self.app.window.bar.toggled.connect(
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

    def setUI(self):

        self.ui=PagerWidget(self.app.window.main)
        self.ui.hide()

    @register('p', modes=['normal', 'command'])
    def toggle(self): 

        self.ui.updatePosition()
        super().toggle()
