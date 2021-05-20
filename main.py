import discord
from os import getenv
from dotenv import load_dotenv
from player import Player
from duel import Duel

load_dotenv()
client = discord.Client()
duel = None


@client.event
async def on_ready():
    print('%s connected to discord!' % client.user)


@client.event
async def on_reaction_add(reaction, user):
    global duel
    if not duel or user == client.user:
        return

    if reaction.message.content.startswith('Choose a spell:'):
        # await reaction.message.channel.send('%s added %s to the message: %s' % (user.name, reaction.emoji, reaction.message.content))
        if user.name == duel.p1.name:
            player = duel.p1
        else:
            player = duel.p2
        
        if reaction.emoji == '🩹':
            print("Assigning Heal to %s" % user.name)
            player.spell = 'Heal'
        elif reaction.emoji == '⚡':
            print("Assigning Lightning to %s" % user.name)
            player.spell = 'Lightning'
    
    if reaction.message.content.startswith('Choose an item:'):
        if user.name == duel.p1.name:
            player = duel.p1
        else:
            player = duel.p2
        
        if reaction.emoji == '🗡️':
            print("Assigning Sword to %s" % user.name)
            player.items.add('Sword')
        elif reaction.emoji == '🛡️':
            print("Assigning Shield to %s" % user.name)
            player.items.add('Shield')
    
    if duel.both_players_picked():
        await reaction.message.channel.send(":crossed_swords:Duel starting between %s and %s!:crossed_swords:\n%s goes second and gets a +1 extra base damage.\nType !duelhelp for list of commands\n\n**Start of %s's turn**" % (duel.p1.name, duel.p2.name, duel.inactive_player.name, duel.active_player.name))


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
            p1 = Player(p1name, base_damage=10)
            p2 = Player(p2name, base_damage=11)
            duel = Duel(p1, p2)
            if message.mentions[0] == client.user:
                # play against the bot
                duel.p2.spell = 'Heal'
                duel.p2.items.add('Sword')
            
            # Spell ideas (actives) - Heal, Fireball +ignite, Lightning - +30% stun opponent, Smokescreen - +%dodge, Focus +%crit
            spells = ['🩹', '⚡'] # https://discordpy.readthedocs.io/en/latest/faq.html#how-can-i-add-a-reaction-to-a-message
            spell_prompt = await message.channel.send("Choose a spell:\n🩹Heal: +10 HP\n⚡Lightning: deals 10 damage")
            for spell in spells:
                await spell_prompt.add_reaction(spell)

            
            # Item ideas (passives) - Sword +dmg, Shield +armor, Bow +atk twice, +lifesteal, +hp, Glove +%crit, charm - %chance to steal X hp
            items = ['🗡️', '🛡️']
            item_prompt = await message.channel.send("Choose an item:\n🗡️Sword: +3 damage modifier\n🛡️Shield: +3 armor")
            for item in items:
                await item_prompt.add_reaction(item)
            
    else:
        # ongoing duel
        if message.content == '!duelhelp':
            await message.channel.send('Commands:\n!attack - attacks the other player\n!spell - use your unique spell\n!stats - display detailed stats')
        elif message.content == '!stats':
            await message.channel.send(duel.get_stats())
        elif message.author.name != duel.active_player.name:
            await message.channel.send("It's not your turn.")
        else:
            if message.content == '!attack':
                msg_to_send, game_ended = duel.attack()
            elif message.content == '!spell':
                msg_to_send, game_ended = duel.spell()
            
            if not game_ended and duel.active_player.name == client.user.name: # playing against bot
                bot_turn, game_ended = duel.attack()
                msg_to_send += bot_turn
            
            await message.channel.send(msg_to_send)
            if game_ended:
                duel = None


# At the start of the game, each player picks 2 items (randomized from a pool), and a spell (randomized)
# each player gets a choice of 2 items offered from the pool, pick one and other player gets the other
client.run(getenv('token'))