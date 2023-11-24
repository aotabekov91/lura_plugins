from plug.qt import Plug 
from PyQt5.QtCore import Qt
from gizmo.utils import tag
from tables import Hash, Metadata
from gizmo.widget import UpDown, InputList

class Documents(Plug):

    position='dock_right'
    prefix_keys={'command': 'd'}

    def setup(self):

        super().setup()
        self.meta=Metadata()
        self.hash=Hash()
        self.setupUI()

    def event_functor(self, e, ear):

        enter=[Qt.Return, Qt.Enter]
        if e.key() in enter: 
            self.open()
            ear.clearKeys()
            return True

    def setupUI(self):

        self.app.uiman.setupUI(self)
        w=InputList(widget=UpDown)
        self.ui.addWidget(
                w, 'main', main=True)
        self.ui.main.input.hideLabel()

    def activateUI(self):

       super().activateUI() 
       self.dlist=self.getList() 
       self.ui.main.setList(self.dlist)

    @tag('t', modes=['command'])
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
            if path: 
                self.app.ui.display.open(
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
