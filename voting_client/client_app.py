import PySimpleGUI as sg
from Client import Client


layout = [[sg.Text("Enter National ID Number:"), sg.Input(key='-NID-', do_not_clear=True, size=(20, 1))],
            [sg.Radio("Donald Trump", "RADIO", key='-TRUMP-'), 
            sg.Radio("Hilary Clinton", "RADIO", key='-CLINTON-'),
            sg.Radio("Bernie Sanders", "RADIO", key='-SANDERS-')
            ],
          [sg.Button('Vote'), sg.Button('Show Table'), sg.Exit()]]

window = sg.Window('Voting Program', layout)

client = Client("http://127.0.0.1:5001")

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == 'Vote':
        candidate = ''
        if values['-TRUMP-']: 
            candidate = 'Donald Trump'
        elif values['-CLINTON-']:
            candidate = 'Hilary Clinton'
        elif values['-SANDERS-']: 
            candidate = 'Bernie Sanders'
        client.create_new_transaction(candidate)

window.close()