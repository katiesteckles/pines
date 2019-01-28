import evdev
import pygame


class EvDevReader:
    def __init__(self, path):
        self.ir_dev = evdev.InputDevice('/dev/input/event4')
        self.btn_dev = evdev.InputDevice('/dev/input/event5')
        self.x = self.y = 0
        self.button = 0

    def consume_all(self):
        try:
            for event in self.ir_dev.read():
                self.note_event(event)
        except IOError: pass

        try:
            for event in self.btn_dev.read():
                self.note_event(event)
        except IOError: pass

    def note_event(self, event):
        if event.type == evdev.ecodes.EV_ABS:
            if event.code == evdev.ecodes.ABS_HAT0X:
                self.x = 2*(1023.0-event.value)/1023 - 1.0
            elif event.code == evdev.ecodes.ABS_HAT0Y:
                self.y = 2*event.value/767.0 - 1.0
        elif event.type == evdev.ecodes.EV_KEY and event.code == evdev.ecodes.BTN_EAST and event.value:
            print 'got fire'
            self.button += 1

    @property
    def pos(self):
        return self.x, self.y


if __name__ == '__main__':
    edr = EvDevReader('/dev/input/event4')

    pygame.init()
    pygame.joystick.init()
    while True:
        pygame.event.get()
        edr.consume_all()

