from plug.qt import Plug 
from gizmo.utils import tag
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

        self.cache={}
        self.view=None
        self.color='#CC885E'
        self.table=Table()
        super().__init__(
                position=position,
                leader_keys=leader_keys,
                **kwargs) 
        self.app.moder.modeChanged.connect(
                self.updateViewBookmarks)
        self.app.moder.plugsLoaded.connect(
                self.setBookmarkPlug)
        self.setUI()

    def setUI(self):

        w=InputList(widget=UpDownEdit)
        w.returnPressed.connect(
                self.openBookmark)
        w.list.widgetDataChanged.connect(
                self.updateContent)
        self.app.uiman.setUI(self, w)

    def setBookmarkPlug(self, plugs):

        p=plugs.get('bookmark', None)
        if p:
            p.bookmarked.connect(
                    self.resetViewBookmarks)

    def resetViewBookmarks(self):

        if self.view:
            self.cache.pop(self.view, None)
            self.setViewBookmarks(self.view)

    @tag('o')
    def openBookmark(self):

        l=self.ui.list
        i=l.currentItem()
        if i:
            v=i.itemData['view']
            v.openLocator(
                    i.itemData, kind='position')

    @tag('d')
    def delete(self):

        l=self.ui.list
        i=l.currentItem()
        cr=max(0, l.currentRow()-1)
        idx=i.itemData['id']
        self.table.removeRow({'id':idx})
        self.resetViewBookmarks()
        l.setCurrentRow(cr)

    @tag('f', modes=['command'])
    def setFocus(self):

        p=self.app.moder.plugs
        self.updateViewBookmarks(
                p.command.client)
        super().setFocus()

    def updateViewBookmarks(self, mode):

        v=mode.getView()
        if v and v.check('canPosition'):
            self.setViewBookmarks(v)
            self.view=v

    def setViewBookmarks(self, v):

        if v in self.cache:
            data=self.cache[v]
        else:
            data=[]
            l=v.getUniqLocator()
            if l:
                data = self.table.getRow(l)
                for r in data:
                    r['view']=v
                    r['down']=r['text']
                    r['up']=f'# {r.get("id")}'
                    self.setColorStyle(r)
                self.cache[v]=data
        self.ui.setList(data)

    def setColorStyle(self, d):

        style=f'background-color: {self.color}'
        d['up_style']=style

    def updateContent(self, w):
        
        self.table.updateRow(
                {'id': w.data['id']}, 
                {'text': w.data['down']})
