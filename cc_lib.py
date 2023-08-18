from tiled_game_map import TiledGameMap
from entity import Entity


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
        # self.SCORE = 0
        # self.player_property = "player"
        # self.player_entity_class = Player
        self.npc_entity_map = {
            "questionmark": QuestionMark,
            "blue_key": BlueKey,
            "blue_lock": BlueLock
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

        self.inventory  = {}

        # self.REMAINING_PELLETES = self.map_obj["tilesets"][0]["tiles"][4]["count"]
        # self.entities[0].direction = Entity.DIRECTION_LEFT

    def check_entity_interaction(self, tile_coords, game_obj):
        """
        Checks for entity specific interactions at a certain tile location.
        e.g. Locks will check for keys in inventory and remove 1 if found then allow passage.

        :param tile_coords: dictionary with x and y entries
        :param game_obj: The game context object
        :return: True if the player can walk on this tile. False otherwise.
        """
        for entity in game_obj.entities:
            if entity.at_coords(tile_coords):
                return entity.check_interaction(game_obj)

        return True
    # def game_tick(self):
    #     super().game_tick()
    #     for enemy in self.entities:
    #         # print("player loc: ({}, {})".format(my_game.player_entity.x, my_game.player_entity.y))
    #         # print("enemy loc: ({}, {})".format(my_game.player_entity.x, my_game.player_entity.y))
    #         if self.player_entity.is_colliding(enemy):
    #             self.lose_level()

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
            if "blue_key" in game_obj.inventory.keys():
                game_obj.inventory['blue_key'] += 1
            else:
                game_obj.inventory['blue_key'] = 1

            _player_index = game_obj.get_index_from_coords(game_obj.player_loc)
            print(f"index: {_player_index} value: {game_obj.map_obj['layers'][2]['data'][_player_index]}")
            #print(f"index: {_player_index + 2} value: {game_obj.map_obj['layers'][2]['data'][_player_index + 2 ]}")
            #print(f"index: {_player_index - 2} value: {game_obj.map_obj['layers'][2]['data'][_player_index - 2]}")

            game_obj.map_obj['layers'][2]['data'][_player_index] = 0
            game_obj.entities.remove(self)
            game_obj.remove(self.tilegrid)


            #print(game_obj.map_obj['layers'][2]['data'])
        #print(game_obj.inventory)



class BlueLock(Entity):
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

    def game_tick(self, game_obj):
        pass

    def check_interaction(self, game_obj):
        if "blue_key" not in game_obj.inventory.keys():
            return False
        else:
            game_obj.inventory['blue_key'] -= 1
            if game_obj.inventory['blue_key'] == 0:
                del game_obj.inventory['blue_key']

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
