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
MOST_RECENT_PANEL = None

def Int2Hex(input):
    o = hex(input)
    if len(o)==3:
        return '0'+o[2]
    else:
        return o[2:4]


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
    OCT = convert_colortext(ColorType.Hex, CT,CURRENT_COLOR_TYPE)
    document['Palette1'] <= SetupColorPanel(OCT, CT, PANEL_ID)
    EXISTING_PANEL_IDS.append(PANEL_ID)
    PANEL_ID += 1


def AddFromInput(ev):
    global PANEL_ID
    global EXISTING_PANEL_IDS
    global CURRENT_COLOR_TYPE
    C = ev.target.value.replace(' ', '')
    ColorIsDetermined = False

    # set invalid
    for i in C:
        if i not in '#,.0123456789abcdefABCDEF':
            document['ColorInvalid'].classList.remove('is-invisible')
            return
    # check C is hex:
    C_Is_Hex = False
    if C.startswith('#') and len(C) == 7:
        for i in C[1:]:
            if i not in '0123456789abcdefABCDEF':
                break
        else:
            C_Is_Hex = True
    if C_Is_Hex:
        ColorIsDetermined = True
        IC = convert_colortext(ColorType.Hex, C, CURRENT_COLOR_TYPE)
        HC = C

    # set invalid
    cs = C.split(',')
    if len(cs) != 3 and not ColorIsDetermined:
        document['ColorInvalid'].classList.remove('is-invisible')
        return
    # check is RGB
    if not ColorIsDetermined:
        if '.' not in C and 0 <= int(cs[0]) <= 255 and 0 <= int(cs[1]) <= 255 and 0 <= int(cs[2]) <= 255:
            ColorIsDetermined = True
            HC = convert_colortext(ColorType.RGB, C, ColorType.Hex)
            IC = convert_colortext(ColorType.RGB, C, CURRENT_COLOR_TYPE)
    # check is linear
    if not ColorIsDetermined:
        if '.' in C and 0 <= float(cs[0]) <= 1.0 and 0 <= float(cs[1]) <= 1.0 and 0 <= float(cs[2]) <= 1.0:
            ColorIsDetermined = True
            HC = convert_colortext(ColorType.Linear, C, ColorType.Hex)
            IC = convert_colortext(ColorType.Linear, C, CURRENT_COLOR_TYPE)

    if ColorIsDetermined:
        print(HC)
        document['ColorInvalid'].classList.add('is-invisible')
        document['Palette1'] <= SetupColorPanel(IC, HC, PANEL_ID)
        EXISTING_PANEL_IDS.append(PANEL_ID)
        PANEL_ID += 1
    else:
        document['ColorInvalid'].classList.remove('is-invisible')


def convert_colortext(InputType, ColorText, TargetType):
    if InputType == TargetType:
        return ColorText
    cs = ColorText.split(',')
    if InputType == ColorType.Hex and TargetType == ColorType.RGB:
        return f'{int(ColorText[1:3], 16)},{int(ColorText[3:5], 16)},{int(ColorText[5:7], 16)}'
    if InputType == ColorType.Hex and TargetType == ColorType.Linear:
        c0 = round(int(ColorText[1:3], 16) / 255, 3)
        c1 = round(int(ColorText[3:5], 16) / 255, 3)
        c2 = round(int(ColorText[5:7], 16) / 255, 3)
        return f'{c0},{c1},{c2}'
    if InputType == ColorType.RGB and TargetType == ColorType.Hex:
        return f'#{Int2Hex(int(cs[0]))}{Int2Hex(int(cs[1]))}{Int2Hex(int(cs[2]))}'
    if InputType == ColorType.RGB and TargetType == ColorType.Linear:
        return f'{round(int(cs[0]) / 255, 3)},{round(int(cs[1]) / 255, 3)},{round(int(cs[2]) / 255, 3)}'
    if InputType == ColorType.Linear and TargetType == ColorType.Hex:
        return f'#{Int2Hex(int(float(cs[0]) * 255))}{Int2Hex(int(float(cs[1]) * 255))}{Int2Hex(int(float(cs[2]) * 255))}'
    if InputType == ColorType.Linear and TargetType == ColorType.RGB:
        return f'{int(float(cs[0]) * 255)},{int(float(cs[1]) * 255)},{int(float(cs[2]) * 255)}'


def ChangeColorType(ev):
    global EXISTING_PANEL_IDS
    global CURRENT_COLOR_TYPE
    if ev.target.value == 'HEX':
        TargetType = ColorType.Hex
    elif ev.target.value == 'RGB':
        TargetType = ColorType.RGB
    else:
        TargetType = ColorType.Linear
    for PID in EXISTING_PANEL_IDS:
        ele = document[f'Panel_{PID}'].children[1]
        ele.value = convert_colortext(CURRENT_COLOR_TYPE, ele.value, TargetType)
    CURRENT_COLOR_TYPE = TargetType


def DeletePanel(ev):
    global EXISTING_PANEL_IDS
    global ALLOW_EDIT
    EXISTING_PANEL_IDS.remove(int(ev.target.parentElement.id.split('_')[1]))
    del (document[ev.target.parentElement.id])


def HideBadge():
    global MOST_RECENT_PANEL
    MOST_RECENT_PANEL.children[2].classList.add('is-hidden')


def CopyOrEditColor(ev):
    global MOST_RECENT_PANEL
    global ALLOW_EDIT
    MOST_RECENT_PANEL = ev.target.parentElement
    if ALLOW_EDIT:
        document['HiddenColorInput'].click()
    else:
        ev.target.select()
        ev.target.setSelectionRange(0, 9999)
        document.execCommand('Copy')
        badge = MOST_RECENT_PANEL.children[2]
        badge.classList.remove('is-hidden')
        timer.set_timeout(HideBadge, 1000)


def SetupColorPanel(ColorText, HexColor, Nid):
    BTN = html.BUTTON(Class="delete is-small is-hidden")
    BTN.bind('click', DeletePanel)
    R = int(HexColor[1:3], 16)
    G = int(HexColor[3:5], 16)
    B = int(HexColor[5:7], 16)
    Luminance = 0.2126 * R + 0.7152 * G + 0.0722 * B
    if Luminance > 120:
        TC = '#000'
    else:
        TC = '#fff'
    ColorDiv = html.INPUT(
        type='text',
        value=ColorText,
        readonly=True,
        style={'background': 'inherit', 'border': 0, 'width': '100%', 'color': TC}
    )
    ColorDiv.bind('click', CopyOrEditColor)
    Badge = html.SPAN('Copied!', Class="badge is-top-right is-info is-hidden")
    O = html.DIV(
        [BTN, ColorDiv, Badge],
        Class="notification",
        id=f'Panel_{Nid}',
        style={
            'margin-bottom': '0.5rem',
            'background-color': HexColor,
        }
    )
    # O.draggable = True
    O.bind('mouseover', MouseOver)
    O.bind('dragstart', DragStart)
    return O


def ChangeThisPanelColor(ev):
    global MOST_RECENT_PANEL
    global CURRENT_COLOR_TYPE
    MOST_RECENT_PANEL.style['background-color'] = ev.target.value
    MOST_RECENT_PANEL.children[1].value = convert_colortext(ColorType.Hex, ev.target.value, CURRENT_COLOR_TYPE)


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
            ele.draggable = True
            ele.children[0].classList.remove('is-hidden')
    else:
        for ID in EXISTING_PANEL_IDS:
            ele = document[f'Panel_{ID}']
            ele.draggable = False
            ele.children[0].classList.add('is-hidden')


document['EditableSwitch'].bind('change', ToggleAllowEdit)


def InitPage(ev):
    document['EditableSwitch'].checked = False
    print('page is reloaded')


document <= html.DIV(id='HiddenTrigger', Class="is-hidden")
document['HiddenTrigger'].bind('click', InitPage)
document['HiddenTrigger'].click()
document <= html.INPUT(type="color", Class="is-hidden", id='HiddenColorInput')
document['HiddenColorInput'].bind('change', ChangeThisPanelColor)

ele = document['DisplayType']
if ele.value == 'RGB':
    CURRENT_COLOR_TYPE = ColorType.RGB
elif ele.value == 'HEX':
    CURRENT_COLOR_TYPE = ColorType.Hex
else:
    CURRENT_COLOR_TYPE = ColorType.Linear
