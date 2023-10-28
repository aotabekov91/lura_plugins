from PyQt5 import QtCore
from plug.qt import Plug 
from tables import Bookmark as Table

class Bookmark(Plug):

    bookmarked=QtCore.pyqtSignal()
    special=['return', 'carriage']

    def __init__(
            self, 
            app, 
            special=special,
            report_keys=False,
            listen_leader='<c-b>',
            **kwargs
            ):

        self.mode=None
        self.table=Table()
        self.bar=app.window.bar
        super().__init__(
                app=app, 
                special=special,
                report_keys=report_keys,
                listen_leader=listen_leader,
                **kwargs) 
        self.setConnect()

    def setConnect(self):

        self.ear.returnPressed.connect(
                self.bookmark)
        self.ear.carriageReturnPressed.connect(
                self.bookmark)

    def delisten(self):

        super().delisten()
        self.bar.bottom.hide()
        self.bar.edit.clear()

    def listen(self):

        super().listen()
        r=self.getBookmark()
        if r: 
            t=r[0]['text']
            self.bar.edit.setText(t)
        self.bar.bottom.show()
        self.bar.edit.setFocus()

    def getBookmark(self):

        v=self.mode.getView()
        if v:
            p=v.itemId()
            i=v.modelId()
            l = v.getLocation()
            d={
               'hash' : i,
               'page' : p,
               'position' : l,
               'kind': v.kind(),
              }
            return self.table.getRow(d)

    def bookmark(self):

        v=self.mode.getView()
        if v:
            t=self.bar.edit.text()
            rows=self.getBookmark()
            if rows:
                c={'id': rows[0]['id']}
                self.table.updateRow(
                        c, {'text':t})
            else:
                p = v.itemId()
                m = v.modelId()
                l = v.getLocation()
                row={
                     'page': p, 
                     'text': t, 
                     'hash': m, 
                     'title': t, 
                     'position': l,
                     'kind': v.kind(), 
                     }
                self.table.writeRow(row)
            self.bookmarked.emit()
        self.delistenWanted.emit()

    def checkLeader(self, e, p):

        if super().checkLeader(e, p):
            if self.ear.listening:
                return True
            m=self.app.moder.current
            if m and getattr(m, 'getView'):
                self.mode=m
                return True
        return False
