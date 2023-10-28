from plug.qt import Plug 
from gizmo.utils import register
from tables import Bookmark as Table
from gizmo.widget import UpDownEdit, InputList

class Bookmarks(Plug):

    def __init__(
            self, 
            app, 
            position='dock_right',
            prefix_keys={
                'command': 'b',
                'Bookmarks': '<c-.>',
                },
            **kwargs):

        self.current=None
        self.color='#CC885E'
        self.table=Table()
        self.display=app.display
        super().__init__(
                app=app, 
                position=position,
                prefix_keys=prefix_keys,
                **kwargs) 
        self.setUI()
        self.connect()

    def connect(self):

        self.app.moder.modeChanged.connect(
                self.update)
        self.app.moder.plugsLoaded.connect(
                self.on_plugsLoaded)

    def on_plugsLoaded(self, plugs):

        b=plugs.get('bookmark', None)
        if b: 
            b.bookmarked.connect(self.update)

    def setUI(self):

        w=InputList(widget=UpDownEdit)
        w.returnPressed.connect(self.open)
        w.list.widgetDataChanged.connect(
                self.on_contentChanged)
        self.uiman.setUI(w)

    @register('o')
    def open(self):

        i=self.ui.list.currentItem()
        if i: 
            d=i.itemData
            v=d['view']
            v.open(**d)

    @register('d')
    def delete(self):

        crow=self.ui.list.currentRow()-1
        nrow=max(0, crow) 
        i=self.ui.list.currentItem()
        bid=i.itemData['id']
        self.table.removeRow({'id':bid})
        self.update()
        self.ui.list.setCurrentRow(nrow)

    def setColorStyle(self, ann):

        style=f'background-color: {self.color}'
        ann['up_style']=style

    @register('f', modes=['command'])
    def setFocus(self):

        p=self.app.moder.plugs
        self.update(p.command.client)
        super().setFocus()

    def update(self, mode=None):

        if mode==self:
            return
        if not mode:
            mode, _ =self.app.moder.getState()
        gv=getattr(mode, 'getView', None)
        if not gv: 
            return
        v=gv()
        if not v or v==self.current:
            return
        k=v.kind()
        i=v.modelId()
        self.current=v
        c={'hash': i, 'kind': k}
        rs = self.table.getRow(c)
        for r in rs:
            r['view']=v
            r['down']=r['text']
            r['up']=f'# {r.get("id")}'
            self.setColorStyle(r)
        sfunc=lambda x: (x['page'], x['position'])
        rs=sorted(rs, key=sfunc)
        self.ui.setList(rs)

    def on_contentChanged(self, w):
        
        xid=w.data['id']
        tdata=w.data['down']
        self.table.updateRow(
                {'id': xid},
                {'text': tdata})
