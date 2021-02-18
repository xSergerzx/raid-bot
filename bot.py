import psutil
import win32con
import win32gui
from pyautogui import locateOnScreen, click
from time import sleep
from random import randrange

window_name = str(input('Window name: '))
amount_click = int(input('Количество кликов: '))

if amount_click < 0:
    energy = int(input('Количество нужной энергии на 1 проход: '))
    amount_click = int(amount_click / -energy)
    text_amount = str(amount_click)
    print("Будет выполнено " + text_amount + " проходок")
elif amount_click == 0:
    amount_click = 9999999999999999999999999999999999999

sleep(0.5)


# Ищем "Начать" или "Заново" и получаем координаты клика
def locate_button(region):
    for defImg in ["begin.png", "replay.png", "replay_dangeon.png"]:
        ls = locateOnScreen(defImg, region=region, confidence=0.8)
        if not ls:
            continue
        else:
            return [ls.left + ls.width / 2 + randrange(-10, 10, 1), ls.top + ls.height / 2 + randrange(-15, 15, 1)]


def is_real_window(hWnd):
    '''Return True if given window is a real Windows application window.'''
    if not win32gui.IsWindowVisible(hWnd):
        return False
    if win32gui.GetParent(hWnd) != 0:
        return False
    hasNoOwner = win32gui.GetWindow(hWnd, win32con.GW_OWNER) == 0
    lExStyle = win32gui.GetWindowLong(hWnd, win32con.GWL_EXSTYLE)
    if (((lExStyle & win32con.WS_EX_TOOLWINDOW) == 0 and hasNoOwner)
      or ((lExStyle & win32con.WS_EX_APPWINDOW != 0) and not hasNoOwner)):
        if win32gui.GetWindowText(hWnd):
            return True
    return False

def get_window_sizes():
    '''
    Return a list of tuples (handler, (width, height)) for each real window.
    '''
    def callback(hWnd, windows):
        if not is_real_window(hWnd):
            return
        rect = win32gui.GetWindowRect(hWnd)
        windows[win32gui.GetWindowText(hWnd)] = rect
    windows = dict()
    win32gui.EnumWindows(callback, windows)
    return windows



n = 0
while n < amount_click:
    windows_with_position = get_window_sizes()
    if window_name in windows_with_position:
       print(windows_with_position[window_name])
       button = locate_button(windows_with_position[window_name])
       print(button)
       if button is not None:
           click(button)
           n += 1
           print(n)
    sleep(3)
exit()
