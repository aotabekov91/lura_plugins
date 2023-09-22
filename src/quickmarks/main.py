from plug.qt import Plug 
from plug.utils import register
from tables import Quickmark as Table
from gizmo.widget import UpDownEdit, InputList

class Quickmarks(Plug):

    def __init__(
            self, 
            app, 
            position='right',
            listen_leader='<c-M>',
            **kwargs):

        super().__init__(
                app=app, 
                position=position,
                listen_leader=listen_leader,
                **kwargs) 

        self.setUI()
        self.table=Table()

    def listen(self):

        super().listen()
        self.activated=True
        self.update()
        self.activateUI()

    def delisten(self):

        super().delisten()
        self.activated=False
        self.deactivateUI()

    def setUI(self):

        super().setUI()
        main=InputList(
                item_widget=UpDownEdit,
                objectName='QuickmarkList')
        self.ui.addWidget(main, 'main', main=True)
        self.ui.main.input.hideLabel()
        self.ui.main.returnPressed.connect(
                self.open)

    @register('.o')
    def open(self):

        item=self.ui.main.list.currentItem()
        if item: 
            self.app.window.main.openBy(
                    'bookmark', 
                    item.itemData['id']
                    )

    @register('.d')
    def delete(self):

        item=self.ui.main.list.currentItem()
        nrow=self.ui.main.list.currentRow()-1
        bid=item.itemData['id']
        self.table.removeRow({'id':bid})
        self.update()
        self.ui.main.list.setCurrentRow(nrow)
        self.ui.show()

    @register('.u')
    def update(self):

        prev=self.app.plugman.prev
        if prev and prev.name=='normal':
            view=self.app.window.main.display.currentView()
            if view:
                criteria={'hash': view.model().hash()}
                rows = self.table.getRow(criteria)
                for a in rows:
                    p, l, t = tuple(a['position'].split(':'))
                    a['down']=a['mark']
                    a['up']=f'# {p}'
                rows=sorted(
                        rows, 
                        key=lambda x: x['position']
                        )
                self.ui.main.setList(rows)
