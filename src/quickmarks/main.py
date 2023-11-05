from plug.qt import Plug 
from gizmo.utils import register
from tables import Quickmark as Table
from gizmo.widget import UpDownEdit, InputList

class Quickmarks(Plug):

    def __init__(
            self, 
            app, 
            position='dock_right',
            leader_keys={
                'command': 'M',
                'Quickmarks': '<c-.>',
                },
            **kwargs):

        self.current=None
        self.table=Table()
        super().__init__(
                app=app, 
                position=position,
                leader_keys=leader_keys,
                **kwargs) 
        self.setUI()
        self.connect()

    def connect(self):

        self.app.moder.modeChanged.connect(
                self.update)
        self.app.moder.plugsLoaded.connect(
                self.on_plugsLoaded)

    def on_plugsLoaded(self, plugs):

        p=plugs.get('quickmark', None)
        if p: 
            p.marked.connect(self.update)
            p.unmarked.connect(self.update)

    def setUI(self):

        w=InputList(widget=UpDownEdit)
        w.returnPressed.connect(self.open)
        self.uiman.setUI(w)

    @register('f', modes=['command'])
    def setFocus(self):

        p=self.app.moder.plugs
        self.update(p.command.client)
        super().setFocus()

    @register('o')
    def open(self):

        i=self.ui.list.currentItem()
        if i: 
            d=i.itemData
            v=d['view']
            v.open(**d)

    @register('d')
    def delete(self):
        raise

        item=self.ui.list.currentItem()
        nrow=self.ui.list.currentRow()-1
        bid=item.itemData['id']
        self.table.removeRow({'id':bid})
        self.update()
        self.ui.list.setCurrentRow(nrow)

    def update(self, mode=None):

        if mode==self:
            return
        if not mode:
            mode=self.app.moder.current
        gv=getattr(mode, 'getView', None)
        if not gv: 
            return
        v=gv()
        if not v or v==self.current:
            return
        self.current=v
        cond={
              'kind': v.kind(),
              'hash': v.modelId(),
             }
        rs = self.table.getRow(cond)
        for r in rs:
            r['view']=v
            r['up']=r['mark']
        rs=sorted(
                rs, key=lambda x: x['position'])
        self.ui.setList(rs)
