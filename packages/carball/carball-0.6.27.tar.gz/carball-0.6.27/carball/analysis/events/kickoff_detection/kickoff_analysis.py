import logging
from typing import Dict, Callable
import pandas as pd

from carball.generated.api import game_pb2
from carball.generated.api.player_pb2 import Player
from carball.generated.api.stats.kickoff_pb2 import KickoffStats
from carball.generated.api.stats import kickoff_pb2 as kickoff
from carball.json_parser.game import Game


logger = logging.getLogger(__name__)


class BaseKickoff:

    @staticmethod
    def get_kickoffs_from_game(game: Game, proto_game: game_pb2, id_creation:Callable,
                               player_map: Dict[str, Player],
                               data_frame: pd.DataFrame, kickoff_frames: pd.DataFrame,
                               first_touch_frames: pd.DataFrame) -> Dict[int, KickoffStats]:
        kickoffs = dict()
        for index,frame in enumerate(kickoff_frames):
            cur_kickoff = proto_game.game_stats.kickoff_stats.add()
            end_frame = first_touch_frames[index]
            cur_kickoff.touch
            cur_kickoff.start_frame = frame
            cur_kickoff.touch_frame = end_frame
            cur_kickoff.touch_time  = data_frame['game']['delta'][frame:end_frame].sum()
            for player in player_map.values():
                kPlayer = cur_kickoff.touch.players.add()
                kPlayer.player.id = player.id.id
                kPlayer.kickoff_position = BaseKickoff.get_kickoff_position(player, data_frame, frame)
                kPlayer.touch_position = BaseKickoff.get_touch_position(player, data_frame, frame, end_frame)
                kPlayer.boost = data_frame[player.name]['boost'][end_frame]
                kPlayer.ball_dist  = BaseKickoff.get_dist(data_frame, player.name, end_frame)
                kPlayer.player_position.pos_x = data_frame[player.name]['pos_x'][end_frame]
                kPlayer.player_position.pos_y = data_frame[player.name]['pos_y'][end_frame]
                kPlayer.player_position.pos_z = data_frame[player.name]['pos_z'][end_frame]
                BaseKickoff.set_jumps(kPlayer, player, data_frame, frame, end_frame)
            cur_kickoff.type = BaseKickoff.get_kickoff_type(cur_kickoff.touch.players)
            kickoffs[frame] = cur_kickoff
        return kickoffs

    @staticmethod
    def set_jumps(kPlayer, player, data_frame, frame, end_frame):
        jump_active_df        = data_frame[player.name]['jump_active']
        double_jump_active_df = data_frame[player.name]['double_jump_active']
        boost = False
        if 'boost_collect' in data_frame[player.name].keys():
            boost = True
            collected_boost_df    = data_frame[player.name]['boost_collect']
        # check the kickoff frames (and then some) for jumps & big boost collection
        for f in range(frame, min(end_frame + 20, len(data_frame))):
            if boost:
                if collected_boost_df[f] == True:
                    kPlayer.boost_time = data_frame['game']['delta'][frame:f].sum()
            if jump_active_df[f] != jump_active_df[f-1] or double_jump_active_df[f] != double_jump_active_df[f-1]:
                kPlayer.jumps.append(data_frame['game']['delta'][frame:f].sum())

    @staticmethod
    def get_kickoff_type(players: list):
        #
        diagonals = [player.kickoff_position for player in players].count(0)
        offcenter = [player.kickoff_position for player in players].count(1)
        goalies   = [player.kickoff_position for player in players].count(2)
        if len(players) == 6:
            # 3's
            if diagonals == 4:
                if offcenter == 2:
                    return kickoff.THREES_DIAG_DIAG_OFFCENT
                if goalies == 2:
                    return kickoff.THREES_DIAG_DIAG_GOAL
            if diagonals == 2:
                if offcenter == 4:
                    return kickoff.THREES_DIAG_OFFCENT_OFFCENT
                if offcenter == 2:
                    return kickoff.THREES_DIAG_OFFCENT_GOAL
            if offcenter == 4:
                return kickoff.THREES_OFFCENT_OFFCENT_GOAL
        if len(players) == 4:
            if diagonals == 4:
                return kickoff.TWOS_DIAG_DIAG
            if diagonals == 2:
                if offcenter == 2:
                    return kickoff.TWOS_DIAG_OFFCENT
                if goalies == 2:
                    return kickoff.TWOS_DIAG_GOAL
            if offcenter == 4:
                return kickoff.TWOS_OFFCENT_OFFCENT
            if offcenter == 2:
                if goalies == 2:
                    return kickoff.TWOS_OFFCENT_GOAL
        if len(players) == 2:
            if diagonals == 2:
                return kickoff.DUEL_DIAG
            if offcenter == 2:
                return kickoff.DUEL_OFFCENT
            if goalies == 2:
                return kickoff.DUEL_GOAL
        return kickoff.UNKNOWN_KICKOFF_TYPE

    @staticmethod
    def get_kickoff_position(player_class: Player, data_frame: pd.DataFrame, frame: int):
        player = player_class.name
        player_df = data_frame[player]
        if abs(abs(player_df['pos_x'][frame]) - 2050) < 100:
            return kickoff.DIAGONAL
        if abs(abs(player_df['pos_x'][frame]) - 256) < 100:
            return kickoff.OFFCENTER
        if abs(abs(player_df['pos_x'][frame])) < 4:
            return kickoff.GOALIE
        return kickoff.UNKNOWN_KICKOFF_POS

    @staticmethod
    def get_dist(data_frame: pd.DataFrame, player: str, frame: int):
        player_df = data_frame[player]
        dist = (player_df['pos_x'][frame]**2 + player_df['pos_y'][frame]**2 + player_df['pos_z'][frame]**2)**(0.5)
        return dist

    @staticmethod
    def get_afk(data_frame: pd.DataFrame, player: str, frame: int, kick_frame: int):
        player_df = data_frame[player]
        return (player_df['pos_x'][frame] == player_df['pos_x'][kick_frame] and
                player_df['pos_y'][frame] == player_df['pos_y'][kick_frame] and
                player_df['pos_z'][frame] == player_df['pos_z'][kick_frame])

    @staticmethod
    def get_touch_position(player: Player, data_frame: pd.DataFrame, k_frame: int, end_frame: int):
        player_df = data_frame[player.name]
        x = abs(player_df['pos_x'][end_frame])
        y = abs(player_df['pos_y'][end_frame])
        if BaseKickoff.get_dist(data_frame, player.name, end_frame) < 700:
            return kickoff.BALL
        if BaseKickoff.get_afk(data_frame, player.name, end_frame, k_frame):
            return kickoff.AFK
        if (x > 2200) and (y > 3600):
            return kickoff.BOOST
        if (x <500) and (y > 3600):
            return kickoff.GOAL
        if (x <500) and (y < 3600):
            return kickoff.CHEAT
        return kickoff.UNKNOWN_TOUCH_POS
