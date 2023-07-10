import pyautogui
import my_keyboard
import button
from pynput.keyboard import Listener
from pynput import keyboard as kb
from time import sleep
import threading


BUBBLE_PNG = 'bubble.PNG'
REGION_PUZZLE = (933, 497, 42, 357)


class Fishing:
    def __init__(self):
        self.minigame_condition = threading.Event()
        self.start_thread = None
        self.running = True
        self.solving_minigame = False  # Variável para controlar o fluxo das ações

    def use_fishing_rod(self):
        print('using fishing rod')
        pyautogui.moveTo(1153, 816)  # move o mouse ate a posicao da agua
        sleep(0.5)
        my_keyboard.press(button.key['CAPS'])  # usa a fishing rod

    def wait_bubble(self):
        count = 0
        while self.running or not self.solving_minigame: 
            count = count + 1
            if count >= 300:
                return
            bubble = pyautogui.locateOnScreen(BUBBLE_PNG, confidence=0.80, region=(1031, 696, 246, 228))
            print('wait bubble', count, bubble)
            if bubble is not None:
                my_keyboard.press(button.key['CAPS'])
                return

    def resolve_minigame(self):
        self.solving_minigame = False
        while self.running:
            mini_fish = pyautogui.locateOnScreen('peixe.png', confidence=0.80, region=REGION_PUZZLE, grayscale=True)
            my_position = pyautogui.locateOnScreen('barra.png', confidence=0.90, region=REGION_PUZZLE)
            if my_position is not None and mini_fish is not None:
                self.solving_minigame = True
                if my_position.top + 60 > mini_fish.top + 60:
                    my_keyboard.key_down(0x39)
                else:
                    my_keyboard.release_key(0x39)
            else:
                my_keyboard.release_key(0x39)

            if self.solving_minigame and mini_fish is None and my_position is None:
                print('Finished minigame')
                self.solving_minigame = False

    def stop(self):
        self.running = False

    def key_code(self, key):
        if key == kb.Key.end or key == kb.Key.esc:
            self.stop()
            self.minigame_condition.set()
            return False
        if key == kb.Key.home:
            if self.start_thread is None or not self.start_thread.is_alive():
                self.minigame_condition.clear()
                self.start_thread = threading.Thread(target=self.start)
                threading.Thread(target=self.resolve_minigame).start()
                self.start_thread.start()


    def attack_battle(self):
        print('attack_battle')
        while pyautogui.locateOnScreen('battle_empty.PNG', region=(1718, 601, 201, 39), confidence=0.8) is None:
            pyautogui.moveTo(1740, 613)
            if not self.solving_minigame:
                pyautogui.click()
                sleep(1)
                for attack in ['F1', 'F2', 'F3', 'F4', 'F5']:
                    my_keyboard.press(button.key[attack], 1)

    def start(self):
        while self.running:
            if not self.solving_minigame:  # Executa as ações do método start apenas se o minigame estiver concluído
                fish.use_fishing_rod()
                fish.wait_bubble()
                sleep(2)
                if not self.solving_minigame:
                    fish.attack_battle()
                my_keyboard.press(button.key['F12'])
            else:
                print('trying minigame...')


fish = Fishing()
with Listener(on_press=fish.key_code) as listener:
    listener.join()