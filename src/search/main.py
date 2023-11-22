from plug.qt import Plug
from gizmo.utils import tag

class Search(Plug):

    special=['return']

    def __init__(self, 
            *args,
            special=special,
            listen_leader='/',
            **kwargs):

        super().__init__(
                *args,
                special=special,
                listen_leader=listen_leader, 
                **kwargs,
                )

        self.m_data=[]
        self.view=None
        self.text=None
        self.match=None
        self.m_idx=-1
        self.setConnect()

    def setConnect(self):

        self.bar=self.app.ui.bar
        self.ear.returnPressed.connect(
                self.startSearch)

    def listen(self): 

        super().listen()
        self.connectView()
        self.activateBar()

    def delisten(self):

        super().delisten()
        self.disconnectView()
        self.deactivateBar()
        self.clear()

    def clear(self):

        self.cleanUp()
        self.m_data=[]
        self.text=None
        self.match=None
        self.m_idx=-1

    def cleanUp(self):

        for (i, r) in self.m_data:
            if self.view.check(
                    'canHighlight', i):
                i.highlight()

    def startSearch(self):

        self.clear()
        t=self.bar.edit.text()
        if t: self.view.search(t)
        self.deactivateBar()

    @tag('<c-f>')
    def toggleFocus(self): 

        if self.bar.edit.hasFocus():
            self.deactivateBar()
        else:
            self.activateBar()

    @tag('j')
    def next(self, digit=1): 
        self.jump(digit)

    @tag('k')
    def prev(self, digit=1): 
        self.jump(-digit)

    def jump(self, digit=1):

        if self.m_data:
            self.m_idx+=digit
            if self.m_idx>=len(self.m_data):
                self.m_idx=0
            elif self.m_idx<0:
                self.m_idx=len(self.m_data)-1
            i, r = self.m_data[self.m_idx]
            if self.view.check(
                    'canHighlight', i):
                i.highlight(r)
            d = i.index()
            self.view.goto(d)
            s=i.mapRectToScene(r)
            self.view.centerOn(s.x(), s.y())

    def update(self, data):

        initial=False
        if not self.m_data and data:
            initial=True
        self.m_data+=data
        # self.view.select(self.m_data)
        if initial: self.jump()

    def activateBar(self):

        self.bar.bottom.show()
        self.bar.mode.setText('/')
        self.bar.edit.show()
        self.bar.edit.setFocus()

    def deactivateBar(self):

        self.bar.bottom.hide()
        self.bar.edit.clear()
        self.bar.mode.clear()

    def connectView(self):

        self.view.searchFound.connect(
                self.update)

    def disconnectView(self):

        self.view.searchFound.disconnect(
                self.update)

    def checkLeader(self, event, pressed):

        if super().checkLeader(event, pressed):
            if self.ear.listening:
                return True
            c=self.app.moder.current
            if c and c.name=='normal':
                v=c.getView()
                if hasattr(v, 'canSearch'):
                    self.view=v
                    return True
        return False
