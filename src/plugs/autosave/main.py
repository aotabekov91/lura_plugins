from tables import Autosave as Table

from plug.qt import PlugObj

class Autosave(PlugObj):

    def __init__(self, app, **kwargs):

        super(Autosave, self).__init__(
                app=app,
                **kwargs,
                )

        self.table=Table()
        app.window.main.display.viewCreated.connect(
                self.on_viewCreated)
        app.window.main.display.positionChanged.connect(
                self.on_positionChanged)

    def on_viewCreated(self, view):

        row=self.table.getRow(
                {'hash':view.model().hash()})
        if row:
            r=row[0]
            page=r['page']
            pos=r['position'].split(':')
            left, top =float(pos[0]), float(pos[1])
            view.goto(page, left, top)

    def on_positionChanged(self, view, item, left, top):

        if view.currentPage() in [0, 1]: return

        data={'page': view.currentPage(), 
                'position': f'{left}:{top}'}

        if self.table.getRow({'hash':view.model().hash()}):
            self.table.updateRow({'hash': view.model().hash()}, data)
        else:
            data['hash']=view.model().hash()
            self.table.writeRow(data, uniqueField='hash')
