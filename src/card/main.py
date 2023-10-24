from threading import Thread
from ankipulator import Submitter
from plyer import notification as echo 

from plug.qt import Plug
from gizmo.utils import register
from gizmo.widget import InputList, UpDownEdit

class Card(Plug):

    def __init__(
            self, 
            app, 
            position='right', 
            prefix_keys={
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
                prefix_keys=prefix_keys,
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
        self.uiman.setUI()
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

    @register('u')
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
            self.model=i.itemData['up']
            flds=self.fields[self.model]
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

    @register('Y', modes=['command'])
    def yankToField(self, digit=1):

        self.yankToFieldJoin(
                digit=digit, sep='\n')

    @register('y', modes=['command'])
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

    @register('a', modes=['command'])
    def appendToField(self, digit=1): 

        self.yankToFieldJoin(
                digit, append=True)

    @register('A', modes=['command'])
    def appendToNewLine(self, digit=1): 

        self.yankToFieldJoin(
                digit=digit,
                append=True, 
                asep='\n',
                sep='\n'
                )

    @register('f', modes=['command'])
    def focusField(self, digit=1):

        digit-=1
        if not self.ui.main.isVisible():
            return
        self.modeWanted(self)
        w=self.getWidget(digit=digit)
        if w: w.setFocus()

    @register('t', modes=['command'])
    def toggle(self): 

        super().toggle()
        if not self.model:
            self.toggleModels()
        self.ui.current.list.setFocus()

    @register('p')
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

    @register('i')
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

    @register('d')
    def toggleDecks(self):

        if self.ui.decks.isVisible():
            self.ui.show(self.ui.main)
        else:
            self.ui.show(self.ui.decks)

    @register('m')
    def toggleModels(self):

        if self.ui.models.isVisible():
            self.ui.show(self.ui.main)
        else:
            self.ui.show(self.ui.models)

    def createNote(self):

        n={
          'deckName':self.deck, 
          'modelName':self.model,
          }
        f={}
        for d in self.ui.main.list.dlist:
            f[d['id']]=d['down']
        n['fields']=f
        return n

    @register('s', modes=['Card', 'command'])
    def submit(self):

        try:
            n=self.createNote()
            self.filler.addNotes(n)
            self.clear()
            msg='Submitted to Anki'
        except:
            msg='Could not be submitted to Anki'
        echo.notify(
                message=msg,
                title='Card', 
                timeout=0.05,
                )

    @register('C')
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

    @register('c', modes=['command'])
    def addCloze(self):

        if self.input:
            self.input.textCreated.connect(
                    self.on_clozeCreated)
            self.input.carriagePressed.connect(
                    self.on_inputEscapePressed)
            self.input.escapePressed.connect(
                    self.on_inputEscapePressed)
            self.input.setRatio(
                    w=0.6, h=0.3)
            self.input.activate()
            text=self.getSelected()
            self.input.setText(text)

    def on_clozeCreated(self):
        raise

    def on_inputEscapePressed(self):

        self.input.setRatio()
        self.input.carriagePressed.disconnect(
                self.on_inputReturnPressed)
        self.input.escapePressed.disconnect(
                self.on_inputEscapePressed)
        self.input.textCreated.disconnect(
                self.on_clozeCreated)

    def on_inputReturnPressed(self):

        self.on_inputEscapePressed()
        t=self.input.widget.field.toPlainText()
        self.input.hideClearField()
        self.app.moder.setMode()
        if self.m_inputField:
            self.m_inputField.setTextDown(t)
