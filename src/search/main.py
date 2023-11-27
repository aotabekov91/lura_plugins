from plug.qt import Plug
from PyQt5.QtCore import Qt
from gizmo.utils import tag

class Search(Plug):

    isMode=True
    listen_leader='/'

    def setup(self):

        super().setup()
        self.m_idx=-1
        self.m_data=[]
        self.view=None
        self.text=None
        self.match=None
        self.bar=self.app.ui.bar

    def event_functor(self, e, ear):

        enter=[Qt.Key_Return, Qt.Key_Enter]
        if e.key() in enter:
            self.startSearch()
            return True
        return False

    def listen(self): 

        super().listen()
        self.activateBar()
        self.view.searchFound.connect(self.update)

    def delisten(self):

        super().delisten()
        self.octivateBar()
        self.view.searchFound.disconnect(self.update)
        self.clear()

    def clear(self):

        self.cleanUp()
        self.m_idx=-1
        self.m_data=[]
        self.text=None
        self.match=None

    def cleanUp(self):

        for (i, r) in self.m_data:
            if self.view.check(
                    'canHighlight', i):
                i.highlight()

    def startSearch(self):

        self.clear()
        t=self.bar.edit.text()
        self.octivateBar()
        if t: self.view.search(t)

    @tag('<c-f>')
    def toggleFocus(self): 

        if self.bar.edit.hasFocus():
            self.octivateBar()
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
            if self.checkProp('canHighlight', i):
                i.highlight({'box': [r]})
            d = i.index()
            x, y = r.x(), r.y()-0.45
            self.view.goto(d, x, y)

    def update(self, data):

        initial=not self.m_data and data
        self.m_data+=data
        if initial: self.jump()

    def activateBar(self):

        self.bar.bottom.show()
        self.bar.mode.setText('/')
        self.bar.edit.show()
        self.bar.edit.setFocus()

    def octivateBar(self):

        self.bar.bottom.hide()
        self.bar.edit.clear()
        self.bar.mode.clear()

    def checkLeader(self, event, pressed):

        v=self.app.handler.view()
        if self.checkProp('canSearch', v):
            self.view=v
            return True
