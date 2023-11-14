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
        self.app.buffer.modelCreated.connect(
                self.connectModel)
        self.app.moder.modeChanged.connect(
                self.updateViewAnnotations)
        self.app.moder.plugsLoaded.connect(
                self.setAnnotatePlug)
        self.setColors()
        self.setUI()

    def setColors(self):

        c=self.colors
        for k, v in c.items():
            n, c = v['name'], v['color']
            self.func_colors[n]=QtGui.QColor(c)

    def setUI(self):

        w=InputList(widget=UpDownEdit)
        w.returnPressed.connect(self.open)
        w.list.widgetDataChanged.connect(
                self.updateContent)
        self.uiman.setUI(w)

    def connectModel(self, m):

        c1=hasattr(m, 'loaded')
        c2=hasattr(m, 'canAnnotate')
        if c1 and c2:
            m.loaded.connect(self.annotateModel)

    def annotateModel(self, model):

        l=model.getUniqLocator(
                kind='annotation')
        data=self.table.getRow(l)
        for d in data: 
            self.updateAnnData(
                    d, model=model)
            model.setLocator(
                    data=d, kind='annotation')

    def updateViewAnnotations(self, mode):

        v=mode.getView()
        if v and v.check('canAnnotate'):
            self.setViewAnnotations(v)
            self.view=v

    def setViewAnnotations(self, v):

        if v in self.cache:
            data=self.cache[v]
        else:
            data=[]
            l=v.getUniqLocator()
            if l:
                data=self.table.getRow(l)
                self.cache[v]=data
                for d in data:
                    self.updateAnnData(
                            d, view=v)
        self.ui.setList(data)

    def updateAnnData(self, d, view=None, model=None):

        if view:
            model=view.model()
        f=d.get('function', 'Default')
        elem=model.getAnnElement(d)
        c=self.func_colors[f]
        d['color']=c
        d['element']=elem
        d['akind']='highlight'
        d['down']=d['content']
        d['box']=model.getAnnBox(d)
        d['up']=f'# {d.get("id")}'
        d['up_style']=f'background-color: {c.name()}'
        if view:
            d['view']=view
            d['item']=view.item(element=elem)


    @register('o')
    def open(self):

        i=self.ui.list.currentItem()
        if i:
            v=i.itemData['view']
            v.openLocator(
                    i.itemData, 
                    kind='annotation')

    @register('d')
    def delete(self):

        i=self.ui.list.currentItem()
        if not i: return
        d=i.itemData
        v=d['view']
        cr=max(self.ui.list.currentRow()-1, 0)
        l=self.view.delLocator(
                data=d, kind='annotation')
        self.table.removeRow(l)
        self.resetViewAnnotations(v)
        self.ui.list.setCurrentRow(cr)

    def setAnnotatePlug(self, plugs):

        p=plugs.get('annotate', None)
        if p:
            p.chosen.connect(self.on_viewAnnChosen)
            p.removed.connect(self.resetViewAnnotations)
            p.annotated.connect(self.resetViewAnnotations)

    def resetViewAnnotations(self, v=None):

        v=v or self.view
        self.cache.pop(v, None)
        self.setViewAnnotations(v)

    def on_viewAnnChosen(self, d):

        l=enumerate(self.ui.list.flist)
        for j, i in l:
            if i.get('id', None)!=d['id']:
                continue
            self.ui.list.setCurrentRow(j)
            return i

    def updateContent(self, w):

        idx=w.data['id']
        text=w.textDown()
        self.table.updateRow(
                {'id':idx}, {'content':text})
