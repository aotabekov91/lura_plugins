from gizmo.utils import tag
from tables import Quickmark
from plug.qt.plugs.render import Render
from gizmo.vimo.model import WTableModel
from gizmo.vimo.view import ListWidgetView

class Quickmarks(Render):

    leader_keys={
        'command': 'q', 
        'normal': '<c-.>'}
    kind='quickmarks'
    position='dock_right'
    vname='QuickmarksView'
    model_class=WTableModel
    model_class.table=Quickmark()
    model_class.widget_map={
        'mark':{'w':'Label', 'p':'0x0x1x1'},
        }

    def setup(self):

        super().setup()
        view=ListWidgetView(
                render=self, name=self.vname)
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
                    index=l, kind=self.kind)
            self.app.buffer.setModel(uid, m)
            m.load()
        return m

    def updateType(self, t):

        v=t.view
        if v and v.check('canLocate'):
            m=self.getModel(v)
            self.view.setModel(m)

    @tag('o', modes=['normal|Quickmarks'])
    def open(self):

        i=self.view.currentItem()
        t=self.app.moder.type()
        if i and t.view:
            e=i.element()
            t.view.openLocator(
                    e.data(), 
                    kind='position')

    @tag('d', modes=['normal|Quickmarks'])
    def delete(self):

        t=self.app.moder.type()
        m=self.getModel(t.view)
        item=self.view.currentItem()
        if item and m:
            e=item.element()
            m.removeElement(e)

    @tag('f', modes=['command'])
    def activate(self):

        self.activated=True
        self.setView(self.view)
