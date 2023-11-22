from gizmo.utils import tag
from tables import Bookmark as Table
from plug.qt.plugs.render import TableRender 

class Bookmarks(TableRender):

    leader_keys={
        'command': 'b',
        'normal': '<c-.>'}
    table=Table()
    color='#CC885E'
    kind='bookmarks'
    position='dock_right'
    view_name='BookmarksView'
    widget_map={
        'id':{'w':'Label', 'p':'0x0x1x1'},
        'text':{'w':'TextEdit', 'p':'1x0x1x1'}
        }

    @tag('f', modes=['command'])
    def activate(self):
        super().activate()

    @tag('o', modes=['normal|Bookmarks'])
    def open(self):
        super().open()

    @tag('d', modes=['normal|Bookmarks'])
    def delete(self):
        super().delete()
