from PyQt5 import QtCore
from plug.qt import Plug 
from tables import Bookmark as Table

class Bookmark(Plug):

    special=['return']
    bookmarked=QtCore.pyqtSignal()

    def __init__(
            self, 
            special=special,
            report_keys=False,
            listen_leader='<c-b>',
            **kwargs
            ):

        super().__init__(
                special=special,
                report_keys=report_keys,
                listen_leader=listen_leader,
                **kwargs) 
        self.view=None
        self.table=Table()
        self.bar=self.app.window.bar
        self.ear.returnPressed.connect(
                self.bookmark)

    def delisten(self):

        super().delisten()
        self.bar.bottom.hide()
        self.bar.edit.clear()

    def listen(self):

        super().listen()
        self.getBookmark(edit_bar=True)
        self.bar.bottom.show()
        self.bar.edit.setFocus()

    def getBookmark(self, edit_bar=False):

        loc=self.view.getLocator()
        r=self.table.getRow(loc)
        if r and edit_bar: 
            t=r[0]['text']
            self.bar.edit.setText(t)
        return r

    def bookmark(self):

        t=self.bar.edit.text()
        rows=self.getBookmark()
        if rows:
            c={'id': rows[0]['id']}
            self.table.updateRow(
                    c, {'text':t})
        else:
            loc=self.view.getLocator()
            loc.update({'text': t, 'title': t})
            self.table.writeRow(loc)
        self.bookmarked.emit()
        self.delistenWanted.emit()

    def checkLeader(self, e, p):

        if super().checkLeader(e, p):
            if self.ear.listening:
                return True
            c=self.app.moder.current
            if c and getattr(c, 'getView'):
                v=c.getView()
                if v.check('canPosition'):
                    self.view=v
                    return True
        return False
