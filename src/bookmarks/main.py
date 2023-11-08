from plug.qt import Plug 
from gizmo.utils import register
from tables import Bookmark as Table
from gizmo.widget import UpDownEdit, InputList

class Bookmarks(Plug):

    def __init__(
            self, 
            position='dock_right',
            leader_keys={
                'command': 'b',
                'Bookmarks': '<c-.>',
                },
            **kwargs
            ):

        self.view=None
        self.color='#CC885E'
        self.table=Table()
        super().__init__(
                position=position,
                leader_keys=leader_keys,
                **kwargs) 
        self.setUI()
        self.connect()

    def connect(self):

        self.app.moder.modeChanged.connect(
                self.update)
        self.app.moder.plugsLoaded.connect(
                self.setBookmark)

    def setUI(self):

        w=InputList(widget=UpDownEdit)
        w.returnPressed.connect(self.open)
        w.list.widgetDataChanged.connect(
                self.updateContent)
        self.uiman.setUI(w)

    def setBookmark(self, p):

        bplug=p.get('bookmark', None)
        if bplug:
            s=bplug.bookmarked
            s.connect(self.update)

    @register('o')
    def open(self):

        l=self.ui.list
        i=l.currentItem()
        if i:
            d=i.itemData
            v=d['view']
            v.setLocator(d)

    @register('d')
    def delete(self):

        l=self.ui.list
        i=l.currentItem()
        crow=l.currentRow()-1
        nrow=max(0, crow) 
        idx=i.itemData['id']
        self.table.removeRow({'id':idx})
        self.setViewData(self.view)
        l.setCurrentRow(nrow)

    def setColorStyle(self, data):

        style=f'background-color: {self.color}'
        data['up_style']=style

    @register('f', modes=['command'])
    def setFocus(self):

        p=self.app.moder.plugs
        self.update(p.command.client)
        super().setFocus()

    def update(self, m=None):

        if not m or not hasattr(m, 'getView'):
            return
        v=m.getView()
        if not v.check('canPosition'):
            return
        self.view=v
        self.setViewData(v)

    def setViewData(self, v):

        l=v.getLocator()
        if l:
            c={
              'hash': l['hash'], 
              'kind': l['kind'],
              }
            rs = self.table.getRow(c)
            for r in rs:
                r['view']=v
                r['down']=r['text']
                r['up']=f'# {r.get("id")}'
                self.setColorStyle(r)
            f=lambda x: (x['page'], x['position'])
            rs=sorted(rs, key=f)
            self.ui.setList(rs)

    def updateContent(self, w):
        
        d=w.data['down']
        idx=w.data['id']
        self.table.updateRow(
                {'id': idx}, 
                {'text': d})
