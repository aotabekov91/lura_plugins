from gizmo.utils import tag
from tables import Bookmark
from plug.qt.plugs.render import Render 
from gizmo.vimo.model import WTableModel
from gizmo.vimo.view import ListWidgetView 

class Bookmarks(Render):

    cache={}
    color='#CC885E'
    position='dock_right'
    leader_keys={
        'command': 'b',
        'normal': '<c-.>'}
    model_class=WTableModel
    model_class.kind='bookmarks'
    model_class.table=Bookmark()

    def setup(self):

        super().setup()
        ui=ListWidgetView(render=self)
        ui.__class__.__name__='BookmarksView'
        self.app.moder.typeChanged.connect(
                self.updateType)
        self.setupView(ui)

    def getModel(self, source):

        uid=source.getUniqLocator()
        uid['type']=self.model_class.kind
        m=self.app.buffer.getModel(uid)
        if m is None: 
            l=source.getUniqLocator()
            m=self.model_class(index=l)
            self.app.buffer.setModel(uid, m)
            m.load()
        return m

    def updateType(self, t):

        v=t.view
        if v and v.check('canLocate'):
            m=self.getModel(v)
            self.view.setModel(m)

    @tag('f', modes=['command'])
    def activate(self):
        self.setView(self.view)

    @tag('o', modes=['normal|Bookmarks'])
    def open(self):

        i=self.view.currentItem()
        t=self.app.moder.type()
        if i and t.view:
            e=i.element()
            t.view.openLocator(
                    e.data(), kind='position')

    @tag('d', modes=['normal|Bookmarks'])
    def delete(self):

        t=self.app.moder.type()
        m=self.getModel(t.view)
        idx=self.view.currentIndex()
        if idx and m:
            m.removeRow(idx.row())

    def setColorStyle(self, d):

        #todo
        style=f'background-color: {self.color}'
        d['up_style']=style

    def updateContent(self, w):
        
        #todo
        # w.list.widgetDataChanged.connect(
                # self.updateContent)
        self.table.updateRow(
                {'id': w.data['id']}, 
                {'text': w.data['down']})
