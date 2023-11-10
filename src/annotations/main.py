from PyQt5 import QtGui
from plug.qt import Plug
from gizmo.utils import register
from tables import Annotation as Table
from gizmo.widget import InputList, UpDownEdit

class Annotations(Plug):

    def __init__(
            self, 
            position='dock_right',
            leader_keys={
                'command': 'a',
                'Annotations': '<c-.>'
                },
            **kwargs
            ):

        self.func_colors={}
        super().__init__(
                position=position,
                leader_keys=leader_keys,
                **kwargs)

        self.cache={}
        self.view=None
        self.setColors()
        self.table=Table()
        self.setConnect()
        self.setUI()

    def setConnect(self):

        self.app.buffer.created.connect(
                self.connectModel)
        self.app.moder.modeChanged.connect(
                self.update)
        self.app.moder.plugsLoaded.connect(
                self.setAnnotatePlug)

    def connectModel(self, m):

        c1=hasattr(m, 'loaded')
        c2=hasattr(m, 'canAnnotate')
        if c1 and c2:
            m.loaded.connect(
                    self.updateModel)

    def updateModel(self, m):

        d={'hash': m.id(), 'kind': m.kind}
        rs=self.table.getRow(d)
        for a in rs: 
            self.updateAnnotation(a)
            e=m.element(a['page'])
            e.setAnnotation(a)

    def updateAnnotation(self, a):

        f=a.get('function', 'Default')
        c=self.func_colors[f]
        a['color']=c
        a['akind']='highlight'

    def setColors(self):

        c=self.colors
        for k, v in c.items():
            n, c = v['name'], v['color']
            self.func_colors[n]=QtGui.QColor(c)

    def setUI(self):

        w=InputList(widget=UpDownEdit)
        w.returnPressed.connect(self.open)
        w.list.widgetDataChanged.connect(
                self.on_contentChanged)
        self.uiman.setUI(w)

    def setColorStyle(self, ann):

        c=ann['color'].name()
        s=f'background-color: {c}'
        ann['up_style']=s

    def update(self, m=None):

        if m and hasattr(m, 'getView'):
            v=m.getView()
            if v and v.check('canAnnotate'):
                self.setList(v)

    def setList(self, v):

        self.view=v
        if not v in self.cache:
            self.setViewAnnotations(v)
        l=self.cache.get(v, [])
        self.ui.setList(l)

    def setViewAnnotations(self, v):

        l=v.getLocator()
        if l:
            d={
              'kind':l['kind'], 
              'hash':l['hash'],
              }
            dlist=self.table.getRow(d)
            for a in dlist:
                a['view']=v
                a['down']=a['content']
                a['up']=f'# {a.get("id")}'
                self.updateAnnotation(a)
                self.setColorStyle(a)
            self.cache[v]=dlist

    @register('o')
    def open(self):

        i=self.ui.list.currentItem()
        if i:
            d=i.itemData
            v=d['view']
            v.setLocator(d)

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
            
    def setAnnotatePlug(self, plugs):

        p=plugs.get('annotate', None)
        if p:
            p.chosen.connect(self.on_chosen)
            p.removed.connect(self.on_action)
            p.annotated.connect(self.on_action)

    def on_action(self):

        self.cache.pop(self.view)
        self.setList(self.view)

    def on_chosen(self, a):

        idx=a['aid']
        d=enumerate(self.ui.list.flist)
        for j, i in d:
            if i.get('id', None)!=idx:
                continue
            self.ui.list.setCurrentRow(j)
            return

    def on_contentChanged(self, w):

        #todo
        d=w.data
        idx=d['id']
        text=w.textDown()
        self.table.updateRow(
                {'id':idx}, {'content':text})
