from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from gizmo.widget import TreeWidget

class PartTree(TreeWidget):
    
    def __init__(self, *args, **kwargs):

        super(PartTree, self).__init__(*args, **kwargs)

        self.setModel(QStandardItemModel())

    def installData(self, data):
    
        self.model().clear()
        self.setData(data)

        root=self.model().invisibleRootItem()

    def setData(self, data, parent=None):

        for k, v in data.items():
            item=QStandardItem()
            item.setText(v['data']['text'])
            item.itemData=v['data']
            if parent: 
                parent.appendRow(item)
            else:
                self.root=item
            for child in v['children']: 
                if k=='root':
                    root=self.model().invisibleRootItem()
                    self.setData(child, root)
                else:
                    self.setData(child, item)
