from PyQt5 import QtCore
from plug.qt import Plug 
from tables import Bookmark as Table

class Bookmark(Plug):

    marked=QtCore.pyqtSignal()
    special=['return', 'carriage']

    def __init__(
            self, 
            app, 
            special=special,
            report_keys=False,
            listen_leader='<c-b>',
            **kwargs
            ):

        self.table=Table()
        self.display=app.display
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
        bar=self.app.window.bar
        bar.bottom.hide()
        bar.edit.clear()

    def listen(self):

        super().listen()
        bar=self.app.window.bar
        r=self.getBookmark()
        if r: 
            text=r[0]['text']
            bar.edit.setText(text)
        bar.bottom.show()
        bar.edit.setFocus()

    def getBookmark(self):

        view=self.display.currentView()
        if view:
            page=view.pageItem().page()
            pnum=page.pageNumber()
            position=[]
            for f in view.getPosition():
                position+=[str(f)]
            data={'page' : pnum, 
                  'hash' : view.model().id(),
                  'position' : ':'.join(position)
                  }
            return self.table.getRow(data)

    def bookmark(self):

        t=self.app.window.bar.edit.text()
        view=self.display.currentView()
        if view:
            rows=self.getBookmark()
            if rows:
                self.table.updateRow(
                        {'id': rows[0]['id']},
                        {'text':t})
            else:
                page=view.pageItem().page()
                pnum=page.pageNumber()
                position=[]
                for f in view.getPosition():
                    position+=[str(f)]
                row={
                     'text':t, 
                     'title':t, 
                     'page':pnum, 
                     'kind':'document', 
                     'hash':view.model().id(),
                     'position':':'.join(position)
                     }
                self.table.writeRow(row)
            self.marked.emit()
        self.delistenWanted.emit()
