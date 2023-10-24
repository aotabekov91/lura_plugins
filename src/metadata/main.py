from plug.qt import Plug 
from tables import Metadata as Table
from gizmo.widget import UpDownEdit, InputList

class Metadata(Plug):

    excludeFields=['id', 'hash', 'url', 'kind']

    def __init__(
            self, 
            app, 
            *args,
            position='right',
            prefix_keys={'command': 'm'},
            **kwargs):

        self.table=Table()
        super().__init__(
                app=app, 
                position=position, 
                prefix_keys=prefix_keys,
                **kwargs,
                )

    def setup(self):

        super().setup()
        self.setUI()
        self.setConnect()

    def setConnect(self):

        self.app.display.viewChanged.connect(
                self.update)

    def setUI(self):

        self.uiman.setUI()
        main=InputList(
                widget=UpDownEdit)
        main.input.hideLabel()
        main.list.widgetDataChanged.connect(
                self.on_contentChanged)
        self.ui.addWidget(
                main, 'main', main=True)
        self.ui.hideWanted.connect(
                self.deactivate)

    def on_contentChanged(self, widget):

        value=widget.textDown()
        dhash=widget.data['hash']
        field=widget.data['field']
        idx={'hash':dhash}
        val={field:value}
        self.table.updateRow(idx, val)

    def update(self, view, prev):

        view=self.app.display.view
        if view:
            dhash=view.model().id()
            meta=self.table.getRow({'hash':dhash})
            if meta:
                dlist=[]
                for f, v in meta[0].items():
                    if not f in self.excludeFields: 
                        dlist+=[{
                            'up':f.title(), 
                            'down':v, 
                            'hash':dhash, 
                            'field':f
                            }]
                self.ui.main.setList(dlist)
                text=self.ui.main.input.text()
                if text: 
                    self.ui.main.list.filter(text)
            else:
                self.table.writeRow({'hash':dhash})
                self.update(view, prev)
