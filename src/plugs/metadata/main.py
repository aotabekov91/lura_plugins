from qapp.plug import PlugObj 
from qapp.utils import register
from qapp.widget import UpDownEdit, InputList

class Metadata(PlugObj):

    excludeFields=['id', 'hash', 'url', 'kind']

    def __init__(self, app):

        super().__init__(app=app, 
                         position='right', 
                         mode_keys={'command': 'm'})

        self.setUI()

    def setUI(self):

        super().setUI()

        main=InputList(item_widget=UpDownEdit)
        self.ui.addWidget(main, 'main', main=True)
        self.ui.main.input.hideLabel()
        self.ui.hideWanted.connect(self.deactivate)

        self.ui.main.list.widgetDataChanged.connect(self.on_contentChanged)

        self.ui.installEventFilter(self)

    def on_contentChanged(self, widget):

        value=widget.textDown()
        dhash=widget.data['hash']
        field=widget.data['field']
        self.app.tables.metadata.updateRow({'hash':dhash}, {field:value})

    def activate(self):

        super().activate()
        self.update()
        self.app.main.display.viewChanged.connect(self.update)

    def deactivate(self):

        super().deactivate()
        self.app.main.display.viewChanged.disconnect(self.update)

    @register('t', modes=['command'])
    def toggle(self): super().toggle()

    def update(self):

        view=self.app.main.display.view
        if view and view.model():

            dhash=view.model().hash()
            meta=self.app.tables.metadata.getRow({'hash':dhash})
            if meta:
                dlist=[]
                for f, v in meta[0].items():
                    if f in self.excludeFields: continue
                    data={'up':f.title(), 'down':v, 'hash':dhash, 'field':f}
                    data['up_color']='green'
                    dlist+=[data]
                self.ui.main.setList(dlist)
                text=self.ui.main.input.text()
                if text: self.ui.main.list.filter(text)
            else:
                self.app.tables.metadata.writeRow({'hash':dhash})
                self.update()
