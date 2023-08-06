from qapp.plug import PlugObj
from qapp.utils import register

from .widget import OverlayedWidget

class Pager(PlugObj):

    def __init__(self, **kwargs):

        super().__init__(position='overlay', **kwargs)

        self.setUI()
        self.app.main.display.itemChanged.connect(
                self.on_itemChanged
                )
        self.app.main.display.viewChanged.connect(
                self.on_itemChanged
                )

    def on_viewChanged(self, view): self.on_itemChanged(view) 

    def on_itemChanged(self, view, item=None): 

        cpage=view.currentPage()
        pages=view.totalPages()
        self.ui.setText(f'{cpage}/{pages}')

    def setUI(self):

        self.ui=OverlayedWidget(self.app.main)
        self.ui.hide()

    @register('p', modes=['normal', 'command'])
    def toggle(self): super().toggle()


