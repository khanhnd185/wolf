from enum import Enum

class Stage(Enum):
  NIGHT_BEGIN  = 0
  DOCTOR_AWAKE = 1
  WOLF_AWAKE   = 2
  WITCH_AWAKE  = 3
  SEER_AWAKE   = 4
  VOTING       = 5
  NUM_STAGES   = 6

class Stat(Enum):
  ALIVE = 0
  DEAD  = 1

class Result(Enum):
  NOTDONE     = "Game is going"
  WOLFWIN     = "Wolf win"
  VILLAGERWIN = "Villager win"
  TIE         = "Tie"

class Role(Enum):
  WOLF         = "wolf"     # soi
  DOCTOR       = "doctor"   # bao ve
  VILLAGER     = "villager" # dan lang
  SEER         = "seer"     # tien tri
  WITCH        = "witch"    # phu thuy


class Player:
  def __init__(self, name
    , stat=Stat.ALIVE
    , role=Role.VILLAGER
  ):
    self.role = role
    self.name = name
    self.stat = stat
        
  def set_name(self, name): self.name = name
  def set_stat(self, stat): self.stat = stat
  def set_role(self, role): self.role = role
  def is_alive(self): return self.stat==Stat.ALIVE
  def is_dead(self) : return self.stat==Stat.DEAD


class Warewolf:
  def __init__(self):
    self.players = {}
    self.names  = []
    self.stage  = Stage.NIGHT_BEGIN
    self.rounds = 0
    self.witch  = None
    self.doctor = None
    self.seer   = None
    self.wolves = []

  def add_player(self, name):
    self.players[name] = Player(name)
    self.names.append(name)

  def set_player_role(self, name, role):
    if name in self.players:
      self.players[name].set_role(role)

      if   role==Role.WITCH : self.witch  = name
      elif role==Role.DOCTOR: self.doctor = name
      elif role==Role.SEER  : self.seer   = name
      elif role==Role.WOLF  : self.wolves.append(name) 

  def kill_player(self, name):
    if name in self.players:
      self.players[name].set_stat(Stat.DEAD)

  def is_alive(self, name):
    if name in self.players:
      return self.players[name].is_alive()
    return False

  def is_dead(self, name):
    if name in self.players:
      return self.players[name].is_dead()
    return True

  def is_valid(self, name):
    if name in self.players:
      return True
    return False

  def is_wolf(self, name):
    return self.players[name].role==Role.WOLF

  def reset(self):
    self.state = Stage.NIGHT_BEGIN
    self.rounds = 0
    for player in self.players:
      player.set_stat(Stat.ALIVE)
      player.set_role(Role.VILLAGER)

  def get_alive(self):
    alive = [name for name,player in self.players.items() if player.stat==Role.ALIVE]

  def is_done(self):
    num_alive_villagers = 0
    num_alive_wolves    = 0
    for player in self.players.values():
      if player.stat == Stat.DEAD: continue
      if player.role == Role.WOLF: num_alive_wolves += 1
      else:                     num_alive_villagers += 1
    
    if num_alive_villagers <= num_alive_wolves: return Result.WOLFWIN
    if num_alive_wolves==0 and num_alive_villagers>0: Result.VILLAGERWIN
    if num_alive_wolves==0 and num_alive_villagers==0: Result.TIE
    return Result.NOTDONE
