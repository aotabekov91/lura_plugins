from plug.qt import Plug 
from tables import Bookmark as Table

class Bookmark(Plug):

    special=['return', 'carriage']

    def __init__(
            self, 
            app, 
            special=special,
            listen_leader='<c-b>',
            **kwargs):

        super().__init__(
                app=app, 
                special=special,
                listen_leader=listen_leader,
                **kwargs) 

    def setup(self):

        super().setup()
        self.table=Table()
        self.display=self.app.display
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
        bar.bottom.show()
        bar.show()
        bar.edit.setFocus()
        rows=self.getBookmark()
        if rows: 
            bar.edit.setText(rows[0]['text'])

    def getBookmark(self):

        prev=self.app.plugman.prev
        if prev and prev.name=='normal':
            view=self.display.currentView()
            if view:
                page=view.pageItem().page().pageNumber()
                position=[str(f) for f in view.saveLeftAndTop()]
                data={'page' : page, 
                      'hash' : view.model().id(),
                      'position' : ':'.join(position)
                      }
                row=self.table.getRow(data)
                return row

    def bookmark(self):

        prev=self.app.plugman.prev
        text=self.app.window.bar.edit.text()
        if prev:
            view=self.display.currentView()
            if prev.name=='normal' and view:
                rows=self.getBookmark()
                if rows:
                    self.table.updateRow(
                            {'id': rows[0]['id']},
                            {'text':text})
                else:
                    page=view.pageItem().page().pageNumber()
                    position=[str(f) for f in view.saveLeftAndTop()]
                    row={
                            'title':text, 
                            'text':text,
                            'kind':'document',
                            'hash':view.model().id(),
                            'page':page,
                            'position':':'.join(position),
                            }
                    self.table.writeRow(row)
        self.delistenWanted.emit()
