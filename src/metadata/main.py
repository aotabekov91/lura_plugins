from plug.qt import Plug 
from plug.utils import register
from tables import Metadata as Table
from gizmo.widget import UpDownEdit, InputList

class Metadata(Plug):

    excludeFields=['id', 'hash', 'url', 'kind']

    def __init__(
            self, 
            app, 
            *args,
            position='right',
            mode_keys={'command': 'm'},
            **kwargs):

        super().__init__(
                app=app, 
                position=position, 
                mode_keys=mode_keys,
                **kwargs,
                )

    def setup(self):

        super().setup()
        self.setUI()
        self.table=Table()
        self.setConnect()

    def setConnect(self):

        self.app.window.main.display.viewChanged.connect(
                self.update)

    def setUI(self):

        super().setUI()
        self.ui.addWidget(
                InputList(item_widget=UpDownEdit),
                'main', 
                main=True)
        self.ui.main.input.hideLabel()
        self.ui.hideWanted.connect(
                self.deactivate)
        self.ui.main.list.widgetDataChanged.connect(
                self.on_contentChanged)

    def on_contentChanged(self, widget):

        value=widget.textDown()
        dhash=widget.data['hash']
        field=widget.data['field']
        self.table.updateRow(
                {'hash':dhash}, 
                {field:value})

    def listen(self):

        super().listen()
        self.activated=True
        self.activateUI()

    def delisten(self):

        super().delisten()
        self.activated=False
        
    @register('t', modes=['command'])
    def toggle(self): super().toggle()

    def update(self, view, prev):

        view=self.app.window.main.display.view
        if view:
            dhash=view.model().hash()
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
