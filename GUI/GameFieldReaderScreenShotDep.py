import pyautogui
import pygetwindow
from PIL import Image
 
programName = "Mesen"
cL = 195
cR = 165
cT = 150
cB = 70

def readGamefield(field):
    window = pygetwindow.getWindowsWithTitle('Mesen')[0]
    x1 = window.left
    y1 = window.top
    width = window.width
    height = window.height
    x2 = x1+width
    y2 = y1+height

    im = pyautogui.screenshot(region=(x1+cL,y1+cT,width-cR,height-cB))
    #im = myScreenshot.crop((x1+cL,y1+cT,x2-cR,y2-cB))
    
    realCellSizeX = ((x2-cR)-(x1+cL))/10
    realCellSizeY = ((y2-cB)-(y1+cT))/20

    px = im.load()

    #path = 'E:\\0000Schule\\20211001_FRIDAY_TetrisAI\\05 POS\\GUI\\Cool.png'
    #im.save(path)
    #im.show(path)

    print(realCellSizeX)
    print(realCellSizeY)
    print("lal")

    for i in range(0, 20):
        for j in range(0,10):
            c = px[(j*realCellSizeX)+10,(i*realCellSizeY)+10]
           # field[i][j] = 1 if(c== (0,0,0)) else 0
            
readGamefield(1)         

