from gizmo.utils import tag
from tables import Bookmark
from plug.qt.plugs.render import Render 
from gizmo.vimo.model import WTableModel
from gizmo.vimo.view import ListWidgetView 

class Bookmarks(Render):

    color='#CC885E'
    leader_keys={
        'command': 'b',
        'normal': '<c-.>'}
    kind='bookmarks'
    position='dock_right'
    vname='BookmarksView'
    model_class=WTableModel
    model_class.table=Bookmark()
    model_class.widget_map={
        'id':{'w':'Label', 'p':'0x0x1x1'},
        'text':{'w':'TextEdit', 'p':'1x0x1x1'}
        }

    def setup(self):

        super().setup()
        view=ListWidgetView(
                render=self,
                name=self.vname)
        self.app.moder.typeChanged.connect(
                self.updateType)
        self.setupView(view)

    def getModel(self, source):

        uid=source.getUniqLocator()
        uid['type']=self.kind
        m=self.app.buffer.getModel(uid)
        if m is None: 
            l=source.getUniqLocator()
            m=self.model_class(
                    index=l, 
                    kind=self.kind
                    )
            self.app.buffer.setModel(uid, m)
            m.load()
        return m

    def updateType(self, t):

        v=t.view
        if v and v.check('canLocate'):
            m=self.getModel(v)
            self.view.setModel(m)

    @tag('f', modes=['command'])
    def activate(self):
        self.setView(self.view)

    @tag('o', modes=['normal|Bookmarks'])
    def open(self):

        i=self.view.currentItem()
        t=self.app.moder.type()
        if i and t.view:
            e=i.element()
            t.view.openLocator(
                    e.data(), kind='position')

    @tag('d', modes=['normal|Bookmarks'])
    def delete(self):

        t=self.app.moder.type()
        m=self.getModel(t.view)
        item=self.view.currentItem()
        if item and m:
            e=item.element()
            m.removeElement(e)
