from gizmo.utils import tag
from tables import Quickmark
from plug.qt.plugs import render
from gizmo.vimo import view, model

class Quickmarks(render.Render):

    leader_keys={
        'command': 'q',
        'Quickmarks': '<c-.>'}
    position='dock_right'
    model_class=model.StandardTableModel
    model_class.kind='quickmarks'
    model_class.table=Quickmark()

    def setup(self):

        super().setup()
        self.client=None
        ui=view.ListView()
        ui.__name__='QuickmarkView'
        self.app.moder.typeChanged.connect(
                self.updateView)
        self.app.uiman.setUI(self, ui)
        self.view=ui

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

    def updateView(self, v):

        if v.check('canLocate'):
            self.client=v
            m=self.getModel(v)
            self.view.setModel(m)

    @tag('o', modes=['normal|QuickmarkView'])
    def open(self):

        i=self.view.currentItem()
        v=self.app.moder.type()
        if i and self.client:
            e=i.element()
            self.client.openLocator(
                    e.data(),
                    kind='position')

    @tag('d', modes=['normal|QuickmarkView'])
    def delete(self):

        idx=self.view.currentIndex()
        m=self.view.model()
        m.removeRow(idx.row())

    @tag('f', modes=['command'])
    def activate(self):

        m=self.app.moder
        self.setView(self.view)
        m.typeWanted.emit(self.view)
