from plug.qt import Plug 
from gizmo.utils import register
from tables import Quickmark as Table
from gizmo.widget import UpDownEdit, InputList

class Quickmarks(Plug):

    def __init__(
            self, 
            position='dock_right',
            leader_keys={
                'command': 'M',
                'Quickmarks': '<c-.>',
                },
            **kwargs):

        self.cache={}
        self.view=None
        self.table=Table()
        super().__init__(
                position=position,
                leader_keys=leader_keys,
                **kwargs) 
        self.app.moder.modeChanged.connect(
                self.updateViewMarks)
        self.app.moder.plugsLoaded.connect(
                self.setQuickmarkPlug)
        self.setUI()

    def setUI(self):

        w=InputList(widget=UpDownEdit)
        w.returnPressed.connect(self.open)
        self.uiman.setUI(w)

    def setQuickmarkPlug(self, plugs):

        p=plugs.get('quickmark', None)
        if p: 
            p.marked.connect(self.resetViewMarks)
            p.unmarked.connect(self.resetViewMarks)

    def resetViewMarks(self, v=None):

        v=v or self.view
        self.cache.pop(v, None)
        self.setViewMarks(v)

    @register('f', modes=['command'])
    def setFocus(self):

        p=self.app.moder.plugs
        self.updateViewMarks(
                p.command.client)
        super().setFocus()

    @register('o')
    def open(self):

        i=self.ui.list.currentItem()
        if i: 
            v=i.itemData['view']
            v.openLocator(
                    i.itemData, 
                    kind='position')

    @register('d')
    def delete(self):

        i=self.ui.list.currentItem()
        cr=max(self.ui.list.currentRow()-1, 0)
        idx=i.itemData['id']
        self.table.removeRow({'id':idx})
        self.resetViewMarks()
        self.ui.list.setCurrentRow(cr)

    def setViewMarks(self, v):

        if v in self.cache:
            data=self.cache[v]
        else:
            data=[]
            l=v.getUniqLocator()
            if l:
                data = self.table.getRow(l)
                for r in data:
                    r['view']=v
                    r['up']=r['mark']
                self.cache[v]=data
        self.ui.setList(data)

    def updateViewMarks(self, mode):

        v=mode.getView()
        if v and v.check('canPosition'):
            self.setViewMarks(v)
            self.view=v
