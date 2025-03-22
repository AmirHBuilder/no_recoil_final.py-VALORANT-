import time
import pyautogui
from pynput import mouse
from threading import Thread, Event

# تعریف الگوهای ریکویل برای تفنگ‌های Phantom, Vandal و Spectre
recoil_patterns = {
    "Vandal": [(0, 10), (2, 12), (3, 14), (5, 16)],  # حرکت ماوس به پایین و کمی به راست
    "Phantom": [(0, 8), (1, 10), (2, 12), (3, 14)],   # حرکت ماوس به پایین
    "Spectre": [(0, 5), (1, 6), (2, 7), (3, 8)]       # حرکت ماوس به پایین
}

# Event برای کنترل توقف ریکویل
stop_event = Event()

def no_recoil(weapon_name):
    """
    تابع برای جبران ریکویل تفنگ مورد نظر
    """
    if weapon_name in recoil_patterns:
        pattern = recoil_patterns[weapon_name]
        print(f"Activating No Recoil for {weapon_name}...")
        
        # شلیک و جبران ریکویل
        while not stop_event.is_set():  # تا زمانی که کلیک فشرده است
            for move in pattern:
                if stop_event.is_set():  # اگر کلیک رها شد، متوقف شو
                    break
                x, y = move
                pyautogui.move(x, y, duration=0.1)  # حرکت ماوس برای جبران ریکویل
    else:
        print(f"Weapon {weapon_name} is not supported for No Recoil!")

# انتخاب تفنگ
weapon = "Vandal"  # می‌توانید نام تفنگ را به "Phantom" یا "Spectre" تغییر دهید

# تابع برای تشخیص کلیک ماوس
def on_click(x, y, button, pressed):
    global stop_event, recoil_thread

    if button == mouse.Button.left:
        if pressed:  # اگر کلیک چپ ماوس فشرده شد
            stop_event.clear()  # رویداد توقف را غیرفعال کن
            # اجرای تابع no_recoil در یک thread جداگانه
            recoil_thread = Thread(target=no_recoil, args=(weapon,))
            recoil_thread.start()
        else:  # اگر کلیک چپ ماوس رها شد
            stop_event.set()  # رویداد توقف را فعال کن

# شروع گوش‌دادن به کلیک‌های ماوس
print("Waiting for mouse click...")

# تنظیم Listener
listener = mouse.Listener(on_click=on_click)
listener.start()

# حلقه اصلی برای جلوگیری از بسته‌شدن برنامه
try:
    while listener.is_alive():
        time.sleep(0.1)  # کاهش استفاده از CPU
except KeyboardInterrupt:
    print("Exiting...")
finally:
    listener.stop()