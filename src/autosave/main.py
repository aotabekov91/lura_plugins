from plug.qt import Plug
from tables import Autosave as Table

class Autosave(Plug):

    table=Table()

    def setup(self):

        self.view=None
        super().setup()
        self.app.buffer.viewCreated.connect(
                self.setViewData)
        self.app.handler.viewChanged.connect(
                self.updateView)

    def setViewData(self, v):

        if self.checkProp('canLocate', v):
            l=v.getUniqLocator()
            d=self.table.getRow(l)
            if not d: return
            v.setLocator(d[0], kind='position')

    def updateView(self, v):

        if self.checkProp('canLocate', v):
            self.setView(v)

    def setView(self, v):

        self.reconnect('disconnect')
        self.view=v
        self.reconnect()

    def reconnect(self, kind='connect'):

        v = self.view
        if not v: return
        f=getattr(v.positionChanged, kind)
        f(self.saveState)

    def saveState(self):

        l=self.view.getUniqLocator()
        p=self.view.getLocator(
                kind='position', data=l)
        self.table.writeRow(l)
