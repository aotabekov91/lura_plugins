from gizmo.utils import tag
from tables import Quickmark
from gizmo.vimo.view import ListView
from plug.qt.plugs.render import Render

from .model import QuickmarkModel

class Quickmarks(Render):

    leader_keys={
        'command': 'q', 
        'normal': '<c-.>'}
    position='dock_right'
    model_class=QuickmarkModel
    model_class.kind='quickmarks'
    model_class.table=Quickmark()

    def setup(self):

        super().setup()
        ui=ListView(render=self)
        ui.__class__.__name__='QuickmarksView'
        self.app.moder.typeChanged.connect(
                self.updateType)
        self.setupView(ui)

    def getModel(self, source):

        uid=source.getUniqLocator()
        uid['type']=self.model_class.kind
        m=self.app.buffer.getModel(uid)
        if m is None: 
            l=source.getUniqLocator()
            m=self.model_class(index=l)
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
                    e.data(), kind='position')

    @tag('d', modes=['normal|Quickmarks'])
    def delete(self):

        t=self.app.moder.type()
        m=self.getModel(t.view)
        idx=self.view.currentIndex()
        if idx and m:
            m.removeRow(idx.row())

    @tag('f', modes=['command'])
    def activate(self):

        self.activated=True
        self.setView(self.view)
