from PyQt5 import QtGui
from plug.qt import Plug
from gizmo.utils import register
from tables import Annotation as Table
from gizmo.widget import InputList, UpDownEdit

class Annotations(Plug):

    def __init__(
            self, 
            app, 
            position='dock_right',
            prefix_keys={
                'command': 'a',
                'Annotations': '<c-.>'
                },
            **kwargs
            ):

        self.current=None
        self.table=Table()
        super().__init__(
                app=app, 
                position=position,
                prefix_keys=prefix_keys,
                **kwargs)
        self.setUI()
        self.connect()

    def connect(self):

        self.display=self.app.display
        self.app.moder.modeChanged.connect(
                self.update)
        self.app.moder.plugsLoaded.connect(
                self.on_plugsLoaded)

    def setUI(self):

        w=InputList(widget=UpDownEdit)
        w.returnPressed.connect(self.open)
        w.list.widgetDataChanged.connect(
                self.on_contentChanged)
        self.uiman.setUI(w)

    def setColorStyle(self, ann):

        color=ann['color'].name()
        style=f'background-color: {color}'
        ann['up_style']=style

    def getCompatibleView(self, mode):

        gv=getattr(mode, 'getView', None)
        if not gv:
            return
        v=gv()
        if not v:
            return
        m=v.model()
        if hasattr(m, 'annotations'):
            return v

    def update(self, m=None, v=None, force=False):

        if not v:
            v=self.getCompatibleView(m)
        if not v:
            return
        if self.current==v and not force:
            return
        self.current=v
        m=v.model()
        anns=m.annotations()
        for a in anns:
            a['view']=v
            a['down']=a['content']
            if a['type']=='native':
                a['up']='Native'
                a['down']=a['text']
                a['up_color']=a['color'] 
            else:
                a['up']=f'# {a.get("id")}'
                self.setColorStyle(a)
        self.ui.setList(anns)

    @register('o')
    def open(self):

        i=self.ui.list.currentItem()
        if i:
            d=i.itemData
            v=d['view']
            v.open(**d)

    @register('d')
    def delete(self):

        i=self.ui.list.currentItem()
        cr=self.ui.list.currentRow()
        nr=max(cr-1, 0)
        if i:
            d=i.itemData
            v=d['view']
            idx=d.get('page')
            aid=d.get('id', None)
            self.table.removeRow(
                    {'id': aid})
            i=v.item(idx)
            e=v.element(idx)
            e.removeAnnotation(d)
            i.refresh(dropCache=True)
            self.update(v=v)
            self.ui.list.setCurrentRow(nr)
            
    def on_plugsLoaded(self, plugs):

        aplug=plugs.get(
                'annotate', None)
        if aplug:
            aplug.removed.connect(
                    self.on_action)
            aplug.annotated.connect(
                    self.on_action)
            aplug.chosen.connect(
                    self.on_chosen)

    def on_action(self):
        self.update(v=self.current, force=True)

    def on_chosen(self, a):

        idx=a['aid']
        d=enumerate(self.ui.list.flist)
        for j, i in d:
            if i.get('id', None)!=idx:
                continue
            self.ui.list.setCurrentRow(j)
            return

    def on_contentChanged(self, w):

        d=w.data
        idx=d['id']
        text=w.textDown()
        print(idx, text)
        self.table.updateRow(
                {'id':idx}, 
                {'content':text})
