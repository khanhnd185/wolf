from warewolf import Warewolf
from warewolf import Role, Result, Stat

class Runner:
  def __init__(self):
    self.game = Warewolf()
    self.players = []
    
  def get_num_player(self):
    num_player = int(input("Number of players: "))
    return num_player

  def get_player_name(self, m):
    name = input(m)
    return name

  def get_yes_no(self, m):
    yes = input(m)
    return yes in ["yes","Yes","y","Y","OK","Ok","ok"]

  def message(self, m):
    print(m)

  def run(self):
    self.message("Let us start the game!")
    num_player = self.get_num_player()

    self.message("Getting Started...")
    for n in range(num_player):
      name = self.get_player_name(f"Name of player {n+1}: ")
      self.game.add_player(name)
      self.players.append(name)

    self.message("Everyone sleep..")
    for role in [
      Role.DOCTOR
      , Role.WOLF
      , Role.WITCH
      , Role.SEER
    ]:
      self.message(f"{role} wake up.")
      name = self.get_player_name(f"Who is {role}: ")
      
      self.game.set_player_role(name, role)
      self.message(f"{role} sleep.")

    result  = Result.NOTDONE
    night   = 0
    poison  = None
    saved   = None
    while result == Result.NOTDONE:
      cured   = None
      killed  = None
      night  += 1
      self.message(f"\nNight {night}")

      while True:
        if night==1:
          doctor = self.get_player_name("Doctor wake up. ")
          self.game.set_player_role(doctor, Role.DOCTOR)
        else:
          self.message("Doctor wake up. ")
        name = self.get_player_name("Who you will cure: ")
        if name in self.players and name != cured:
          break
      if self.game.is_dead(doctor): cured = name
      self.message("Doctor sleep")

      while True:
        name = self.get_player_name("Wolves wake up. Who you will kill: ")
        if name in self.players and self.game.is_alive(name): break
      killed = name
      self.message("Wolves sleep")

      if self.get_yes_no(f"Witch wake up. {killed} is killed, you wanna save? "):
        if saved == None:
          saved  = killed
          killed = None
      name = self.get_player_name("Who you will poison: ")
      if name in self.players and self.game.is_alive(name):
        if poison == None:
          poison = name
      self.message("Witch sleep")

      while True:
        name = self.get_player_name("Seer wake up. Choose a person to scan: ")
        if name in self.players and self.game.is_alive(name):
          role = Role.WOLF if self.game.is_wolf(name) else Role.VILLAGER
          self.message(f"{name} is a {role}")
          break

      victim = []
      if killed and killed!=cured:
        self.game.kill_player(killed)
        victim.append(killed)
      if poison and poison!=killed:
        self.game.kill_player(poison)
        victim.append(poison)
      self.message(f"Last night {len(victim)} dead. They are {victim}")

      name = self.get_player_name("Let us vote a person to hang: ")
      if name in self.players:
        self.game.kill_player(name)
      result = self.game.is_done()

    self.message(f"{result}")


if __name__ == '__main__':
  runner = Runner()
  runner.run()
