from PyQt5 import QtCore
from plug.qt import Plug
from plug.qt.utils import register
from gizmo.widget import ListWidget, Item

class SearchList(Plug):

    def setup(self):

        self.text_color='green'

        super().setup()
        self.app.plugman.plugsLoaded.connect(
                self.on_plugsLoaded)

    def on_plugsLoaded(self, plugs):

        self.search=plugs.get('Search', None)

        if self.search:
            self.searchSearch=self.search.search
            self.search.search=self.ownSearch
            self.searchJump=self.search.jump
            self.search.jump=self.jump
            self.setUI()

    def jump(self, *args, **kwargs):

        self.searchJump(*args, **kwargs)
        idx=self.search.index
        self.ui.list.setCurrentRow(idx)

    def ownSearch(self, text, *args, **kwargs):

        found=self.searchSearch(text, *args, **kwargs)
        if found:
            # self.ui.model.clear()
            for f in found:
                page, rect = f
                text=self.getLine(text, page, rect)
                item=QtGui.QStandardItem(text)
                self.ui.model.appendRow(item)
            self.ui.updatePosition()
            self.ui.show()
        return found

    def setUI(self):

        self.ui=ListWidget(
                    objectName='SearchList',
                    parent=self.app.window,
                )
        self.ui.hide()
        
    def getLine(self, text, page, rectF):

        w=page.size().width()
        lrec=QtCore.QRectF(0, rectF.y(), w, rectF.height())
        line=f'<html>{page.find(lrec)}</html>'
        rep=f'<font color="{self.text_color}">{text}</font>'
        return line.replace(text, rep)
