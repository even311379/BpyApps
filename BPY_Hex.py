from browser import document, html, timer
from enum import Enum


class ColorType(Enum):
    Hex = 1
    RGB = 2
    Linear = 3


PANEL_ID = 0
EXISTING_PANEL_IDS = []
ALLOW_EDIT = False
CURRENT_COLOR_TYPE = ColorType.Hex
MOST_RECENT_BADGE = None


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
    document[ev.target.id] <= document[src_id]
    ev.preventDefault()


def AddFromPicker(ev):
    global PANEL_ID
    global EXISTING_PANEL_IDS
    global CURRENT_COLOR_TYPE
    CT = ev.target.value
    if CURRENT_COLOR_TYPE == ColorType.RGB:
        CT = f'{int(CT[1:3], 16)},{int(CT[3:5], 16)},{int(CT[5:7], 16)}'
    elif CURRENT_COLOR_TYPE == ColorType.Linear:
        c0 = round(int(CT[1:3], 16)/255, 3)
        c1 = round(int(CT[3:5], 16)/255, 3)
        c2 = round(int(CT[5:7], 16)/255, 3)
        CT = f'{c0},{c1},{c2}'
    document['Palette1'] <= SetupColorPanel(CT, ev.target.value, PANEL_ID)
    EXISTING_PANEL_IDS.append(PANEL_ID)
    PANEL_ID += 1


def AddFromInput(ev):
    global PANEL_ID
    global EXISTING_PANEL_IDS
    global CURRENT_COLOR_TYPE
    C = ev.target.value
    # check C is hex:
    C_Is_Hex = False
    if C.startswith('#') and len(C) == 7:
        for i in C[1:]:
            if i not in '0123456789abcdefABCDEF':
                print(i)
                break
        else:
            C_Is_Hex = True
    if C_Is_Hex:
        CT = ev.target.value
        if CURRENT_COLOR_TYPE == ColorType.RGB:
            CT = f'{int(CT[1:3], 16)},{int(CT[3:5], 16)},{int(CT[5:7], 16)}'
        elif CURRENT_COLOR_TYPE == ColorType.Linear:
            c0 = round(int(CT[1:3], 16)/255, 3)
            c1 = round(int(CT[3:5], 16)/255, 3)
            c2 = round(int(CT[5:7], 16)/255, 3)
            CT = f'{c0},{c1},{c2}'
        document['Palette1'] <= SetupColorPanel(CT, ev.target.value, PANEL_ID)
        EXISTING_PANEL_IDS.append(PANEL_ID)
        PANEL_ID += 1
        return

    # check is RGB

    
    # check is linear

    print('input color is not hex')
    print(ev.target.value)


def convert_colortext(CT, ColorText):
    global CURRENT_COLOR_TYPE
    if CT == CURRENT_COLOR_TYPE:
        return ColorText
    cs = ColorText.split(',')
    if CT == ColorType.RGB:
        if CURRENT_COLOR_TYPE == ColorType.Hex:
            return f'{int(ColorText[1:3], 16)},{int(ColorText[3:5], 16)},{int(ColorText[5:7], 16)}'
        if CURRENT_COLOR_TYPE == ColorType.Linear:
            return f'{int(float(cs[0])*255)},{int(float(cs[1])*255)},{int(float(cs[2])*255)}'
    if CT == ColorType.Hex:
        if CURRENT_COLOR_TYPE == ColorType.RGB:
            return f'#{hex(int(cs[0]))[2:4]}{hex(int(cs[1]))[2:4]}{hex(int(cs[2]))[2:4]}'
        if CURRENT_COLOR_TYPE == ColorType.Linear:
            return f'#{hex(int(float(cs[0])*255))[2:4]}{hex(int(float(cs[1])*255))[2:4]}{hex(int(float(cs[2])*255))[2:4]}'
    if CT == ColorType.Linear:
        if CURRENT_COLOR_TYPE == ColorType.RGB:
            return f'{round(int(cs[0])/255, 3)},{round(int(cs[1])/255, 3)},{round(int(cs[2])/255, 3)}'
        if CURRENT_COLOR_TYPE == ColorType.Hex:
            c0 = round(int(ColorText[1:3], 16)/255, 3)
            c1 = round(int(ColorText[3:5], 16)/255, 3)
            c2 = round(int(ColorText[5:7], 16)/255, 3)
            return f'{c0},{c1},{c2}'


def SetupColorText(CT):
    global EXISTING_PANEL_IDS
    global CURRENT_COLOR_TYPE
    for PID in EXISTING_PANEL_IDS:
        ele = document[f'Panel_{PID}'].children[1]
        ele.value = convert_colortext(CT, ele.value)
    CURRENT_COLOR_TYPE = CT


def ChangeColorType(ev):
    if ev.target.value == 'HEX':
        SetupColorText(ColorType.Hex)
    elif ev.target.value == 'RGB':
        SetupColorText(ColorType.RGB)
    else:
        SetupColorText(ColorType.Linear)


def DeletePanel(ev):
    global EXISTING_PANEL_IDS
    global ALLOW_EDIT
    EXISTING_PANEL_IDS.remove(int(ev.target.parentElement.id.split('_')[1]))
    del (document[ev.target.parentElement.id])


def HideBadge():
    global MOST_RECENT_BADGE
    MOST_RECENT_BADGE.style = dict(display='none')


def CopyColor(ev):
    global MOST_RECENT_BADGE
    ev.target.select()
    ev.target.setSelectionRange(0, 9999)
    document.execCommand('Copy')
    MOST_RECENT_BADGE = ev.target.parentElement.children[2]
    MOST_RECENT_BADGE.style = {'display': 'block'}
    timer.set_timeout(HideBadge, 1000)
    print('Copied!?')


def SetupColorPanel(ColorText, HexColor, Nid):
    BTN = html.BUTTON(Class="delete is-small", style={'display': 'none'})
    BTN.bind('click', DeletePanel)
    ColorDiv = html.INPUT(
        type='text',
        value=ColorText,
        readonly=True,
        style={'background': 'inherit', 'border': 0, 'width':'100%'}
    )
    ColorDiv.bind('click', CopyColor)
    Badge = html.SPAN('Copied!', Class="badge is-top-right is-info", style={'display': 'none'})
    O = html.DIV(
        [BTN, ColorDiv, Badge],
        Class="notification",
        id=f'Panel_{Nid}',
        style={
            'margin-bottom': '0.5rem',
            'background-color': HexColor
        }
    )
    # O.draggable = True
    O.bind('mouseover', MouseOver)
    O.bind('dragstart', DragStart)
    return O


# document['Palette4']<=ocument['Panel1'] # can easily move item
# del(document['Palette3']) # Can easily delete item!

document['ColorInput'].bind('change', AddFromInput)
document['ColorPicker'].bind("change", AddFromPicker)
document['DisplayType'].bind("change", ChangeColorType)

for i in range(1, 5):
    document[f'Palette{i}'].bind('dragover', DragOver)
    document[f'Palette{i}'].bind('drop', Drop)


def ToggleAllowEdit(ev):
    global EXISTING_PANEL_IDS
    global ALLOW_EDIT
    ALLOW_EDIT = ev.target.checked
    if ev.target.checked:
        for ID in EXISTING_PANEL_IDS:
            ele = document[f'Panel_{ID}']
            # print(dir(ele))
            ele.draggable = True
            ele.children[0].style = {'display': 'block'}
    else:
        for ID in EXISTING_PANEL_IDS:
            ele = document[f'Panel_{ID}']
            ele.draggable = False
            ele.children[0].style = {'display': 'none'}


document['EditableSwitch'].bind('change', ToggleAllowEdit)


def InitPage(ev):
    document['EditableSwitch'].checked = False
    print('page is reloaded')


document <= html.DIV(id='HiddenTrigger', style=dict(display='none'))
document['HiddenTrigger'].bind('click', InitPage)
document['HiddenTrigger'].click()

ele = document['DisplayType']
if ele.value == 'RGB':
    CURRENT_COLOR_TYPE = ColorType.RGB
elif ele.value == 'HEX':
    CURRENT_COLOR_TYPE = ColorType.Hex
else:
    CURRENT_COLOR_TYPE = ColorType.Linear
