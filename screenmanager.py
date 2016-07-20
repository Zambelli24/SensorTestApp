import kivy
import random
kivy.require('1.8.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.progressbar import ProgressBar
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.textinput import TextInput

class LoginScreen(Screen):
    pass

class TestScreen(Screen):
    def saveTest(self, testname):
        print('Selected Test: {test}'.format(test=testname))

class UserScreen(Screen):
    def saveUser(self, username):
        print('Selected User: {user}'.format(user=username))

class ResultsLabel(Label):
    def __init__(self, filename, *args, **kwargs):
        super(ResultsLabel, self).__init__(*args, **kwargs)
        f = open(filename, 'r')
        text = ''
        for line in f:
            text += str(line)
        f.close()
        self.text=text
        self.halign='center'
        self.height=self.texture_size[1]
        self.text_size=app.width, None

class InstructionLabel(Label):
    def __init__(self, *args, **kwargs):
        super(InstructionLabel, self).__init__(*args, **kwargs)
        self.halign='center'
        #self.height=self.texture_size
        #self.text_size=app.width, None

class ResultsPopUp(Popup):
    def __init__(self, **kwa):
        super(ResultsPopUp, self).__init__(**kwa)
        layout = BoxLayout(orientation='vertical')
        b = Button(text='Close', size_hint=[.2, .075],
            pos_hint={'x':.4, 'y':.5})
        l = ResultsLabel('directions.txt')
        layout.add_widget(l)
        layout.add_widget(b)
        self.popup = Popup(title='Results', content=layout)
        b.bind(on_press=self.popup.dismiss)

    def show(self):
        self.popup.open()

class ProgressBarScreen(Screen):
    progress_bar = ObjectProperty()

    def __init__(self, **kwa):
        super(ProgressBarScreen, self).__init__(**kwa)

        self.progress_bar = ProgressBar()
        self.popup = Popup(
            title='Running, Do Not Exit',
            content=self.progress_bar
        )
        self.popup.bind(on_open=self.puopen)
        layout = BoxLayout(orientation='horizontal', size_hint=[.5, .1],
            pos_hint={'x':.5, 'y':0})
        layout.add_widget(Button(text='Run Current Test', on_release=self.pop))
        layout2 = BoxLayout(orientation='vertical', size_hint=[1, .9],
            pos_hint={'x':0, 'y':.1})
        layout2.add_widget(Label(text='Here are the instructions'))
        f = open('directions.txt', 'r')
        n = 0
        for line in f:
            n += 1
            layout2.add_widget(InstructionLabel(text='#' + str(n) + '. ' + str(line)))
        f.close()
        self.add_widget(layout)
        self.add_widget(layout2)

    def pop(self, instance):
        self.progress_bar.value = 1
        self.popup.open()

    def next(self, dt):
        self.progress_bar.value += 1

    def puopen(self, instance):
        while self.progress_bar.value<100:
            Clock.schedule_once(self.next, 5)
            self.progress_bar.value += 1
        if self.progress_bar.value>=100:
            self.popup.dismiss()
            ResultsPopUp().show()

class CreateNewUserScreen(Screen):

    def createNewUser(self, string):
        print('Newly Created User: {}'.format(string))


class ScreenManagement(ScreenManager):
    pass

app = Builder.load_file("tests.kv")

class TestApp(App):
    def build(self):
        return app

if __name__ == '__main__':
    TestApp().run()