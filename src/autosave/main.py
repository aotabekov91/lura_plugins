from plug.qt import Plug
from tables import Autosave as Table

class Autosave(Plug):

    def setup(self):

        self.view=None
        super().setup()
        self.table=Table()
        self.app.buffer.viewCreated.connect(
                self.setViewData)
        self.app.moder.modeChanged.connect(
                self.updateView)

    def updateView(self, mode):

        v=mode.getView()
        if v and v.check('canMove'):
            self.setView(v)

    def setView(self, v):

        self.reset()
        self.view=v
        self.updateViewData(v)
        self.reset('connect')

    def updateViewData(self, v):

        ul=v.getUniqLocator()
        if not self.table.getRow(ul):
            self.table.writeRow(ul)

    def reset(self, kind='disconnect'):

        if not self.view: return
        f=getattr(self.view.positionChanged, kind)
        f(self.saveViewData)

    def setViewData(self, v):

        l=v.getUniqLocator()
        d=self.table.getRow(l)
        if d:
            print(d)
            v.setLocator(
                    d[0], kind='position')
            self.setView(v)

    def saveViewData(self):

        ul=self.view.getUniqLocator()
        pl=self.view.getLocator(
                kind='position')
        self.table.updateRow(ul, pl)
