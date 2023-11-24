from plug.qt import Plug
from gizmo.utils import tag
from PyQt5 import QtGui, QtCore
from tables import Annotation as Table
from gizmo.widget import InputList, UpDownEdit

class Annotations(Plug):

    cache={}
    view=None
    table=Table()
    func_colors={}
    position='dock_right'
    prefix_keys={
        'command': 'a',
        'Annotations': '<c-.>'}

    def setup(self):

        super().setup()
        self.app.buffer.modelCreated.connect(
                self.connectModel)
        self.app.moder.modeChanged.connect(
                self.updateData)
        self.app.moder.plugsLoaded.connect(
                self.setAnnotatePlug)
        self.setColors()
        self.setupUI()

    def setColors(self):

        c=self.colors
        for k, v in c.items():
            n, c = v['name'], v['color']
            self.func_colors[n]=QtGui.QColor(c)

    def event_functor(self, e, ear):

        if e.key()==QtCore.Qt.Key_Return:
            self.open()
            ear.clearKeys()
            return True

    def setupUI(self):

        w=InputList(widget=UpDownEdit)
        w.list.widgetDataChanged.connect(
                self.updateContent)
        self.app.uiman.setupUI(self, w)

    def connectModel(self, m):

        props=['loaded', 'canAnnotate']
        if self.checkProp(props, m):
            m.loaded.connect(self.annotateModel)

    def annotateModel(self, m):

        l=m.getUniqLocator(
                kind='annotation')
        rs=self.table.getRow(l)
        for r in rs: 
            self.updateAnnData(r, model=m)
            m.setLocator(r, 'annotation')

    def updateData(self, mode):

        if self.checkProp('hasView', mode):
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
        d['up_style']=f'background-color: {c.name}'
        if view:
            d['view']=view
            d['item']=view.item(element=elem)

    @tag('o')
    def open(self):

        i=self.ui.list.currentItem()
        if i:
            v=i.itemData['view']
            v.openLocator(
                    i.itemData, 
                    kind='annotation')

    @tag('d')
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
