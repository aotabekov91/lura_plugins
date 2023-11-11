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

        self.cache={}
        self.view=None
        self.table=Table()
        self.func_colors={}
        super().__init__(
                position=position,
                leader_keys=leader_keys,
                **kwargs)
        self.setConnect()
        self.setColors()
        self.setUI()

    def setConnect(self):

        self.app.buffer.created.connect(
                self.connectModel)
        self.app.moder.modeChanged.connect(
                self.updateList)
        self.app.moder.plugsLoaded.connect(
                self.setAnnotatePlug)

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

    def connectModel(self, m):

        c1=hasattr(m, 'loaded')
        c2=hasattr(m, 'canAnnotate')
        if c1 and c2:
            m.loaded.connect(self.updateModel)

    def updateModel(self, model):

        l=model.getUniqLocator(kind='annotation')
        data=self.table.getRow(l)
        for d in data: 
            self.updateAnnData(d, model)
            model.setLocator(
                    data=d, 
                    kind='annotation')

    def updateList(self, mode=None):

        if mode and hasattr(mode, 'getView'):
            v=mode.getView()
            if v and v.check('canAnnotate'):
                self.setList(v)

    def setList(self, v):

        if not v in self.cache:
            self.cacheAnnotations(v)
        l=self.cache.get(v, [])
        self.ui.setList(l)
        self.view=v

    def cacheAnnotations(self, v):

        m=v.model()
        l=m.getUniqLocator(kind='annotation')
        if l:
            data=self.table.getRow(l)
            self.cache[v]=data
            for d in data:
                self.updateAnnData(d, m)
                self.updateAnnViewData(d, v)

    def updateAnnData(self, d, m):

        f=d.get('function', 'Default')
        c=self.func_colors[f]
        d['color']=c
        d['akind']='highlight'
        d['down']=d['content']
        d['box']=m.getAnnBox(d)
        d['up']=f'# {d.get("id")}'
        d['element']=m.getAnnElement(d)
        d['up_style']=f'background-color: {c.name()}'

    def updateAnnViewData(self, d, v):

        i=v.item(element=d['element'])
        d['view']=v
        d['item']=i

    @register('o')
    def open(self):

        i=self.ui.list.currentItem()
        if not i: return
        data=i.itemData
        v=data['view']
        v.setLocator(
                data=data, 
                kind='annotation')

    @register('d')
    def delete(self):

        i=self.ui.list.currentItem()
        if not i: return
        d=i.itemData
        v=i.itemData['view']
        cr=max(self.ui.list.currentRow()-1, 0)
        loc=self.view.delLocator(
                data=d, kind='annotation')
        self.table.removeRow(loc)
        self.cacheAnnotations(v)
        self.setList(v)
        self.ui.list.setCurrentRow(cr)

    def setAnnotatePlug(self, plugs):

        p=plugs.get('annotate', None)
        if p:
            p.chosen.connect(self.on_viewAnnChosen)
            p.removed.connect(self.on_viewAnnChanged)
            p.annotated.connect(self.on_viewAnnChanged)

    def on_viewAnnChanged(self):

        self.cache.pop(self.view)
        self.setList(self.view)

    def on_viewAnnChosen(self, a):

        idx=a['aid']
        d=enumerate(self.ui.list.flist)
        for j, i in d:
            if i.get('id', None)!=idx:
                continue
            self.ui.list.setCurrentRow(j)
            return i

    def on_contentChanged(self, w):

        #todo
        d=w.data
        idx=d['id']
        text=w.textDown()
        self.table.updateRow(
                {'id':idx}, {'content':text})
