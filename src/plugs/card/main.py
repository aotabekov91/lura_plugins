from threading import Thread

from plyer import notification
from ankipulator import Submitter

from qapp.plug import PlugObj
from qapp.utils import register
from qapp.widget import InputList, UpDownEdit

class Card(PlugObj):

    def __init__(self, app):

        super(Card, self).__init__(
                app=app,
                position='right',
                mode_keys={'command':'c'})

        self.decks=[]
        self.models=[]
        self.fields={}
        self.pinned=[]

        self.deck='No deck chosen'
        self.model='No model chosen'

        self.submitter=Submitter()
        self.setUI()

    def setUI(self):

        super().setUI()

        self.ui.addWidget(
                InputList(item_widget=UpDownEdit),
                'main', 
                main=True)

        self.ui.main.input.setLabel('Card')
        self.ui.main.returnPressed.connect(
                self.confirm)
        self.ui.main.list.widgetDataChanged.connect(
                self.on_contentChanged)

        self.ui.addWidget(InputList(), 'decks')
        self.ui.decks.input.setLabel('Decks')
        self.ui.decks.returnPressed.connect(
                self.on_decksReturnPressed)

        self.ui.addWidget(InputList(), 'models')
        self.ui.models.input.setLabel('Models')
        self.ui.models.returnPressed.connect(
                self.on_modelsReturnPressed)

        self.ui.addWidget(
                InputList(item_widget=UpDownEdit),
                'info')

        self.ui.info.input.setLabel('Info')
        self.ui.info.returnPressed.connect(
                self.on_modelsReturnPressed)

        self.ui.hideWanted.connect(self.deactivate)
        self.ui.installEventFilter(self)

    @register('cu', modes=['command', 'normal'])
    def inputField(self, digit=1):

        self.app.modes.input.returnPressed.connect(
                self.on_inputReturnPressed)
        self.app.modes.input.forceDelisten.connect(
                self.on_inputEscapePressed)

        self.app.modes.setMode('input')
        self.app.modes.input.showField()

        digit-=1

        self.inputField=None
        if hasattr(self.ui.current, 'list'):
            self.inputField=self.ui.current.list.getWidget(digit)
            label=self.inputField.textUp()
            self.app.modes.input.widget.label.setText(label)
            self.app.modes.input.showField(field=True, label=True)


    def on_inputEscapePressed(self):

        self.app.modes.input.returnPressed.disconnect(
                self.on_inputReturnPressed)
        self.app.modes.input.forceDelisten.disconnect(
                self.on_inputEscapePressed)

    def on_inputReturnPressed(self):

        self.on_inputEscapePressed()

        text=self.app.modes.input.widget.field.toPlainText()
        self.app.modes.input.hideClearField()
        self.app.modes.setMode('normal')

        if self.inputField:
            self.inputField.setTextDown(text)

    @register(key='u')
    def update(self):

        def _update():

            for d in self.submitter.getDecks():
                self.decks+=[{'up':d}]
                self.ui.decks.setList(self.decks)

            for m, flds in self.submitter.getModels().items():
                self.models+=[{'up':m}]
                self.ui.models.setList(self.models)
                self.fields[m]=flds

        t=Thread(target=_update)
        t.run()

    def on_contentChanged(self, widget):

        field=widget.textUp()
        value=widget.textDown()
        for data in self.ui.main.dataList():
            if data['up']==field: 
                data['down']=value
                return

    def on_decksReturnPressed(self):

        item=self.ui.decks.list.currentItem()
        if item:
            self.deck=item.itemData['up']
            self.ui.decks.clear()
            self.ui.show(self.ui.main)

    def on_modelsReturnPressed(self):

        item=self.ui.models.list.currentItem()
        if item:
            self.model=item.itemData['up']
            flds=self.fields[self.model]
            data=[{'up':f, 'down':''} for f in flds]
            self.ui.main.setList(data)
            self.ui.models.clear()
            self.ui.show(self.ui.main)

    @register('Y', modes=['command'])
    def yankToFieldSaveStructure(self, digit=1):

        view=self.app.main.display.view
        if view.selected(): 
            text=[]
            for s in view.selected(): text+=['\n'.join(s['text_data'])]
            text='\n'.join(text)

        self.yankToField(digit, separator='\n\n', text=text) 

    @register('y', modes=['command'])
    def yankToField(self, digit=1, append=False, separator=' ', text=None):

        digit-=1

        if hasattr(self.ui.current, 'list'):
            widget=self.ui.current.list.getWidget(digit)
            view=self.app.main.display.view
            if widget: 
                if not text:
                    if view.selected():
                        text=[]
                        for s in view.selected(): text+=[s['text']]
                        text=' '.join(text)
                    else:
                        return

                if append: 
                    wtext=widget.textDown()
                    text=f'{wtext}{separator}{text}'

                widget.setTextDown(text)
                view.select()

    @register('a', modes=['command'])
    def appendToField(self, digit=1): self.yankToField(digit, append=True)

    @register('A', modes=['command'])
    def AppendToField(self, digit=1): 

        self.yankToField(digit, append=True, separator='\n\n')

    @register('f', modes=['command'])
    def focusField(self, digit=1):

        digit-=1

        if hasattr(self.ui.current, 'list'):
            self.modeWanted(self)
            self.ui.current.list.focusItem(digit)

    @register('t', modes=['command'])
    def toggle(self): 

        super().toggle()
        if self.model=='No model chosen': self.toggleModels()
        if not self.decks: self.update()

    @register('p')
    def togglePin(self):

        item=self.ui.main.list.currentItem()
        if item: 
            fieldName=item.itemData['up']
            if fieldName in self.pinned:
                self.pinned.pop(self.pinned.index(fieldName))
            else:
                self.pinned.append(fieldName)

    @register('i')
    def toggleInfo(self):

        if self.ui.info.isVisible():
            self.ui.show(self.ui.main)
        else:
            infoList=[{'up':'Model', 'down': self.model}, 
                      {'up':'Deck', 'down': self.deck}]

            for p in self.pinned: 
                infoList+=[{'up': 'Pinned', 'down':p}]
            self.ui.info.setList(infoList)
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

        note={'deckName':self.deck, 'modelName':self.model}
        note['fields']={}
        for data in self.ui.main.dataList():
            note['fields'][data['up']]=data['down']
        return note

    @register('s', modes=['command'])
    def submit(self, note=None):

        if not note: note=self.createNote()

        try:

            self.submitter.addNotes(note)
            notification.notify(
                    title='LookupMode', 
                    message='Submitted to Anki')
            self.clear()

        except:
            notification.notify(
                    title='LookupMode', 
                    message='Could not be submitted to Anki')

    @register('C')
    def clear(self, force=False):

        flds=self.fields[self.model]
        data=[]
        for f in flds:
            if force or not f in self.pinned: 
                data+=[{'up':f, 'down':''}]
            else:
                for item in self.ui.main.dataList():
                    if item['up']==f: 
                        data+=[{'up':f, 'down':item['down']}]
                        break
        self.ui.main.setList(data)

    def confirm(self):

        if self.deck:
            if self.model:
                self.submit(self.createNote())
                self.clear()
                self.ui.show(self.ui.main)
        else:
            self.showDecks()
