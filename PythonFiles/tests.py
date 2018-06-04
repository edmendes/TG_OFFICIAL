from pynput.keyboard import Key, Controller
import time
keyboard = Controller()


time.sleep(3)
keyboard.press(Key.f11)
keyboard.release(Key.f11)