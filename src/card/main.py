from ankipulator import Submitter
from plyer import notification as echo 

from plug.qt import Plug
from gizmo.utils import tag
from gizmo.widget import InputList, UpDownEdit

class Card(Plug):

    def __init__(
            self, 
            app, 
            position='dock_right', 
            leader_keys={
                'command': 'c', 
                'Card': '<c-.>', 
                }, 
            **kwargs
            ):

        self.decks=[]
        self.models=[]
        self.fields={}
        self.pinned=[]
        self.deck=None
        self.model=None
        self.field_color='#AC33EF'
        super(Card, self).__init__(
                app=app,
                position=position,
                leader_keys=leader_keys,
                **kwargs
                )

    def setup(self):

        super().setup()
        self.filler=Submitter()
        self.setUI()
        self.update()
        self.app.moder.plugsLoaded.connect(
                self.on_plugsLoaded)

    def on_plugsLoaded(self, plugs):
        self.input=plugs.get('input', None)

    def setUI(self):

        special=['return']
        self.app.uiman.setUI(self)
        main=InputList(
                widget=UpDownEdit,
                special=special)
        main.input.setLabel('Card')
        main.returnPressed.connect(
                self.submit)
        main.list.widgetDataChanged.connect(
                self.on_contentChanged)
        self.ui.addWidget(
                main, 'main', main=True)
        decks=InputList(
                special=special)
        decks.input.setLabel(
                'Decks')
        decks.returnPressed.connect(
                self.on_decksReturnPressed)
        self.ui.addWidget(
                decks , 'decks')
        models=InputList(
                special=special)
        models.input.setLabel('Models')
        models.returnPressed.connect(
                self.on_modelsReturnPressed)
        self.ui.addWidget(
                models, 'models')
        info=InputList(
                widget=UpDownEdit,
                special=special)
        info.input.setLabel('Info')
        info.returnPressed.connect(
                self.on_modelsReturnPressed)
        self.ui.addWidget(
                info, 'info')

    def getWidget(self, digit=None):

        c=self.ui.current
        l=getattr(c, 'list', None)
        if not l: return
        if digit: l.setCurrentRow(digit)
        item=l.currentItem()
        if not item: return
        return item.widget

    @tag('u')
    def update(self):

        for d in self.filler.getDecks():
            d={'up':d.name, 'id':d.id}
            self.decks+=[d]
        models=self.filler.getModels()
        for m, flds in models.items():
            self.fields[m]=flds
            m={'up':m}
            self.models+=[m]
        self.ui.decks.setList(
                self.decks)
        self.ui.models.setList(
                self.models)

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
            self.deck=item.itemData['up']
            self.ui.show()

    def on_modelsReturnPressed(self):

        i=self.ui.models.list.currentItem()
        if i:
            model=i.itemData['up']
            self.setModel(model)

    def setModel(self, model):

        self.model=model
        flds=self.fields.get(
                self.model, {})
        data=[]
        for f in flds:
            data+=[{
              'id': f,
              'up': f'# {f}',
              'up_style': f'background-color: {self.field_color}',
              'down': ''
              }]
        self.ui.main.setList(data)
        if self.deck:
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

    @tag('t', modes=['command'])
    def toggle(self): 

        super().toggle()
        if not self.model:
            self.toggleModels()
        self.ui.current.list.setFocus()

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
                 {'up':'Model', 'down': self.model}, 
                 {'up':'Deck', 'down': self.deck},
                 ]
            for p in self.pinned: 
                info+=[{'up': 'Pinned', 'down':p}]
            self.ui.info.setList(info)
            self.ui.show(self.ui.info)

    @tag('d')
    def toggleDecks(self):

        if self.ui.decks.isVisible():
            self.ui.show(self.ui.main)
        else:
            self.ui.show(self.ui.decks)

    @tag('m')
    def toggleModels(self):

        if self.ui.models.isVisible():
            self.ui.show(self.ui.main)
        else:
            self.ui.show(self.ui.models)


    @tag('s', modes=['Card', 'command'])
    def submit(self, note=None):

        try:
            if not note:
                note=self.createNote()
            self.filler.addNotes(note)
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
        for f in self.fields[self.model]:
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


        if self.deck and self.input:
            self.input.follow=False
            self.input.getter=self.getSelected
            self.input.activate()
            self.input.setRatio(w=0.6, h=0.3)
            self.input.setter=self.createCloze
        else:
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
            deck=self.deck
        if not model:
            model=self.model
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
