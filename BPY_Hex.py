from browser import document, html
from browser.widgets.dialog import InfoDialog
import re

PANEL_ID = 0

# drag and drop events
def MouseOver(ev):
    ev.target.style.cursor = "pointer"

def DragStart(ev):
    ev.dataTransfer.setData("dpanel", ev.target.id)
    ev.dataTransfer.effectAllowed = "move"

def DragOver(ev):
    ev.dataTransfer.dropEffect = "move"
    ev.preventDefault()

def Drop(ev):
    src_id = ev.dataTransfer.getData('dpanel')
    document[ev.target.id]<=document[src_id]
    ev.preventDefault()

def show(ev):
    document['ColorInput'].value = document['ColorPicker'].value
    # InfoDialog("Hey", f"You triggered things...{document['DisplayType'].value}")

def ChangeColorType(ev):
    pass

def DeletePanel(ev):
    del(document[ev.target.parentElement.id])

def SetupColorPanel(ColorText, Nid):
    BTN = html.BUTTON(Class="delete is-small")
    BTN.bind('click', DeletePanel)
    O = html.DIV(
        [BTN, ColorText],
        Class="notification",
        id=f'Panel_{Nid}',
        style={
            'padding': '0.8rem',
            'margin-bottom': '0.5rem',
            'background-color': ColorText
        }
    )
    O.draggable = True
    O.bind('mouseover', MouseOver)
    O.bind('dragstart', DragStart)
    return O

# document['Palette4']<=document['Panel1'] # can easily move item
# del(document['Palette3']) # Can easily delete item!


def AddPanelToPalette(et):
    global PANEL_ID
    document['Palette1'] <= SetupColorPanel(document['ColorInput'].value, PANEL_ID)
    PANEL_ID += 1


document['ColorPicker'].bind("change", show)
document['DisplayType'].bind("change", ChangeColorType)
document['Add'].bind('click', AddPanelToPalette)

for i in range(1,5):
    document[f'Palette{i}'].bind('dragover', DragOver)
    document[f'Palette{i}'].bind('drop', Drop)

ALLOW_EDIT = -1

def ToggleAllowEdit(ev):
    global ALLOW_EDIT
    ALLOW_EDIT *= -1
    if (ALLOW_EDIT > 0): 
        pass        
    else:
        pass

document['EditableSwitch'].bind('change', ToggleAllowEdit)