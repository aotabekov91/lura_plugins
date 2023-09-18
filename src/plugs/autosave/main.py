from plug.qt import Plug
from tables import Autosave as Table

class Autosave(Plug):

    def setup(self):

        super().setup()
        self.table=Table()
        self.setConnect()

    def setConnect(self):

        self.app.window.main.display.viewCreated.connect(
                self.on_viewCreated)
        self.app.window.main.display.positionChanged.connect(
                self.on_positionChanged)

    def on_viewCreated(self, view):

        data=self.getData(view)
        if data:
            page, left, top = data
            view.goto(page, left, top)

    def getData(self, view):

        data=self.table.getRow(
                {'hash':view.model().hash()})
        if data:
            r=data[0]
            page=r['page']
            pos=r['position'].split(':')
            left, top =float(pos[0]), float(pos[1])
            return page, left, top

    def on_positionChanged(self, view, item, left, top):

        if view.currentPage() in [0, 1]: 
            return

        data={'page': view.currentPage(), 
                'position': f'{left}:{top}'}

        vdata=self.getData(view)
        if vdata:
            hdata={'hash':view.model().hash()}
            self.table.updateRow(hdata, data)
        else:
            data['hash']=view.model().hash()
            self.table.writeRow(data, uniqueField='hash')
