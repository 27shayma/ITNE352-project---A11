import socket
import PySimpleGUI as psg
import signal
import sys

# Theme for the PySimpleGUI windows
psg.theme('TealMono')

# Functions
# Creation Function: To create a PySimpleGUI window with a specific title & layout
def Creation(title, layout):
    window= psg.Window(title, layout, resizable=True)
    return window