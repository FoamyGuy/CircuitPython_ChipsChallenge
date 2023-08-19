import time

import terminalio
from tiled_game_map import TiledGameMap
from entity import Entity
from displayio import Group, Palette
from vectorio import Rectangle
from adafruit_display_text.bitmap_label import Label
from adafruit_display_text import wrap_text_to_pixels


class ChipsChallengeGame(TiledGameMap):
    def __init__(
            self,
            map_json_file,
            camera_width=15,
            camera_height=15,
            background_default_tile=82,
            entity_default_tile=35,
            player_default_tile=118,
            cursor_default_tile=82,
            empty_map_tile=82,
            use_cursor=False
    ):
        self.game_over = False

        # self.SCORE = 0
        # self.player_property = "player"
        # self.player_entity_class = Player
        self.npc_entity_map = {
            "questionmark": QuestionMark,
            "blue_key": BlueKey,
            "blue_lock": BlueLock,
            "green_key": GreenKey,
            "green_lock": GreenLock,
            "red_key": RedKey,
            "red_lock": RedLock,
            "yellow_key": YellowKey,
            "yellow_lock": YellowLock,
            "fire": Fire,
        }
        self.player_property = "player"
        super().__init__(
            map_json_file,
            camera_width,
            camera_height,
            background_default_tile,
            entity_default_tile,
            player_default_tile,
            cursor_default_tile,
            empty_map_tile,
            use_cursor
        )

        self.showing_q_data = False

        self.inventory = {}

        self.text_dialog_group = Group()
        self.text_dialog_bg_palette = Palette(2)
        self.text_dialog_bg_palette[0] = 0x00ff00
        self.text_dialog_bg_palette[1] = 0x000000
        self.text_dialog_bg_rect = Rectangle(pixel_shader=self.text_dialog_bg_palette, width=200, height=160,
                                             x=320 // 2 - 200 // 2, y=240 // 2 - 160 // 2)

        self.text_dialog_fg_rect = Rectangle(pixel_shader=self.text_dialog_bg_palette, width=192, height=152,
                                             x=320 // 2 - 192 // 2, y=240 // 2 - 152 // 2, color_index=1)

        self.text_dialog_group.append(self.text_dialog_bg_rect)
        self.text_dialog_group.append(self.text_dialog_fg_rect)

        self.text_dialog_lbl = Label(terminalio.FONT, scale=1, color=0x00ee00)

        # self.text_dialog_lbl.text = "\n".join(
        #     wrap_text_to_pixels("It's dangerous, you shouldn't go alone.", 186, terminalio.FONT))
        self.text_dialog_lbl.anchor_point = (0, 0)
        self.text_dialog_lbl.anchored_position = (self.text_dialog_fg_rect.x + 3, self.text_dialog_fg_rect.y + 3)
        self.text_dialog_group.hidden = True
        self.text_dialog_group.append(self.text_dialog_lbl)

        self.append(self.text_dialog_group)

        # self.REMAINING_PELLETES = self.map_obj["tilesets"][0]["tiles"][4]["count"]
        # self.entities[0].direction = Entity.DIRECTION_LEFT

    def show_text(self, text):
        self.text_dialog_lbl.text = "\n".join(wrap_text_to_pixels(text, 186, terminalio.FONT))
        self.text_dialog_lbl.anchor_point = (0, 0)
        self.text_dialog_lbl.anchored_position = (self.text_dialog_fg_rect.x + 3, self.text_dialog_fg_rect.y + 3)
        self.text_dialog_group.hidden = False

    def process_before_move(self, tile_coords, game_obj):
        """
        Calls before_move() on the entity at the given location. Useful for interaction with player and
        other items.
        e.g. Locks will check for keys in inventory and remove 1 if found then allow passage.

        :param tile_coords: dictionary with x and y entries
        :param game_obj: The game context object
        :return: True if the player can walk on this tile. False otherwise.
        """
        for entity in game_obj.entities:
            if entity.at_coords(tile_coords):
                return entity.before_move(game_obj)

        return True

    def process_after_move(self, tile_coords, game_obj):
        """
        Calls before_move() on the entity at the given location. Useful for interaction with player and
        other items.
        e.g. Locks will check for keys in inventory and remove 1 if found then allow passage.

        :param tile_coords: dictionary with x and y entries
        :param game_obj: The game context object
        :return: True if the player can walk on this tile. False otherwise.
        """
        for entity in game_obj.entities:
            if entity.at_coords(tile_coords):
                entity.after_move(game_obj)

    def game_tick(self):
        super().game_tick()

        # for enemy in self.entities:
        #     # print("player loc: ({}, {})".format(my_game.player_entity.x, my_game.player_entity.y))
        #     # print("enemy loc: ({}, {})".format(my_game.player_entity.x, my_game.player_entity.y))
        #     if self.player_entity.is_colliding(enemy):
        #         self.lose_level()


class BlueKey(Entity):
    def __init__(self,
                 bitmap,
                 pixel_shader,
                 width: int = 1,
                 height: int = 1,
                 tile_width: int = 16,
                 tile_height: int = 16,
                 **kwargs):
        super().__init__(bitmap,
                         pixel_shader,
                         width,
                         height,
                         tile_width,
                         tile_height,
                         default_tile=71,
                         **kwargs)

    def game_tick(self, game_obj):
        if self.is_colliding(game_obj.player_entity):
            self.collect_item(game_obj, 'blue_key')


class RedKey(Entity):
    def __init__(self,
                 bitmap,
                 pixel_shader,
                 width: int = 1,
                 height: int = 1,
                 tile_width: int = 16,
                 tile_height: int = 16,
                 **kwargs):
        super().__init__(bitmap,
                         pixel_shader,
                         width,
                         height,
                         tile_width,
                         tile_height,
                         default_tile=70,
                         **kwargs)

    def game_tick(self, game_obj):
        if self.is_colliding(game_obj.player_entity):
            self.collect_item(game_obj, 'red_key')


class YellowKey(Entity):
    def __init__(self,
                 bitmap,
                 pixel_shader,
                 width: int = 1,
                 height: int = 1,
                 tile_width: int = 16,
                 tile_height: int = 16,
                 **kwargs):
        super().__init__(bitmap,
                         pixel_shader,
                         width,
                         height,
                         tile_width,
                         tile_height,
                         default_tile=72,
                         **kwargs)

    def game_tick(self, game_obj):
        if self.is_colliding(game_obj.player_entity):
            self.collect_item(game_obj, 'yellow_key')


class Lock(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def before_move(self, game_obj):
        print(game_obj.inventory)
        if self.key_type not in game_obj.inventory.keys():
            return False
        else:
            game_obj.inventory[self.key_type] -= 1
            if game_obj.inventory[self.key_type] == 0:
                del game_obj.inventory[self.key_type]

            _entity_index = game_obj.get_index_from_coords(self.map_loc)

            game_obj.map_obj['layers'][2]['data'][_entity_index] = 0
            game_obj.entities.remove(self)
            game_obj.remove(self.tilegrid)

            return True


class BlueLock(Lock):
    def __init__(self,
                 bitmap,
                 pixel_shader,
                 width: int = 1,
                 height: int = 1,
                 tile_width: int = 16,
                 tile_height: int = 16,
                 **kwargs):
        super().__init__(bitmap,
                         pixel_shader,
                         width,
                         height,
                         tile_width,
                         tile_height,
                         default_tile=61,
                         **kwargs)
        self.key_type = 'blue_key'

    def game_tick(self, game_obj):
        pass


class RedLock(Lock):
    def __init__(self,
                 bitmap,
                 pixel_shader,
                 width: int = 1,
                 height: int = 1,
                 tile_width: int = 16,
                 tile_height: int = 16,
                 **kwargs):
        super().__init__(bitmap,
                         pixel_shader,
                         width,
                         height,
                         tile_width,
                         tile_height,
                         default_tile=60,
                         **kwargs)
        self.key_type = 'red_key'

    def game_tick(self, game_obj):
        pass


class YellowLock(Lock):
    def __init__(self,
                 bitmap,
                 pixel_shader,
                 width: int = 1,
                 height: int = 1,
                 tile_width: int = 16,
                 tile_height: int = 16,
                 **kwargs):
        super().__init__(bitmap,
                         pixel_shader,
                         width,
                         height,
                         tile_width,
                         tile_height,
                         default_tile=62,
                         **kwargs)
        self.key_type = 'yellow_key'

    def game_tick(self, game_obj):
        pass


class GreenKey(Entity):
    def __init__(self,
                 bitmap,
                 pixel_shader,
                 width: int = 1,
                 height: int = 1,
                 tile_width: int = 16,
                 tile_height: int = 16,
                 **kwargs):
        super().__init__(bitmap,
                         pixel_shader,
                         width,
                         height,
                         tile_width,
                         tile_height,
                         default_tile=73,
                         **kwargs)

    def game_tick(self, game_obj):
        if self.is_colliding(game_obj.player_entity):
            self.collect_item(game_obj, 'green_key')

            # print(game_obj.map_obj['layers'][2]['data'])
        # print(game_obj.inventory)


class GreenLock(Lock):
    def __init__(self,
                 bitmap,
                 pixel_shader,
                 width: int = 1,
                 height: int = 1,
                 tile_width: int = 16,
                 tile_height: int = 16,
                 **kwargs):
        super().__init__(bitmap,
                         pixel_shader,
                         width,
                         height,
                         tile_width,
                         tile_height,
                         default_tile=63,
                         **kwargs)
        self.key_type = 'green_key'

    def game_tick(self, game_obj):
        pass

    def before_move(self, game_obj):
        print(game_obj.inventory)
        if self.key_type not in game_obj.inventory.keys():
            return False
        else:
            # Green key is not consumed

            _entity_index = game_obj.get_index_from_coords(self.map_loc)

            game_obj.map_obj['layers'][2]['data'][_entity_index] = 0
            game_obj.entities.remove(self)
            game_obj.remove(self.tilegrid)

            return True


class QuestionMark(Entity):
    def __init__(self,
                 bitmap,
                 pixel_shader,
                 width: int = 1,
                 height: int = 1,
                 tile_width: int = 16,
                 tile_height: int = 16,
                 **kwargs):
        super().__init__(bitmap,
                         pixel_shader,
                         width,
                         height,
                         tile_width,
                         tile_height,
                         default_tile=35,
                         **kwargs)

    def game_tick(self, game_obj):

        if self.is_colliding(game_obj.player_entity):
            if not game_obj.showing_q_data:
                print(game_obj.get_layer_property(2, 'qdata'))
                game_obj.showing_q_data = True
        else:
            game_obj.showing_q_data = False


class Fire(Entity):
    ANIM_DELAY = 0.3
    ANIM_INDEXES = (29, 30, 31)

    def __init__(self,
                 bitmap,
                 pixel_shader,
                 width: int = 1,
                 height: int = 1,
                 tile_width: int = 16,
                 tile_height: int = 16,
                 **kwargs):
        super().__init__(bitmap,
                         pixel_shader,
                         width,
                         height,
                         tile_width,
                         tile_height,
                         default_tile=29,
                         **kwargs)

        self.anim_meta_index = 0
        self.last_animate_time = 0

    def game_tick(self, game_obj):
        if time.monotonic() > self.last_animate_time + self.ANIM_DELAY:
            self.animate()

    def animate(self):
        self.anim_meta_index += 1
        if self.anim_meta_index >= len(self.ANIM_INDEXES):
            self.anim_meta_index = 0

        self.tilegrid[0] = self.ANIM_INDEXES[self.anim_meta_index]
        self.last_animate_time = time.monotonic()

    def after_move(self, game_obj):
        if "fire_boot" not in game_obj.inventory.keys():
            print("You stepped on fire :(")
            game_obj.game_over = True
            game_obj.show_text("You stepped on fire.\n\nGame Over :(")
