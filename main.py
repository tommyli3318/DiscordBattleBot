import discord
import os
import random


client = discord.Client()
duel = None


class Player:
  def __init__(self, name, damage=10):
    self.name = name
    self.health = 100
    self.armor = 0
    self.damage = damage

class Duel:
  def __init__(self, p1name, p2name):
    self.p1 = Player(p1name)
    self.p2 = Player(p2name, damage=11)
    self.whose_turn = self.p1 # if random.random() > 0.5 else self.p2
  
  def attack(self):
    if self.whose_turn == self.p1:
      attacker = self.p1
      defender = self.p2
      self.whose_turn = self.p2
    else:
      attacker = self.p2
      defender = self.p1
      self.whose_turn = self.p1
    
    damage_dealt = round(attacker.damage * random.uniform(0.5, 1.5))
    defender.health -= damage_dealt
    if defender.health <= 0:
      return '%s attacked %s for %s damage! %s wins the duel.' % (attacker.name, defender.name, damage_dealt, attacker.name), True
    return "%s attacked %s for %s damage!\n%s's turn.\n%s's HP: %s, %s's HP: %s" % (attacker.name, defender.name, damage_dealt, defender.name, attacker.name, attacker.health, defender.name, defender.health), False
    

@client.event
async def on_ready():
  print('%s connected to discord!' % client.user)

@client.event
async def on_message(message):
  print("Message from %s" % message.author)

  if message.author == client.user:
    return
  
  global duel
  if not duel: # no ongoing duel
    if message.content.startswith('!duel') and message.mentions:
      p1name = message.author.name
      p2name = message.mentions[0].name

      # start new duel
      duel = Duel(p1name, p2name)
      await message.channel.send(":crossed_swords:Duel starting between %s and %s!:crossed_swords:\n%s's turn, %s goes second and gets a +1 damage bonus.\nType !duelhelp for list of commands" % (p1name, p2name, duel.p1.name, duel.p2.name))

  else:
    # ongoing duel
    if message.content == '!duelhelp':
      await message.channel.send('Commands: !attack, !armorup')
    elif message.author.name != duel.whose_turn.name:
      await message.channel.send("It's not your turn.")
    else:
      if message.content == '!attack':
        msg_to_send, game_ended = duel.attack()
        await message.channel.send(msg_to_send)
        if game_ended:
          duel = None



client.run(os.environ['token'])