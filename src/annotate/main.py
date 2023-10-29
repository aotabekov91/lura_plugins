from plug.qt import Plug
from functools import partial
from PyQt5 import QtGui, QtCore
from gizmo.utils import register
from tables import Annotation as Table

class Annotate(Plug):

    removed=QtCore.pyqtSignal()
    annotated=QtCore.pyqtSignal()
    chosen=QtCore.pyqtSignal(object)

    def __init__(
            self, 
            app, 
            *args, 
            listen_leader='<c-a>', 
            **kwargs
            ):

        self.cache=[]
        self.colors={}
        self.current=None
        self.table=Table()
        self.selected=None
        self.func_colors={}
        self.default_color='cyan'
        self.ignore_selection=False
        super().__init__(
                *args, 
                app=app, 
                listen_leader=listen_leader,
                **kwargs,
                )
        self.connect()
        self.setColors()

    def setColors(self):

        c=self.colors
        for k, v in c.items():
            n=v['name']
            c=v['color']
            f=partial(self.annotate, func=n)
            f.key=f'{k}'
            f.modes=[]
            self.func_colors[n]=c
            self.actions[(self.name, n)]=f
        self.app.moder.save(
                self, self.actions)

    def connect(self):

        self.display=self.app.display
        self.app.moder.modeChanged.connect(
                self.on_mode)
        self.app.display.viewCreated.connect(
                self.on_view)
        self.app.selection.connect(
                self.on_selection)

    def on_selection(self, v, s):

        if self.ignore_selection:
            return
        self.selected=None
        if not s:
            return
        s=s[0]
        i=s['item']
        idx=i.index()
        pos=s['area_unified'][0]
        anns=v.model().annotations()
        for a in anns: 
            if idx!=a['page']: 
                continue
            for b in a['boundaries']:
                if not b.intersects(pos): 
                    continue
                a['box']=[]
                self.selected=a
                for b in a['boundaries']:
                    box = i.mapToItem(
                            b, isUnified=True)
                    box = i.mapToPage(
                            box, unify=False)
                    a['box'] += [box]
                a['item'] = i
                a['aid']=a.get('id', None)
                self.chosen.emit(a)
                return a

    def on_view(self, v):
        self.on_mode(v=v)

    def on_mode(self, m=None, v=None):

        if m==self:
            return
        if not v:
            v=self.retrieveView(m)
        if v and not v in self.cache:
            self.cache+=[v]
            d={
              'kind': v.kind(),
              'hash': v.modelId(),
              }
            rs=self.table.getRow(d)
            for a in rs: 
                self.add(v, a)

    def annotate(self, func):

        s=self.current.selected()
        if s:
            d=self.write(func)
            self.add(self.current, d)
        self.annotated.emit()
        self.delistenWanted.emit()

    def write(self, func):

        v=self.current
        mid = v.modelId()
        s=v.selected()[0]
        i=s['item']
        x=i.index()
        t=s['text']
        a=s['area_unified']
        pos=v.getLocation(a)
        data = {
                'page': x,
                'hash': mid,
                'content':t,
                'position': pos,
                'function':func,
                'kind': v.kind(),
                }
        self.table.writeRow(data)
        fld=['function', 'kind', 'content']
        for f in fld:
            data.pop(f)
        i.select(dropCache=True)
        return self.table.getRow(data)[0]

    def add(self, v, a):

        if hasattr(v, 'annotate'):
            idx=a['page']
            f=a['function']
            p=a['position']
            l=v.getLocation(p)
            a['boundaries']=l
            c=self.default_color
            c=self.func_colors.get(f, c) 
            a['color'] = QtGui.QColor(c)
            a['akind']='highlightAnnotation'
            return v.annotate(idx, **a)

    @register('<c-.>d')
    def remove(self):

        if self.selected:
            e=self.selected['pAnn'].element()
            d={'id': self.selected['id']} 
            self.table.removeRow(d)
            e.removeAnnotation(self.selected)
            e.item().refresh(dropCache=True)
            self.selected=None
            self.removed.emit()

    @register('<c-.>s')
    def selectAnnotation(self):

        if self.selected:
            print(self.selected)
            i=self.selected['item']
            v=self.selected['view']
            self.ignore_selection=True
            v.select([self.selected])
            self.ignore_selection=False
            i.update()

    def retrieveView(self, mode):

        gv=getattr(mode, 'getView', None)
        if gv:
            v=gv()
            if v: return v

    def checkLeader(self, event, pressed):

        if super().checkLeader(event, pressed):
            if self.ear.listening: 
                self.current=None
                return True
            m=self.app.moder.current
            v=self.retrieveView(m)
            if v:
                self.current=v
                return True
        return False
