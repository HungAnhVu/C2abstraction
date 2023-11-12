import pyautogui
import time

# Move the mouse to a specific position and click
#pyautogui.moveTo(100, 100, duration=1)  # Move the mouse to XY coordinates over 1 second
#pyautogui.click()  # Click the mouse at its current location

# You can also directly click at a specified location
# pyautogui.click(x=100, y=100)

# To navigate a web page, you might need to scroll
# pyautogui.scroll(200)  # Scroll up
# pyautogui.scroll(-200)  # Scroll down

# Wait for 2 seconds
time.sleep(2)

# You can also perform a double click
# pyautogui.doubleClick(x=100, y=100)

# Use this to find the location of your mouse so that you can use the move command to move it to the right location
while True:
    print(pyautogui.position())
    time.sleep(1)