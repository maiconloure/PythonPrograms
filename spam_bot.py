import pyautogui
import time
time.sleep(5)

messages = open('chatbot_text.txt', 'r')
for word in messages:
    pyautogui.typewrite(word)
    pyautogui.press('enter')

print()
