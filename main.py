import time
import badger2040
import qrcode
import os
import time
import state_handling

from global_constants import BATTERY_TIMER, SKEW_LIST, ALTERNATE_GALLERY_SKEWS, MAX_PARTIAL_UPDATES

NUMBER_SKEWS = len(SKEW_LIST)
NUMBER_ALTERNATE_GALLERIES = len(ALTERNATE_GALLERY_SKEWS)

import badge, qrgen, gallery

display = badger2040.Badger2040()


def update_content(state):
    mode = state['mode']
    current_index = state['index']
    skew = state['skew']
    
    if state['partial_updates'] > MAX_PARTIAL_UPDATES:
        state['mode_change'] = True
        state['partial_updates'] = 0
    
    if mode == 'badge':
        badge.draw_badge(current_index, skew, full_update = state['mode_change'])
            
    if mode == 'qr':
        qrgen.draw_qr_file(current_index, skew)
                    
    if mode == 'gallery':
        gallery.show_image(current_index, skew)
        
        
def buttons_abc(state):
    button_a = machine.Pin(badger2040.BUTTON_A).value()
    button_b = machine.Pin(badger2040.BUTTON_B).value()
    button_c = machine.Pin(badger2040.BUTTON_C).value()
    
    if any([button_a, button_b, button_c]):
        state['mode_change'] = True
        state['partial_updates'] = 0
        
        if button_a and not button_c:
            state['mode'] = 'badge'
            
        if button_c and not button_a:
            state['mode'] = 'gallery'
            
        if button_b:
            state['mode'] = 'qr'
            
        if button_a and button_c:
            a_and_c = True
            state['mode'] = 'gallery'
            state['gallery_index'] += 1
            if NUMBER_ALTERNATE_GALLERIES > 0:
                state['gallery_index'] = state['gallery_index'] % NUMBER_ALTERNATE_GALLERIES
                state['skew'] = ALTERNATE_GALLERY_SKEWS[state['gallery_index']]
            else:
                print('Tried to access alternate galleries but none has been defined.')
                pass
        else:
            if state['skew'] in ALTERNATE_GALLERY_SKEWS:
                state['skew'] = SKEW_LIST[0]
                
        state['index'] = 0
        
        return True
    
    return False


def buttons_updown(state):
        
    button_up = machine.Pin(badger2040.BUTTON_UP).value()
    button_down = machine.Pin(badger2040.BUTTON_DOWN).value()
               
    if button_up:
        state['index'] += 1
        state['mode_change'] = False
        state['partial_updates'] += 1
        
    if button_down:
        state['index'] -= 1
        state['mode_change'] = False
        state['partial_updates'] += 1
        
    if button_up and button_down:
        state['mode_change'] = True
        state['partial_updates'] = 0
        
        if state['skew'] in ALTERNATE_GALLERY_SKEWS:
            state['skew'] = SKEW_LIST[0]
        else:
            state['skew_index'] += 1
            state['skew_index'] = state['skew_index'] % NUMBER_SKEWS
            state['skew'] = SKEW_LIST[state['skew_index']]
            
        state['index'] = 0
            
    if button_up or button_down:
        return True

    return False

        
def main_loop():
    state = state_handling.state_defaults()
    if not state_handling.state_load('main', state):
        update_content(state)
        
    start_time = time.time()

    woken_by_button = badger2040.woken_by_button()

    while True:
        
        if woken_by_button:
            start_time = time.time()
            display.led(128)
            woken_by_button = False
            
        if buttons_abc(state) or buttons_updown(state):
            update_content(state)
            start_time = time.time()
            state_handling.state_modify('main', state)
            
        current_time = time.time()

        if current_time - start_time > BATTERY_TIMER:
            display.led(0)
            display.halt()
            
# ------------------------------
#       Main program
# ------------------------------

if __name__ == '__main__':
    main_loop()
