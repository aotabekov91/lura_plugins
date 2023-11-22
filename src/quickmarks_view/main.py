from gizmo.utils import tag
from tables import Quickmark as Table
from plug.qt.plugs.render import Render
from gizmo.vimo.view import ListWidgetView

class QuickmarksView(Render):

    unique=True
    kind='quickmarks'
    view_prop='canLocate'
    locator_kind='position'
    view_class=ListWidgetView
    view_name='QuickmarksView'
    model_prop='isQuickmarksModel'
    position={
            'QuickmarksView': 'dock_right'
            }

    def setup(self):

        super().setup()
        self.app.moder.typeChanged.connect(
                self.setType)

    def setType(self, t):

        obj=self.checkView(t)
        if obj:
            m=self.getModel(obj)
            v=self.getView(m)
            return v

    @tag('qq', modes=['command'])
    def toggle(self):
        super().toggle()

    def getModel(self, obj):

        uid=obj.getUniqLocator()
        uid['type']=self.kind
        return self.app.buffer.getModel(uid)

    def checkView(self, t=None):

        t = t or self.app.moder.type()
        obj=t.view()
        if obj and obj.check(self.view_prop):
            return obj
