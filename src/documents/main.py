from plug.qt import Plug 
from gizmo.utils import register
from tables import Hash, Metadata
from gizmo.widget import UpDown, InputList

class Documents(Plug):

    special=['return', 'carriage']

    def __init__(
            self, 
            app, 
            *args,
            special=special,
            position='right',
            mode_keys={'command': 'd'},
            **kwargs):

        super(Documents, self).__init__(
                app=app, 
                special=special,
                position=position, 
                mode_keys=mode_keys,
                **kwargs
                )

        self.hash=Hash()
        self.meta=Metadata()
        self.setUI()

    def setup(self):

        super().setup()
        self.setConnect()

    def setConnect(self):

        self.ear.returnPressed.connect(
                self.open)
        self.ear.carriageReturnPressed.connect(
                self.open)

    def setUI(self):

        super().setUI()
        main=InputList(item_widget=UpDown)
        self.ui.addWidget(main, 'main', main=True)
        self.ui.main.input.hideLabel()

    def activateUI(self):

       super().activateUI() 
       self.dlist=self.getList() 
       self.ui.main.setList(self.dlist)

    @register('t', modes=['command'])
    def toggle(self): super().toggle()

    def getList(self):

        data=self.hash.getAll()
        for d in data:
            d['up']=d['path'].split('/')[-1]
            meta=self.meta.getRow({'hash':d['hash']})
            if meta and meta[0]['title']:
                d['down']=meta[0]['title']
                d['up']=d['path'].split('/')[-1]
                d['up_color']='green'
        return data

    def open(self, focus=False, how='reset', hide=False):

        item=self.ui.main.list.currentItem()
        if item:
            path=self.hash.getPath(
                    item.itemData['hash'])
            print(path)
            if path: 
                self.app.window.display.open(
                        path, how=how)
        if hide: 
            self.delistenWanted.emit()

    def openAndHide(self): 

        if self.activated: 
            self.open(focus=True, hide=True)

    def openBelow(self): 

        if self.activated: 
            self.open(focus=True, how='below')

    def openBelowAndHide(self): 

        if self.activated: 
            self.open(how='below', hide=True)
