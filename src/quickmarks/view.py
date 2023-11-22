from gizmo.utils import tag
from tables import Quickmark as Table
from plug.qt.plugs.render import Render

class QuickmarksView(Render):

    unique=True
    kind='quickmarks'
    view_prop='canLocate'
    locator_kind='position'
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
            self.setCurrentView(v)

    def getModel(self, obj):

        uid=obj.getUniqLocator()
        uid['type']=self.kind
        b=self.app.buffer
        return b.getModel(uid)

    def checkView(self, t=None):

        t = t or self.app.moder.type()
        obj=t.view()
        if obj and obj.check(self.view_prop):
            return obj
