from plug.qt import Plug 
from tables import Metadata as Table
from gizmo.widget import UpDownEdit, InputList

class Metadata(Plug):

    position='dock_right'
    leader_keys={'command': 'm'}
    exclude=['id', 'hash', 'url', 'kind']

    def setup(self):

        super().setup()
        self.setupUI()
        self.cache={}
        self.table=Table()
        self.app.moder.modeChanged.connect(
                self.updateData)

    def setupUI(self):

        w=InputList(widget=UpDownEdit)
        w.input.hideLabel()
        w.list.widgetDataChanged.connect(
                self.updateContent)
        self.app.uiman.setupUI(self, w)

    def updateData(self, m):

        if self.checkProp('hasView', m):
            v=m.getView()
            self.view=v
            self.checkRowExists(v)
            self.setViewMetadata(v)
            self.setFilter()

    def checkRowExists(self, v):

        l=v.getUniqLocator()
        rs=self.table.getRow(l)
        if not rs:
            self.table.writeRow(l)
            return self.table.getRow(l)

    def setFilter(self):

        t=self.ui.input.text()
        if t: self.ui.list.filter(t)

    def setViewMetadata(self, v):

        if v in self.cache:
            data=self.cache[v]
        else:
            data, r = [], {}
            l=v.getUniqLocator()
            rs=self.table.getRow(l)
            if rs: r=rs[0]
            for f, j in r.items():
                if f in self.exclude: 
                    continue
                data+=[{
                    'field':f,
                    'view': v,
                    'down': j,
                    'up':f.title()
                    }]
            self.cache[v]=data
        self.ui.setList(data)

    def updateContent(self, w):

        l=self.view.getUniqLocator()
        d={w.data['field']:w.textDown()}
        self.table.updateRow(l, d)
