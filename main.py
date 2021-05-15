import discord
import os
import random
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()
duel = None


class Player:
  def __init__(self, name, damage=10, spell=None, items=set()):
    self.name = name
    self.health = 100
    self.armor = 0
    self.damage = damage
    self.spell = spell
    self.lifesteal = 0
    self.crit = .05 # crit chance
    self.items = items # set 'bow' in self.items, 'charm' in self.items

class Duel:
  def __init__(self, p1, p2):
    self.p1 = p1
    self.p2 = p2
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
    
    
    damage_dealt = round(attacker.damage * random.uniform(0.5, 1.5)) - defender.armor
    crit = False
    if random.random() < attacker.crit:
      # crittical strike
      damage_dealt *= 2
      crit = True
    
    defender.health -= damage_dealt
    
    message = '%s attacked %s for %s damage' % (attacker.name, defender.name, damage_dealt)
    message += '(critical strike)!\n' if crit else '\n'
    
    if defender.health <= 0:
      return message + '%s wins the duel.' % (attacker.name), True
    return message + "%s's turn.\n%s's remaining health: %s\n%s's remaining health: %s" % (defender.name, attacker.name, attacker.health, defender.name, defender.health), False
  
  def spell(self):
    # use spell
    if self.whose_turn == self.p1:
      attacker = self.p1
      defender = self.p2
      self.whose_turn = self.p2
    else:
      attacker = self.p2
      defender = self.p1
      self.whose_turn = self.p1
    
    if attacker.spell == 'Heal':
      attacker.health += 10
    elif attacker.spell == 'Lightning Bolt':
      defender.health -= 10


@client.event
async def on_ready():
  print('%s connected to discord!' % client.user)

@client.event
async def on_reaction_add(reaction, user):
  if not duel or user == client.user or not reaction.message.content.startswith('Choose a spell:'):
    return

  # await reaction.message.channel.send('%s added %s to the message: %s' % (user.name, reaction.emoji, reaction.message.content))
  print('Detected %s reaction from %s' % (reaction.emoji, user.name))
  
  if user.name == duel.p1.name:
    player = duel.p1
  else:
    player = duel.p2
  
  
  if reaction == ":heart:":
    player.spell = 'Heal'
  elif reaction == ":cloud_lightning":
    player.spell = 'Lightning Bolt'
    

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  global duel
  if not duel: # no ongoing duel
    if message.content.startswith('!duel') and message.mentions:
      p1name = message.author.name
      p2name = message.mentions[0].name
      
      # initialize players here
      
      p1 = Player(p1name)
      p2 = Player(p2name)
      duel = Duel(p1, p2)
      # ask p1 to choose a spell using reactions
      

      spells = ['🩹', '⚡'] # https://discordpy.readthedocs.io/en/latest/faq.html#how-can-i-add-a-reaction-to-a-message
      bot_message = await message.channel.send("Choose a spell:\n🩹Heal: +10 HP\n⚡Lightning Bolt: deals 10 damage")
      
      for spell in spells: # assert type(spell) == discord.Emoji
        await bot_message.add_reaction(spell)

      
      # Items = [":crossed_swords:", ":shield:"]
      # https://discordpy.readthedocs.io/en/stable/api.html ctrl+F wait_for
      
      # ask players to choose items
      
      # start new duel
      
      await message.channel.send(":crossed_swords:Duel starting between %s and %s!:crossed_swords:\n%s's turn, %s goes second and gets a +1 damage bonus.\nType !duelhelp for list of commands" % (p1name, p2name, duel.p1.name, duel.p2.name))

  else:
    # ongoing duel
    if message.content == '!duelhelp':
      await message.channel.send('Commands: !attack - attacks the other player\n!spell - use your unique spell')
    elif message.content == '!stats':
      await message.channel.send('Player 1 - name: %s, spell: %s \n Player 2 - name: %s, spell: %s' % (duel.p1.name, duel.p1.spell, duel.p2.name, duel.p2.spell))
    elif message.author.name != duel.whose_turn.name:
      await message.channel.send("It's not your turn.")
    else:
      if message.content == '!attack':
        msg_to_send, game_ended = duel.attack()
        await message.channel.send(msg_to_send)
        if game_ended:
          duel = None
      # elif message.content == '!spell':
      #   msg_to_send, game_ended = duel.spell()
    

# At the start of the game, each player picks 2 items (randomized from a pool), and a spell (randomized)
# each player gets a choice of 2 items offered from the pool, pick one and other player gets the other

# Item ideas (passives) - Armor +armor, Sword +dmg, Bow +atk twice, +lifesteal, +hp, Glove +%crit, charm - %chance to steal X hp
# Spell ideas (actives) - Heal +ignite, Fireball +ignite, Lightning bolt - +30% stun opponent, Smokescreen - +%dodge, Focus +%crit



client.run(os.getenv('token'))