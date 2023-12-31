from ankipulator import Submitter
from PyQt5 import QtWidgets, QtGui
from plyer import notification as echo 

from plug.qt import Plug
from gizmo.utils import tag
from gizmo.vimo.model import SModel
from gizmo.vimo.view import ListView
from gizmo.widget import StackedWidget

class Card(Plug):

    anki=Submitter()
    field_color='#AC33EF'
    listen_leader='<c-e>'
    position={'ui': 'dock_right'}
    prefix_keys={'command': 'c', 'Card': '<c-.>'} 

    def setup(self):

        super().setup()
        self.m_decks=[]
        self.m_models=[]
        self.fields={}
        self.pinned=[]
        self.m_deck=None
        self.m_model=None
        self.setData()
        self.setupUI()

    def setupUI(self):

        raise
        self.ui=StackedWidget()
        self.decks_view=ListView()
        self.decks_view.setModel(self.m_decks)
        self.ui.addWidget(self.decks_view, 'decks')
        self.app.uiman.setupUI(self, self.ui)

    @tag('d', modes=['command'])
    def activate(self):

        super().activate()
        self.ui.show(self.ui.decks)
        self.app.handler.setView(self.ui.decks)

        # main=InputList(
        #         widget=UpDownEdit,
        #         special=special)
        # main.input.setLabel('Card')
        # main.returnPressed.connect(
        #         self.submit)
        # main.list.widgetDataChanged.connect(
        #         self.on_contentChanged)
        # self.ui.addWidget(
        #         main, 'main', main=True)

        # decks=InputList(
        #         special=special)
        # decks.input.setLabel(
        #         'Decks')
        # decks.returnPressed.connect(
        #         self.on_decksReturnPressed)
        # self.ui.addWidget(
        #         decks , 'decks')

        # models=InputList(
        #         special=special)
        # models.input.setLabel('Models')
        # models.returnPressed.connect(
        #         self.on_modelsReturnPressed)
        # self.ui.addWidget(
        #         models, 'models')

        # info=InputList(
        #         widget=UpDownEdit,
        #         special=special)
        # info.input.setLabel('Info')
        # info.returnPressed.connect(
        #         self.on_modelsReturnPressed)
        # self.ui.addWidget(
        #         info, 'info')

    def getWidget(self, digit=None):

        c=self.ui.current
        l=getattr(c, 'list', None)
        if not l: return
        if digit: l.setCurrentRow(digit)
        item=l.currentItem()
        if not item: return
        return item.widget

    def setData(self):

        self.m_decks=SModel()
        for d in self.anki.getDecks():
            i=QtGui.QStandardItem(d.name)
            i.itemData=d.id
            self.m_decks.appendRow(i)
            # d={'up':d.name, 'id':d.id}
            # self.m_decks+=[d]

        # models=self.anki.getModels()
        # for m, flds in models.items():
        #     self.fields[m]=flds
        #     m={'up':m}
        #     self.m_models+=[m]
        # self.ui.decks.setList(self.m_decks)
        # self.ui.models.setList(self.m_models)

    def on_contentChanged(self, widget):

        f=widget.textUp()
        v=widget.textDown()
        for d in self.ui.main.list.dlist:
            if d['up']!=f: continue
            d['down']=v
            return

    def on_decksReturnPressed(self):

        item=self.ui.decks.list.currentItem()
        if item:
            self.m_deck=item.itemData['up']
            self.ui.show()

    def on_modelsReturnPressed(self):

        i=self.ui.models.list.currentItem()
        if i:
            model=i.itemData['up']
            self.setModel(model)

    def setModel(self, model):

        self.m_model=model
        flds=self.fields.get(
                self.m_model, {})
        data=[]
        for f in flds:
            data+=[{
              'id': f,
              'up': f'# {f}',
              'up_style': f'background-color: {self.field_color}',
              'down': ''
              }]
        self.ui.main.setList(data)
        if self.m_deck:
            self.ui.show()
        else:
            self.toggleDecks()

    @tag('Y', modes=['command'])
    def yankToField(self, digit=1):

        self.yankToFieldJoin(
                digit=digit, sep='\n')

    @tag('y', modes=['command'])
    def yankToFieldJoin(
            self, 
            sep=' ', 
            digit=1, 
            append=False, 
            asep=' ',
            ):

        if not self.ui.main.isVisible():
            return
        w=self.getWidget(digit=digit-1)
        if not w: return
        text=self.getSelected(sep)
        if not text: return
        if append: 
            wtext=w.textDown()
            text=f'{wtext}{asep}{text}'
        w.setTextDown(text)

    @tag('a', modes=['command'])
    def appendToField(self, digit=1): 

        self.yankToFieldJoin(
                digit, append=True)

    @tag('A', modes=['command'])
    def appendToNewLine(self, digit=1): 

        self.yankToFieldJoin(
                digit=digit,
                append=True, 
                asep='\n',
                sep='\n'
                )

    @tag('f', modes=['command'])
    def focusField(self, digit=1):

        digit-=1
        if not self.ui.main.isVisible():
            return
        self.modeWanted(self)
        w=self.getWidget(digit=digit)
        if w: w.setFocus()

    @tag('p')
    def togglePin(self):

        item=self.ui.main.list.currentItem()
        if item: 
            fieldName=item.itemData['up']
            if fieldName in self.pinned:
                self.pinned.pop(
                        self.pinned.index(fieldName))
            else:
                self.pinned.append(
                        fieldName)

    @tag('i')
    def toggleInfo(self):

        if self.ui.info.isVisible():
            self.ui.show(self.ui.main)
        else:
            info=[
                 {'up':'Model', 'down': self.m_model}, 
                 {'up':'Deck', 'down': self.m_deck},
                 ]
            for p in self.pinned: 
                info+=[{'up': 'Pinned', 'down':p}]
            self.ui.info.setList(info)
            self.ui.show(self.ui.info)

    @tag('d')
    def toggleDecks(self):
        self.toggleUI(self.ui.decks)

    @tag('m')
    def toggleModels(self):
        self.toggleUI(self.ui.models)

    def toggleUI(self, ui):

        if not ui.isVisible():
            self.ui.show(ui)
        else:
            self.ui.show()

    @tag('s', modes=['Card', 'command'])
    def submit(self, note=None):

        try:
            if not note:
                note=self.createNote()
            self.anki.addNotes(note)
            self.clear()
            msg='Submitted to Anki'
        except:
            msg='Could not be submitted to Anki'
        echo.notify(
                message=msg,
                title='Card', 
                timeout=0.05,
                )

    @tag('C')
    def clear(self, force=False):

        d=[]
        for f in self.fields[self.m_model]:
            if force or not f in self.pinned: 
                d+=[{'up':f, 'down':''}]
            else:
                dlist=self.ui.main.list.dlist
                for i in dlist: 
                    if i['up']!=f: continue
                    d+=[{'up':f, 'down':i['down']}]
                    break
        self.ui.main.setList(d)

    @tag('c', modes=['command'])
    def addCloze(self):

        self.activate()
        self.setModel('Cloze')

    def getSelected(self, sep=' '):

        v=self.app.display.view
        if v.selected(): 
            text=[]
            for s in v.selected(): 
                if 'lines' in s:
                    text+=s['lines']
                else:
                    text+=[s['text']]
            return f'{sep}'.join(text)
        return ''

    def createCloze(self, text):

        note=self.createNote(
                model='Cloze',
                fields={'Text':text},
                )
        self.submit(note)

    def createNote(
            self,
            deck=None,
            model=None,
            fields={}
            ):

        if not deck:
            deck=self.m_deck
        if not model:
            model=self.m_model
        if not fields:
            d=self.ui.main.list.dlist
            for f in d: 
                xid=f['id']
                fields[xid]=f['down']
        return {
                'deckName' : deck, 
                'modelName' : model, 
                'fields': fields
                }
