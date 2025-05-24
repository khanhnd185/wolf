from warewolf import Warewolf

class Runner:
  def __init__(self):
    self.game = Warewolf()
    
  def run(self):
    
    is_done = False
    
    while not is_done:
      # Do something
      
      is_done = self.game.is_done()