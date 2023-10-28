from plug.qt import Plug
from tables import Autosave as Table

class Autosave(Plug):

    def setup(self):

        super().setup()
        self.table=Table()
        self.setConnect()

    def setConnect(self):

        self.app.display.viewCreated.connect(
                self.on_viewCreated)
        self.app.display.positionChanged.connect(
                self.save)

    def on_viewCreated(self, view):

        d=self.get(view)
        if d:
            idx, x, y = d
            # view.goto(idx, x, y)

    def get(self, view):

        data=self.table.getRow(
                {'hash':view.model().id()})
        if data:
            r=data[0]
            page=int(r['page'])
            pos=r['position'].split(':')
            left, top =float(pos[0]), float(pos[1])
            return page, left, top

    def save(
            self, 
            view, 
            item, 
            left, 
            top
            ):

        top, left=str(top), str(left)
        idx=view.currentItem().index()
        data={
             'page': idx,
             'position': f'{left}:{top}',
             }
        vdata=self.get(view)
        if vdata:
            idx=view.model().id()
            self.table.updateRow(
                    {'hash':idx}, data)
        else:
            data['hash']=view.model().id()
            self.table.writeRow(
                    data, uniqueField='hash')
