from enum import Enum

class Stage(Enum):
  NIGHT = 0
  DAY   = 1

class Stat(Enum):
  ACTIVE = 0
  DEAD   = 1

class Result(Enum):
  NOTDONE     = 0
  WOLFWIN     = 1
  VILLAGERWIN = 2
  TIE         = 3

class Role(Enum):
  WOLF         = "wolf"     # soi
  DOCTOR       = "doctor"   # bao ve
  VILLAGER     = "villager" # dan lang
  SEER         = "seer"     # tien tri
  WITCH        = "witch"    # phu thuy


class Player:
  def __init__(self, name, stat=Stat.ACTIVE):
    self.role = None
    self.name = name
    self.stat = stat
        
  def set_name(self, name): self.name = name
  def set_stat(self, stat): self.stat = stat
  def set_role(self, role): self.role = role


class Warewolf:
  def __init__(self):
    self.players = {}
    self.stage  = Stage.NIGHT
    self.rounds = 0
    self.player = None

  def add_player(self, name):
    self.players[name] = Player(name)

  def set_player_role(self, name, role):
    for player in self.players:
      if player.name == name:
        player.set_role(role)
        break

  def reset(self):
    self.state = Stage.NIGHT
    self.rounds = 0
    self.player = self.players[self.players.keys()[0]]
    for player in self.players:
      player.set_stat(Stat.ACTIVE)

  def is_done(self):
    num_alive_villagers = 0
    num_alive_wolves    = 0
    for player in self.players:
      if player.stat == Stat.DEAD: continue
      if player.role == Role.WOLF: num_alive_wolves += 1
      else:                     num_alive_villagers += 1
    
    if num_alive_villagers <= num_alive_wolves: return Result.WOLFWIN
    if num_alive_wolves==0 and num_alive_villagers>0: Result.VILLAGERWIN
    if num_alive_wolves==0 and num_alive_villagers==0: Result.TIE
    return Result.NOTDONE
