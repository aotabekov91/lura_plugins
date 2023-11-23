from gizmo.utils import tag
from tables import Quickmark as Table
from plug.qt.plugs.render import TableRender

from .utils import CreateMixin

class Quickmarks(
        CreateMixin,
        TableRender,
        ):

    table=Table()
    kind='quickmarks'
    view_prop='canLocate'
    locator_kind='position'
    view_name='QuickmarksView'
    position={
            'QuickmarksView': 'dock_right'
            }
    leader_keys={
            'command': 'q', 
            'normal|QuickmarksView': '<c-.>'
            }
    widget_map={
            'mark':{'w':'Label', 'p':'0x0x1x1'}
            }

    @tag('o', modes=['normal|QuickmarksView'])
    def open(self):
        raise
        super().open()

    @tag('d', modes=['normal|QuickmarksView'])
    def delete(self):
        raise
        super().delete()

    # @tag('f', modes=['command'])
    def focusView(self):

        self.rendering=False
        super().toggleRender()

    # @tag('t', modes=['command'])
    def toggleRender(self):
        super().toggleRender()
