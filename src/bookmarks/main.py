from plug.qt import Plug 
from gizmo.utils import register
from tables import Bookmark as Table
from gizmo.widget import UpDownEdit, InputList

class Bookmarks(Plug):

    def __init__(
            self, 
            app, 
            position='right',
            prefix_keys={
                'command': 'B',
                'Bookmarks': '<c-.>',
                },
            **kwargs):

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

        self.display.viewChanged.connect(
                self.update)
        self.app.moder.plugsLoaded.connect(
                self.on_plugsLoaded)

    def on_plugsLoaded(self, plugs):

        self.bookmark=plugs.get(
                'bookmark', None)
        if self.bookmark:
            self.bookmark.marked.connect(
                    self.update)

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
            p=i.itemData['page']
            l, t=i.itemData['pos']
            view=i.itemData['view']
            view.goto(p, l, t)

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

    def update(self):

        view=self.display.currentView()
        if view:
            dhash=view.model().id()
            cond={'hash': dhash}
            rows = self.table.getRow(cond)
            print(cond, rows)
            for a in rows:
                p=a['position'].split(':')
                a['view']=view
                a['down']=a['text']
                a['up']=f'# {a.get("id")}'
                a['pos']=float(p[0]), float(p[0])
                self.setColorStyle(a)
            rows=sorted(
                    rows, 
                    key=lambda x: (x['page'], x['position'])
                    )
            self.ui.setList(rows)

    def on_contentChanged(self, w):
        
        xid=w.data['id']
        tdata=w.data['down']
        self.table.updateRow(
                {'id': xid},
                {'text': tdata})
