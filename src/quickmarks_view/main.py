from gizmo.utils import tag
from tables import Quickmark as Table
from plug.qt.plugs.render import Render
from gizmo.vimo.model import WTableModel
from gizmo.vimo.view import ListWidgetView

class QuickmarksView(Render):


    unique=True
    kind='quickmarks'
    view_prop='canLocate'
    locator_kind='position'
    model_class=WTableModel
    view_class=ListWidgetView
    view_name='QuickmarksView'
    model_prop='isQuickmarksModel'
    position={
            'QuickmarksView': 'dock_right',
            'ListWidgetView': 'dock_right',
            }

    def setup(self):

        super().setup()
        self.m_table=Table()
        self.app.moder.typeChanged.connect(
                self.setType)

    def setType(self, t):

        obj=self.checkView(t)
        if obj:
            uid=obj.getUniqLocator()
            uid['type']=self.kind
            m=self.getModel(
                    source=uid,
                    table=self.m_table)

            self.ui=self.getView(m)

    @tag('qq', modes=['command'])
    def toggle(self):
        super().toggle()
        self.setCurrentView(self.ui)

    def checkView(self, t=None):

        t = t or self.app.moder.type()
        obj=t.view()
        if obj and obj.check(self.view_prop):
            return obj
