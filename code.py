import gc

import board
import displayio
from cc_lib import ChipsChallengeGame

import time
import board
from micropython import const
from adafruit_seesaw.seesaw import Seesaw

BUTTON_COOLDOWN = 0.3

BUTTON_X = const(6)
BUTTON_Y = const(2)
BUTTON_A = const(5)
BUTTON_B = const(1)
BUTTON_SELECT = const(0)
BUTTON_START = const(16)
button_mask = const(
    (1 << BUTTON_X)
    | (1 << BUTTON_Y)
    | (1 << BUTTON_A)
    | (1 << BUTTON_B)
    | (1 << BUTTON_SELECT)
    | (1 << BUTTON_START)
)

i2c_bus = board.STEMMA_I2C()  # The built-in STEMMA QT connector on the microcontroller
# i2c_bus = board.I2C()  # Uses board.SCL and board.SDA. Use with breadboard.

seesaw = Seesaw(i2c_bus, addr=0x50)

seesaw.pin_mode_bulk(button_mask, seesaw.INPUT_PULLUP)

last_x = 0
last_y = 0


display = board.DISPLAY

# Make the display context
main_group = displayio.Group()
display.show(main_group)

my_game = ChipsChallengeGame(
    "lvl_0.json",
    camera_width=15,
    camera_height=15
)

main_group.append(my_game)


LAST_BTN_TIME = 0
_cur_player_loc = my_game.player_loc.copy()

print(f"memfree: {gc.mem_free()}")
while True:

    my_game.game_tick()
    x = 1023 - seesaw.analog_read(14)
    y = 1023 - seesaw.analog_read(15)

    if (abs(x - last_x) > 23) or (abs(y - last_y) > 23):
        if time.monotonic() - LAST_BTN_TIME > BUTTON_COOLDOWN:
            #print(x, y)
            if (x < 30):
                print("left")
                _next_loc = {"x": my_game.player_loc['x'] - 1, "y": my_game.player_loc['y']}
                if my_game.is_tile_moveable(_next_loc) and my_game.check_entity_interaction(_next_loc, my_game):
                    my_game.player_loc['x'] -= 1
                    my_game.update_player_location()
                #my_game.player_entity.x -= my_game.player_entity.tilegrid.tile_width
            elif (x > 990):
                _next_loc = {"x": my_game.player_loc['x'] + 1, "y": my_game.player_loc['y']}
                if my_game.is_tile_moveable(_next_loc) and my_game.check_entity_interaction(_next_loc, my_game):
                    my_game.player_loc['x'] += 1
                    my_game.update_player_location()
                print("right")
                #my_game.player_entity.x += my_game.player_entity.tilegrid.tile_width
            if (y < 30):
                print("down")
                _next_loc = {"x": my_game.player_loc['x'], "y": my_game.player_loc['y'] + 1}
                if my_game.is_tile_moveable(_next_loc) and my_game.check_entity_interaction(_next_loc, my_game):
                    my_game.player_loc['y'] += 1
                    my_game.update_player_location()
                #my_game.player_entity.y += my_game.player_entity.tilegrid.tile_width
            elif (y > 990):
                print("up")
                _next_loc = {"x": my_game.player_loc['x'], "y": my_game.player_loc['y'] - 1}
                if my_game.is_tile_moveable(_next_loc) and my_game.check_entity_interaction(_next_loc, my_game):
                    my_game.player_loc['y'] -= 1
                    my_game.update_player_location()
                #my_game.player_entity.y -= my_game.player_entity.tilegrid.tile_width

        last_x = x
        last_y = y

    buttons = seesaw.digital_read_bulk(button_mask)

    if not buttons & (1 << BUTTON_X):
        print("Button x pressed")

    if not buttons & (1 << BUTTON_Y):
        print("Button Y pressed")

    if not buttons & (1 << BUTTON_A):
        print("Button A pressed")

    if not buttons & (1 << BUTTON_B):
        print("Button B pressed")

    if not buttons & (1 << BUTTON_SELECT):
        print("Button Select pressed")

    if not buttons & (1 << BUTTON_START):
        print("Button Start pressed")

    time.sleep(0.01)
