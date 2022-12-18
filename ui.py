#Autor: Nathan Silva Rodrigues
#Disciplina: PDI - EngComp 2022/02
#Data: Dezembro 2022

import PySimpleGUI as sg
import numpy as np

def buildUi():
    reset_button = sg.Button(
        'Reset Count'
    )

    debug_button = sg.Button(
        'Show/Hide Debug'
    )

    table = sg.Table(
        values=[[0.0,0.0,0.0,0.0,0.0,0.0], [0.0,0.0,0.0,0.0,0.0,0.0], [0.0,0.0,0.0,0.0,0.0,0.0]],
        row_colors=([(0,'black','white'),(1,'white','red'),(2,'black','yellow')]),
        headings=['Num 1','Num 2','Num 3','Num 4','Num 5','Num 6'],
        auto_size_columns=True,
        justification='center',
        key='data_table',
        select_mode=sg.TABLE_SELECT_MODE_NONE
        )

    last_launch = sg.Text(
        'No Launch',
        key='txt_last_launch'
    )

    #Window Layout
    layout = [  [table], [reset_button, last_launch], [debug_button]]

    #Create the Window
    window = sg.Window('Dice Dot Counter', layout)
    return window

def updateTableValues(window, wht_data, red_data, ylw_data):
    window['data_table'].update(values=(wht_data.tolist(),red_data.tolist(),ylw_data.tolist()), row_colors=([(0,'black','white'),(1,'white','red'),(2,'black','yellow')]),)

def updateLastLaunch(window, mean_wht, mean_red, mean_ylw):
    window['txt_last_launch'].update(f'Last Launch: WHT={mean_wht} RED={mean_red} YLW={mean_ylw}')

def clearTableValues(window):
    window['data_table'].update(values=([0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0,0.0]), row_colors=([(0,'black','white'),(1,'white','red'),(2,'black','yellow')]),)



#Autor: Nathan Silva Rodrigues
#Disciplina: PDI - EngComp 2022/02
#Data: Dezembro 2022