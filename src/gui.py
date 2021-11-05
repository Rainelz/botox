from multiprocessing import Process, Queue
from threading import Thread
import PySimpleGUI as sg

from crypto import preprocess_key


class CredentialsGUI(Process):
    def __init__(self, dataQ, *args, **kwargs):
        super(CredentialsGUI, self).__init__(*args, **kwargs)
        self.dataQ = dataQ

    def run(self):
        layout = [
            [sg.Text('Please enter your Name, Address, Phone', font=40)],
            [sg.Text('Domain', size=(8, 1), font=18), sg.InputText(key='domain', font=32, size=(20, 1))],
            [sg.Text('Username', size=(8, 1), font=18), sg.InputText(key="username", font=32, size=(20, 1))],
            [sg.Text('Password', size=(8, 1), font=18),
             sg.InputText(key='password', font=32, size=(20, 1), password_char='•')],
            [sg.Submit(size=(12, 1), font=40), sg.Cancel(size=(12, 1), font=40)]
        ]

        window = sg.Window('Enter your data', layout, icon='resources/icon.ics', element_justification='c')
        event, values = window.read()
        window.close()
        if event == 'Submit':
            self.dataQ.put(values)
        else:
            self.dataQ.put(None)


class PasswordGUI(Process):
    def __init__(self, dataQ, *args, **kwargs):
        super(PasswordGUI, self).__init__(*args, **kwargs)
        self.dataQ = dataQ

    def run(self):
        layout = [
            [sg.Text('Please enter your password', font=40)],
            [sg.Text('Password', size=(8, 1), font=18),
             sg.InputText(key='password', font=32, size=(20, 1), password_char='•')],
            [sg.Submit(size=(12, 1), font=40), sg.Cancel(size=(12, 1), font=40)]
        ]

        window = sg.Window('Enter your data', layout, icon='resources/icon.ics', element_justification='c')
        event, values = window.read()
        window.close()
        if event == 'Submit':
            key = preprocess_key(values['password'])
            self.dataQ.put(key)
        else:
            self.dataQ.put(None)
