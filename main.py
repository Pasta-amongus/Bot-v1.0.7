try:
    import asyncio
    import sys
    import os
    import time
    import datetime

    import json
    from functools import partial
    from keep_alive import keep_alive

    import random as rand

    from colorama import Fore, Back, Style, init

    init(autoreset=True)

    import fortnitepy
    from fortnitepy.ext import commands
    import BenBotAsync
    import aiohttp
    import requests

except ModuleNotFoundError as e:
    print(e)
    print(
        Fore.LIGHTYELLOW_EX
        + " • "
        + Fore.RESET
        + 'Failed to import 1 or more modules. Run "INSTALL PACKAGES.bat'
    )
    exit()

os.system("cls||clear")

intro = (
    Fore.LIGHTBLUE_EX
    + """ 
   
███████╗██╗██████╗░███████╗░██████╗░██╗░░░░░██╗████████╗░█████╗░██╗░░██╗███████╗░██████╗
██╔════╝██║██╔══██╗██╔════╝██╔════╝░██║░░░░░██║╚══██╔══╝██╔══██╗██║░░██║██╔════╝██╔════╝
█████╗░░██║██████╔╝█████╗░░██║░░██╗░██║░░░░░██║░░░██║░░░██║░░╚═╝███████║█████╗░░╚█████╗░
██╔══╝░░██║██╔══██╗██╔══╝░░██║░░╚██╗██║░░░░░██║░░░██║░░░██║░░██╗██╔══██║██╔══╝░░░╚═══██╗
██║░░░░░██║██║░░██║███████╗╚██████╔╝███████╗██║░░░██║░░░╚█████╔╝██║░░██║███████╗██████╔╝
╚═╝░░░░░╚═╝╚═╝░░╚═╝╚══════╝░╚═════╝░╚══════╝╚═╝░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝╚══════╝╚═════╝░
                                                                    
 """
)

print(intro)


def lenPartyMembers():
    members = client.party.members
    return len(members)


def warn(*args, **kwargs):
    pass


import warnings

warnings.warn = warn


def lenFriends():
    friends = client.friends
    return len(friends)


def getNewSkins():
    r = requests.get("https://benbotfn.tk/api/v1/files/added")

    response = r.json()

    cids = []

    for cid in [
        item for item in response if item.split("/")[-1].upper().startswith("CID_")
    ]:
        cids.append(cid.split("/")[-1].split(".")[0])

    return cids


def getNewEmotes():
    r = requests.get("https://benbotfn.tk/api/v1/files/added")

    response = r.json()

    eids = []

    for cid in [
        item for item in response if item.split("/")[-1].upper().startswith("EID_")
    ]:
        eids.append(cid.split("/")[-1].split(".")[0])

    return eids


def get_device_auth_details():
    if os.path.isfile("auths.json"):
        with open("auths.json", "r") as fp:
            return json.load(fp)
    else:
        with open("auths.json", "w+") as fp:
            json.dump({}, fp)
    return {}


def store_device_auth_details(email, details):
    existing = get_device_auth_details()
    existing[email] = details

    with open("auths.json", "w") as fp:
        json.dump(existing, fp)


with open("config.json") as f:
    try:
        data = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print(
            Fore.LIGHTYELLOW_EX
            + " [ERROR] "
            + Fore.RESET
            + "There was an error in one of the bot's files! (config.json). If you have problems trying to fix it, contact support."
        )
        print(Fore.LIGHTYELLOW_EX + f"\n {e}")
        exit(1)


with open("config.json") as f:
    try:
        info = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print(
            Fore.LIGHTYELLOW_EX
            + " [ERROR] "
            + Fore.RESET
            + "There was an error in one of the bot's files! (info.json) If you have problems trying to fix it, contact support."
        )
        print(Fore.LIGHTYELLOW_EX + f"\n {e}")
        exit(1)


def is_admin():
    async def predicate(ctx):
        return ctx.author.id in info["FullAccess"]

    return commands.check(predicate)


device_auth_details = get_device_auth_details().get(data["email"], {})

prefix = data["prefix"]

client = commands.Bot(
    command_prefix=prefix,
    case_insensitive=True,
    auth=fortnitepy.AdvancedAuth(
        email=data["email"],
        password=data["password"],
        prompt_authorization_code=True,
        delete_existing_device_auths=True,
        **device_auth_details,
    ),
    platform=fortnitepy.Platform(data["platform"]),
)





@client.event
async def event_device_auth_generate(details, email):
    store_device_auth_details(email, details)


@client.event
async def event_ready():
    
    os.system("cls||clear")
    print(intro)
    print(
        Fore.LIGHTBLUE_EX
        + " • "
        + Fore.RESET
        + "Client is called "
        + Fore.LIGHTBLUE_EX
        + f"{client.user.display_name}"
    )

    member = client.party.me

    await member.edit_and_keep(
        partial(fortnitepy.ClientPartyMember.set_outfit, asset=data["cid"]),
        partial(fortnitepy.ClientPartyMember.set_backpack, asset=data["bid"]),
        partial(fortnitepy.ClientPartyMember.set_pickaxe, asset=data["pid"]),
        partial(
            fortnitepy.ClientPartyMember.set_banner,
            icon=data["banner"],
            color=data["banner_color"],
            season_level=data["level"],
        ),
        partial(
            fortnitepy.ClientPartyMember.set_battlepass_info,
            has_purchased=True,
            level=data["bp_tier"],
        ),
    )

    client.set_avatar(
        fortnitepy.Avatar(
            asset=data["avatar"], background_colors=["#ffffff", "#2E8B57", "#7FFF00"]
        )
    )


@client.event
async def event_party_invite(invite):
    if data["joinoninvite"].lower() == "true":
        try:
            await invite.accept()
            print(
                Fore.LIGHTBLUE_EX
                + " • "
                + Fore.RESET
                + "Accepted party invite from"
                + Fore.LIGHTBLUE_EX
                + f"{invite.sender.display_name}"
            )
        except Exception:
            pass
    elif data["joinoninvite"].lower() == "false":
        if invite.sender.id in info["FullAccess"]:
            await invite.accept()
            print(
                Fore.LIGHTBLUE_EX
                + " • "
                + Fore.RESET
                + "Accepted party invite from "
                + Fore.LIGHTBLUE_EX
                + f"{invite.sender.display_name}"
            )
        else:
            print(
                Fore.LIGHTBLUE_EX
                + " • "
                + Fore.RESET
                + "Never accepted party invite from "
                + Fore.LIGHTBLUE_EX
                + f"{invite.sender.display_name}"
            )


@client.event
async def event_friend_request(request):
    if data["friendaccept"].lower() == "true":
        try:
            await request.accept()
            print(
                f" • Accepted friend request from {request.display_name}"
                + Fore.LIGHTBLACK_EX
                + f" ({lenFriends()})"
            )
        except Exception:
            pass
    elif data["friendaccept"].lower() == "false":
        if request.id in info["FullAccess"]:
            try:
                await request.accept()
                print(
                    Fore.LIGHTBLUE_EX
                    + " • "
                    + Fore.RESET
                    + "Accepted friend request from "
                    + Fore.LIGHTBLUE_EX
                    + f"{request.display_name}"
                    + Fore.LIGHTBLACK_EX
                    + f" ({lenFriends()})"
                )
            except Exception:
                pass
        else:
            print(f" • Never accepted friend request from {request.display_name}")

banned = []

@client.event
async def event_party_message(message: fortnitepy.PartyMessage):
    if message.content == "" and client.party.me.leader:
        await message.author.kick()
        banned.append(message.author.id)
@client.event
async def event_party_member_confirm(confirmation: fortnitepy.PartyJoinConfirmation):
    if confirmation.user.id not in banned:
        await confirmation.accept()

banned = []

@client.event
async def event_party_message(message: fortnitepy.PartyMessage):
    if message.content == "Heyy :bruh)                                                                                                                                For your own bot:                                                                                                                                : Youtube: LupusLeaks                                                                                                                                - TikTok: LupusLeaks                                                                                                                                -Instagram: LupusLeaks                                                                                                                                -Discord: https://ezfn.net/discord"and client.party.me.leader:
        await message.author.kick()
        banned.append(message.author.id)

@client.event
async def event_party_member_confirm(confirmation: fortnitepy.PartyJoinConfirmation):
    if confirmation.user.id not in banned:
        await confirmation.accept()

@client.event
async def event_party_member_join(member: fortnitepy.PartyMember) -> None:
    
    await client.party.send(
        f"Thanks for using our Bot!"
    )
    await client.party.me.set_emote(asset="EID_Accolades")
    await asyncio.sleep(5.25)
    await client.party.me.clear_emote()
    await client.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

@client.event
async def event_party_member_confirm(confirmation):
    if confirmation.user.id in client.blocked_users:
        await confirmation.reject()
    else:
        await confirmation.confirm()


@client.event
async def event_party_member_leave(member):
    
    await client.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
    if client.user.display_name != member.display_name:
        try:
            print(
                Fore.LIGHTYELLOW_EX
                + f" • {member.display_name}"
                + Fore.RESET
                + " has left the lobby."
                + Fore.LIGHTBLACK_EX
                + f" ({lenPartyMembers()})"
            )
        except fortnitepy.HTTPException:
            pass


@client.event
async def event_party_message(message):
    if message.author.id in info["FullAccess"]:
        name = Fore.LIGHTBLUE_EX + f"{message.author.display_name}"
    else:
        name = Fore.RESET + f"{message.author.display_name}"
    print(Fore.GREEN + " • [Party] " + f"{name}" + Fore.RESET + f": {message.content}")


@client.event
async def event_friend_message(message):
    if message.author.id in info["FullAccess"]:
        name = Fore.LIGHTMAGENTA_EX + f"{message.author.display_name}"
    else:
        name = Fore.RESET + f"{message.author.display_name}"
    print(
        Fore.LIGHTMAGENTA_EX
        + " • [Whisper] "
        + f"{name}"
        + Fore.RESET
        + f": {message.content}"
    )

    if message.content.upper().startswith("CID_"):
        await client.party.me.set_outfit(asset=message.content.upper())
        await message.reply(f"Skin set to: {message.content}")
    elif message.content.upper().startswith("BID_"):
        await client.party.me.set_backpack(asset=message.content.upper())
        await message.reply(f"Backpack set to: {message.content}")
    elif message.content.upper().startswith("EID_"):
        await client.party.me.set_emote(asset=message.content.upper())
        await message.reply(f"Emote set to: {message.content}")
    elif message.content.upper().startswith("PID_"):
        await client.party.me.set_pickaxe(asset=message.content.upper())
        await message.reply(f"Pickaxe set to: {message.content}")
    elif message.content.startswith("Playlist_"):
        try:
            await client.party.set_playlist(playlist=message.content)
            await message.reply(f"Playlist set to: {message.content}")
        except fortnitepy.Forbidden:
            await message.reply(
                f"I can not set gamemode because I am not party leader."
            )
    elif message.content.lower().startswith("prefix"):
        await message.reply(f"Current prefix: !")


@client.event
async def event_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"")
    elif isinstance(error, IndexError):
        pass
    elif isinstance(error, fortnitepy.HTTPException):
        pass
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("")
    elif isinstance(error, TimeoutError):
        await ctx.send("You took too long to respond!")
    else:
        print(error)

@client.command()
async def hi(ctx):
    await ctx.send('Hello')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#Gold-style
    
@client.command()
async def goldcat(ctx):
    variants = client.party.me.create_variants(progressive=4)

    await client.party.me.set_outfit(
        asset='CID_693_Athena_Commando_M_BuffCat',
        variants=variants,
        enlightenment=(2, 350)
    )

    await ctx.send('Skin set to: Golden cat')
    
@client.command()
async def goldtnt(ctx):
    variants = client.party.me.create_variants(progressive=8)

    await client.party.me.set_outfit(
        asset='CID_691_Athena_Commando_F_TNTina',
        variants=variants,
        enlightenment=(2, 350)
    )

    await ctx.send('Skin set to: Golden Tntina')
    
@client.command()
async def goldpeely(ctx):
    variants = client.party.me.create_variants(progressive=4)

    await client.party.me.set_outfit(
        asset='CID_701_Athena_Commando_M_BananaAgent',
        variants=variants,
        enlightenment=(2, 350)
    )

    await ctx.send('Skin set to: Golden Peely')
    
@client.command()
async def goldskye(ctx):
    variants = client.party.me.create_variants(progressive=4)

    await client.party.me.set_outfit(
        asset='CID_690_Athena_Commando_F_Photographer',
        variants=variants,
        enlightenment=(2, 350)
    )

    await ctx.send('Skin set to: Golden Skye')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#GOLD SEASON 14 style-skin

    
@client.command()
async def thor2(ctx):
    variants = client.party.me.create_variants(progressive=2)

    await client.party.me.set_outfit(
        asset='CID_845_Athena_Commando_M_HightowerTapas',
        variants=variants,
        enlightenment=(2, 350)
    )

    await ctx.send('Skin set to: lightning thor')
    
    
    
    
    
    
    
    
    
    
    
    
    
#style-skin
@client.command()
async def pinkghoul(ctx):
    variants = client.party.me.create_variants(material=3)

    await client.party.me.set_outfit(
        asset='CID_029_Athena_Commando_F_Halloween',
        variants=variants
    )

    await ctx.send('Skin set to: Pink ghoul')
@client.command()
async def purpleskull(ctx):
    variants = client.party.me.create_variants(clothing_color=1)

    await client.party.me.set_outfit(
        asset='CID_030_Athena_Commando_M_Halloween',
        variants=variants
    )

    await ctx.send('Skin set to: purple skull')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# customize command

    
@client.command()
async def fruit(ctx):
    await client.party.me.set_outfit(
        asset='CID_764_Athena_Commando_F_Loofah'
    )
    
    await ctx.send("Skin set to: Loserfruit")
    await client.party.me.set_emote(
        asset='EID_Loofah'
    )
    
    await ctx.send("")
    

    
@client.command()
async def witch(ctx):
    await client.party.me.set_outfit(
        asset='CID_608_Athena_Commando_F_ModernWitch'
    )
    
    await ctx.send("Skin set to: witch")
    
@client.command()
async def bot(ctx):
    await client.party.me.set_outfit(
        asset='CID_NPC_Athena_Commando_M_HightowerHenchman'
    )
    
    await ctx.send("Skin set to: bot")

@client.command()
async def jules2(ctx):
    await client.party.me.set_outfit(
        asset='CID_A_077_Athena_Commando_F_ArmoredEngineer'
    )
    
    await ctx.send("Skin set to: Scrapknight Jules")



# basic commands
@client.command()
async def skin(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No skin was given, try: {prefix}skin (skin name)')
    elif content.upper().startswith('CID_'):
        await client.party.me.set_outfit(asset=content.upper())
        await ctx.send(f'Skin set to: {content}')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                name=content,
                backendType="AthenaCharacter"
            )
            await client.party.me.set_outfit(asset=cosmetic.id)
            await ctx.send(f'Skin set to: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a skin named: {content}')


@client.command()
async def backpack(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No backpack was given, try: {prefix}backpack (backpack name)')
    elif content.lower() == 'none':
        await client.party.me.clear_backpack()
        await ctx.send('Backpack set to: None')
    elif content.upper().startswith('BID_'):
        await client.party.me.set_backpack(asset=content.upper())
        await ctx.send(f'Backpack set to: {content}')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaBackpack"
            )
            await client.party.me.set_backpack(asset=cosmetic.id)
            await ctx.send(f'Backpack set to: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a backpack named: {content}')


@client.command()
async def emote(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No emote was given, try: {prefix}emote (emote name)')
    elif content.lower() == 'floss':
        await client.party.me.clear_emote()
        await client.party.me.set_emote(asset='EID_Floss')
        await ctx.send(f'Emote set to: Floss')
    elif content.lower() == 'none':
        await client.party.me.clear_emote()
        await ctx.send(f'Emote set to: None')
    elif content.upper().startswith('EID_'):
        await client.party.me.clear_emote()
        await client.party.me.set_emote(asset=content.upper())
        await ctx.send(f'Emote set to: {content}')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaDance"
            )
            await client.party.me.clear_emote()
            await client.party.me.set_emote(asset=cosmetic.id)
            await ctx.send(f'Emote set to: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find an emote named: {content}')

@client.command()
async def pickaxe(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No pickaxe was given, try: {prefix}pickaxe (pickaxe name)')
    elif content.upper().startswith('Pickaxe_'):
        await client.party.me.set_pickaxe(asset=content.upper())
        await ctx.send(f'Pickaxe set to: {content}')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaPickaxe"
            )
            await client.party.me.set_pickaxe(asset=cosmetic.id)
            await ctx.send(f'Pickaxe set to: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a pickaxe named: {content}')


@client.command()
async def pet(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No pet was given, try: {prefix}pet (pet name)')
    elif content.lower() == 'none':
        await client.party.me.clear_pet()
        await ctx.send('Pet set to: None')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaPet"
            )
            await client.party.me.set_pet(asset=cosmetic.id)
            await ctx.send(f'Pet set to: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a pet named: {content}')



@client.command()
async def emoji(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No emoji was given, try: {prefix}emoji (emoji name)')
    try:
        cosmetic = await BenBotAsync.get_cosmetic(
            lang="en",
            searchLang="en",
            matchMethod="contains",
            name=content,
            backendType="AthenaEmoji"
        )
        await client.party.me.clear_emoji()
        await client.party.me.set_emoji(asset=cosmetic.id)
        await ctx.send(f'Emoji set to: {cosmetic.name}')
    except BenBotAsync.exceptions.NotFound:
        await ctx.send(f'Could not find an emoji named: {content}')

    

@client.command()
async def current(ctx, setting = None):
    if setting is None:
        await ctx.send(f"Missing argument. Try: {prefix}current (skin, backpack, emote, pickaxe, banner)")
    elif setting.lower() == 'banner':
        await ctx.send(f'Banner ID: {client.party.me.banner[0]}  -  Banner Color ID: {client.party.me.banner[1]}')
    else:
        try:
            if setting.lower() == 'skin':
                    cosmetic = await BenBotAsync.get_cosmetic_from_id(
                        cosmetic_id=client.party.me.outfit
                    )

            elif setting.lower() == 'backpack':
                    cosmetic = await BenBotAsync.get_cosmetic_from_id(
                        cosmetic_id=client.party.me.backpack
                    )

            elif setting.lower() == 'emote':
                    cosmetic = await BenBotAsync.get_cosmetic_from_id(
                        cosmetic_id=client.party.me.emote
                    )

            elif setting.lower() == 'pickaxe':
                    cosmetic = await BenBotAsync.get_cosmetic_from_id(
                        cosmetic_id=client.party.me.pickaxe
                    )

            await ctx.send(f"My current {setting} is: {cosmetic.name}")
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f"I couldn't find a {setting} name for that.")


@client.command()
async def gift(ctx):
    await client.party.me.set_emote(asset="EID_nevergonna")

    await ctx.send(f"What did you think would happen?")
    await asyncio.sleep(10)
    await client.party.me.clear_emote()

@client.command()
async def marvel(ctx):
    await ctx.send(f"All marvel skins with emotes !")
    await ctx.send(f"Thor !")
    await client.party.me.set_backpack(asset="bid_600_hightowertapas")
    await client.party.me.set_outfit(asset="cid_845_athena_commando_m_hightowertapas")
    await client.party.me.set_emote(asset="eid_hightowertapas")
    await asyncio.sleep(3.25)
    await ctx.send(f"She-Hulk !")
    await client.party.me.set_backpack(asset="bid_594_hightowerhoneydew")
    await client.party.me.set_outfit(
        asset="cid_842_athena_commando_f_hightowerhoneydew"
    )
    await client.party.me.set_emote(asset="eid_hightowerhoneydew")
    await asyncio.sleep(3.25)
    await ctx.send(f"Groot !")
    await client.party.me.set_backpack(asset="bid_598_hightowergrape")
    await client.party.me.set_outfit(asset="cid_840_athena_commando_m_hightowergrape")
    await client.party.me.set_emote(asset="eid_hightowergrape")
    await asyncio.sleep(3.25)
    await ctx.send(f"Storm !")
    await client.party.me.set_outfit(asset="cid_839_athena_commando_f_hightowersquash")
    await client.party.me.set_emote(asset="eid_hightowersquash")
    await asyncio.sleep(3.25)
    await ctx.send(f"Doctor Doom !")
    await client.party.me.set_backpack(asset="bid_599_hightowerdate")
    await client.party.me.set_outfit(asset="cid_846_athena_commando_m_hightowerdate")
    await client.party.me.set_emote(asset="eid_hightowerdate")
    await asyncio.sleep(5.25)
    await ctx.send(f"Mystique !")
    await client.party.me.set_backpack(asset="bid_595_hightowermango")
    await client.party.me.set_outfit(asset="cid_844_athena_commando_f_hightowermango")
    await client.party.me.set_emote(asset="eid_hightowermango")
    await asyncio.sleep(2.25)
    await ctx.send(f"Ironman !")
    await client.party.me.set_backpack(asset="bid_596_hightowertomato")
    await client.party.me.set_outfit(
        asset="cid_843_athena_commando_m_hightowertomato_casual"
    )
    await client.party.me.set_emote(asset="eid_hightowertomato")
    await asyncio.sleep(4.25)
    await ctx.send(f"Wolverine !")
    await client.party.me.set_backpack(asset="bid_597_hightowerwasabi")
    await client.party.me.set_outfit(asset="cid_841_athena_commando_m_hightowerwasabi")
    await client.party.me.set_emote(asset="eid_hightowerwasabi")
    await asyncio.sleep(4.25)
    await ctx.send(f"Silver Surfer !")
    await client.party.me.set_backpack(asset="bid_605_soy_y0dw7")
    await client.party.me.set_skin(asset="cid_847_athena_commando_m_soy_2as3cg")
    await ctx.send(
        f"All the marvel skins! "
    )
@client.command()
async def name(ctx, *, content=None):
    if content is None:
        await ctx.send(f'No ID was given, try: {prefix}name (cosmetic ID)')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic_from_id(
                cosmetic_id=content
            )
            await ctx.send(f'The name for that ID is: {cosmetic.name}')
            print(f' [+] The name for {cosmetic.id} is: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a cosmetic name for ID: {content}')



@client.command()
async def cid(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No skin was given, try: {prefix}cid (skin name)')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaCharacter"
            )
            await ctx.send(f'The CID for {cosmetic.name} is: {cosmetic.id}')
            print(f' [+] The CID for {cosmetic.name} is: {cosmetic.id}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a skin named: {content}')
        

@client.command()
async def bid(ctx, *, content):
    if content is None:
        await ctx.send(f'No backpack was given, try: {prefix}bid (backpack name)')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaBackpack"
            )
            await ctx.send(f'The BID for {cosmetic.name} is: {cosmetic.id}')
            print(f' [+] The BID for {cosmetic.name} is: {cosmetic.id}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a backpack named: {content}')



@client.command()
async def eid(ctx, *, content):
    if content is None:
        await ctx.send(f'No emote was given, try: {prefix}eid (emote name)')
    elif content.lower() == 'floss':
        await ctx.send(f'The EID for Floss is: EID_Floss')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaDance"
            )
            await ctx.send(f'The EID for {cosmetic.name} is: {cosmetic.id}')
            print(f' [+] The EID for {cosmetic.name} is: {cosmetic.id}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find an emote named: {content}')



@client.command()
async def pid(ctx, *, content):
    if content is None:
        await ctx.send(f'No pickaxe was given, try: {prefix}pid (pickaxe name)')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaPickaxe"
            )
            await ctx.send(f'The PID for {cosmetic.name} is: {cosmetic.id}')
            print(f' [+] The PID for {cosmetic.name} is: {cosmetic.id}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a pickaxe named: {content}')



@client.command()
async def random(ctx, content = None):

    skins = await BenBotAsync.get_cosmetics(
        lang="en",
        backendType="AthenaCharacter"
    )

    skin = rand.choice(skins)

    backpacks = await BenBotAsync.get_cosmetics(
        lang="en",
        backendType="AthenaBackpack"
    )

    backpack = rand.choice(backpacks)

    emotes = await BenBotAsync.get_cosmetics(
        lang="en",
        backendType="AthenaDance"
    )

    emote = rand.choice(emotes)

    pickaxes = await BenBotAsync.get_cosmetics(
        lang="en",
        backendType="AthenaPickaxe"
    )

    pickaxe = rand.choice(pickaxes)

    
    if content is None:
        me = client.party.me
        await me.set_outfit(asset=skin.id)
        await me.set_backpack(asset=backpack.id)
        await me.set_pickaxe(asset=pickaxe.id)

        await ctx.send(f'Loadout randomly set to: {skin.name}, {backpack.name}, {pickaxe.name}')
    else:
        if content.lower() == 'skin':
            await client.party.me.set_outfit(asset=skin.id)
            await ctx.send(f'Skin randomly set to: {skin.name}')

        elif content.lower() == 'backpack':
            await client.party.me.set_backpack(asset=backpack.id)
            await ctx.send(f'Backpack randomly set to: {backpack.name}')

        elif content.lower() == 'emote':
            await client.party.me.set_emote(asset=emote.id)
            await ctx.send(f'Emote randomly set to: {emote.name}')

        elif content.lower() == 'pickaxe':
            await client.party.me.set_pickaxe(asset=pickaxe.id)
            await ctx.send(f'Pickaxe randomly set to: {pickaxe.name}')

        else:
            await ctx.send(f"I don't know that, try: {prefix}random (skin, backpack, emote, pickaxe - og, exclusive, unreleased")

@client.command()
async def point(ctx, *, content = None):
    if content is None:
        await client.party.me.clear_emote()
        await client.party.me.set_emote(asset='EID_IceKing')
        await ctx.send(f'Pointing with: {client.party.me.pickaxe}')
    
    else:
        if content.upper().startswith('Pickaxe_'):
            await client.party.me.set_pickaxe(asset=content.upper())
            await client.party.me.clear_emote()
            asyncio.sleep(0.25)
            await client.party.me.set_emote(asset='EID_IceKing')
            await ctx.send(f'Pointing with: {content}')
        else:
            try:
                cosmetic = await BenBotAsync.get_cosmetic(
                    lang="en",
                    searchLang="en",
                    matchMethod="contains",
                    name=content,
                    backendType="AthenaPickaxe"
                )
                await client.party.me.set_pickaxe(asset=cosmetic.id)
                await client.party.me.clear_emote()
                await client.party.me.set_emote(asset='EID_IceKing')
                await ctx.send(f'Pointing with: {cosmetic.name}')
            except BenBotAsync.exceptions.NotFound:
                await ctx.send(f'Could not find a pickaxe named: {content}')





@client.command()
async def floss(ctx, *, content=None):
    await client.party.me.set_emote(asset="eid_floss")


@client.command()
async def sit(ctx, *, content=None):
    await client.party.me.set_emote(asset="eid_sitpapayacomms")


@client.command()
async def ninja(ctx):
    await client.party.me.set_skin(asset="cid_605_athena_commando_m_tourbus")
    await client.party.me.set_backpack(asset="bid_402_tourbus")
    await client.party.me.set_emote(asset="eid_tourbus")


@client.command()
async def hologram(ctx):
    await client.party.me.set_outfit(
        asset='CID_VIP_Athena_Commando_M_GalileoGondola_SG'
    )
    
    await ctx.send("Skin set to: Hologram")


@client.command()
async def last(ctx):
    await client.party.me.set_emote(
        asset='EID_TwistEternity'
    )
    
    await ctx.send("Emote set to: Last Forever")


@client.command()
async def new(ctx, content = None):
    newSkins = getNewSkins()
    newEmotes = getNewEmotes()

    previous_skin = client.party.me.outfit

    if content is None:
        await ctx.send(f'There are {len(newSkins) + len(newEmotes)} new skins + emotes')

        for cosmetic in newSkins + newEmotes:
            if cosmetic.startswith('CID_'):
                await client.party.me.set_outfit(asset=cosmetic)
                await asyncio.sleep(4)
            elif cosmetic.startswith('EID_'):
                await client.party.me.clear_emote()
                await client.party.me.set_emote(asset=cosmetic)
                await asyncio.sleep(4)

    elif 'skin' in content.lower():
        await ctx.send(f'There are {len(newSkins)} new skins')

        for skin in newSkins:
            await client.party.me.set_outfit(asset=skin)
            await asyncio.sleep(4)

    elif 'emote' in content.lower():
        await ctx.send(f'There are {len(newEmotes)} new emotes')

        for emote in newEmotes:
            await client.party.me.clear_emote()
            await client.party.me.set_emote(asset=emote)
            await asyncio.sleep(4)

    await client.party.me.clear_emote()
    
    await ctx.send('Done!')

    await asyncio.sleep(1.5)

    await client.party.me.set_outfit(asset=previous_skin)

    if (content is not None) and ('skin' or 'emote' not in content.lower()):
        ctx.send(f"Not a valid option. Try: {prefix}new (skins, emotes)")



@client.command()
async def ready(ctx):
    await client.party.me.set_ready(fortnitepy.ReadyState.READY)
    await ctx.send('Ready!')



@client.command()
async def unready(ctx):
    await client.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
    await ctx.send('Unready!')


@client.command()
async def sitin(ctx):
    await client.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
    await ctx.send('Sitting in')

@client.command()
async def sitout(ctx):
    await client.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
    await ctx.send('Sitting out')


@client.command()
async def tier(ctx, tier = None):
    if tier is None:
        await ctx.send(f'No tier was given. Try: {prefix}tier (tier number)') 
    else:
        await client.party.me.set_battlepass_info(
            has_purchased=True,
            level=tier
        )

        await ctx.send(f'Battle Pass tier set to: {tier}')


@client.command()
async def level(ctx, level = None):
    if level is None:
        await ctx.send(f'No level was given. Try: {prefix}level (number)')
    else:
        await client.party.me.set_banner(season_level=level)
        await ctx.send(f'Level set to: {level}')



@client.command()
async def og(ctx):
    previous_skin = client.party.me.outfit
    variants = client.party.me.create_variants(material=1)

    await client.party.me.set_outfit(
        asset="CID_028_Athena_Commando_F", variants=variants
    )
    await ctx.send(f"Renegade Raider")

    await asyncio.sleep(2.25)
    await client.party.me.set_outfit(
        asset="cid_017_athena_commando_m",
    )
    await ctx.send(f"Aerial Assault Trooper")

    await asyncio.sleep(2.25)
    variants = client.party.me.create_variants(material=3)
    await client.party.me.set_outfit(
        asset="CID_029_Athena_Commando_F_Halloween", variants=variants
    )
    await ctx.send("Pink Ghoul Trooper")

    await asyncio.sleep(2.25)
    variants = client.party.me.create_variants(clothing_color=1)

    await client.party.me.set_outfit(
        asset="CID_030_Athena_Commando_M_Halloween", variants=variants
    )
    await ctx.send("Purple Skull Trooper")

    await asyncio.sleep(2.25)
    await client.party.me.set_outfit(asset=previous_skin)

    await ctx.send(
        f"Season one og skins "
    )

@client.command()
async def banner(ctx, args1 = None, args2 = None):
    if (args1 is not None) and (args2 is None):
        if args1.startswith('defaultcolor'):
            await client.party.me.set_banner(
                color = args1
            )
            
            await ctx.send(f'Banner color set to: {args1}')

        elif args1.isnumeric() == True:
            await client.party.me.set_banner(
                color = 'defaultcolor' + args1
            )

            await ctx.send(f'Banner color set to: defaultcolor{args1}')

        else:
            await client.party.me.set_banner(
                icon = args1
            )

            await ctx.send(f'Banner Icon set to: {args1}')

    elif (args1 is not None) and (args2 is not None):
        if args2.startswith('defaultcolor'):
            await client.party.me.set_banner(
                icon = args1,
                color = args2
            )

            await ctx.send(f'Banner icon set to: {args1} -- Banner color set to: {args2}')
        
        elif args2.isnumeric() == True:
            await client.party.me.set_banner(
                icon = args1,
                color = 'defaultcolor' + args2
            )

            await ctx.send(f'Banner icon set to: {args1} -- Banner color set to: defaultcolor{args2}')

        else:
            await ctx.send(f'Not proper format. Try: {prefix}banner (Banner ID) (Banner Color ID)')


copied_player = ""


@client.command()
async def stop(ctx):
    global copied_player
    if copied_player != "":
        copied_player = ""
        await ctx.send(f'Stopped copying all users.')
        return
    else:
        try:
            await client.party.me.clear_emote()
        except RuntimeWarning:
            pass


@client.command()
async def say(ctx, *, message = None):
    if message is not None:
        await client.party.send(message)
        await ctx.send(f'Sent "{message}" to party chat')
    else:
        await ctx.send(f'No message was given. Try: {prefix}say (message)')



@client.command()
async def admin(ctx, setting = None, *, user = None):
    if (setting is None) and (user is None):
        await ctx.send(f"Missing one or more arguments. Try: {prefix}admin (add, remove, list) (user)")
    elif (setting is not None) and (user is None):

        user = await client.fetch_profile(ctx.message.author.id)

        if setting.lower() == 'add':
            if user.id in info['FullAccess']:
                await ctx.send("You are already an admin")

            else:
                await ctx.send("Password?")
                response = await client.wait_for('friend_message', timeout=20)
                content = response.content.lower()
                if content == data['AdminPassword']:
                    info['FullAccess'].append(user.id)
                    with open('info.json', 'w') as f:
                        json.dump(info, f, indent=4)
                        await ctx.send(f"Correct. Added {user.display_name} as an admin.")
                        print(Fore.GREEN + " [+] " + Fore.LIGHTGREEN_EX + user.display_name + Fore.RESET + " was added as an admin.")
                else:
                    await ctx.send("Incorrect Password.")

        elif setting.lower() == 'remove':
            if user.id not in info['FullAccess']:
                await ctx.send("You are not an admin.")
            else:
                await ctx.send("Are you sure you want to remove yourself as an admin?")
                response = await client.wait_for('friend_message', timeout=20)
                content = response.content.lower()
                if (content.lower() == 'yes') or (content.lower() == 'y'):
                    info['FullAccess'].remove(user.id)
                    with open('info.json', 'w') as f:
                        json.dump(info, f, indent=4)
                        await ctx.send("You were removed as an admin.")
                        print(Fore.BLUE + " [+] " + Fore.LIGHTBLUE_EX + user.display_name + Fore.RESET + " was removed as an admin.")
                elif (content.lower() == 'no') or (content.lower() == 'n'):
                    await ctx.send("You were kept as admin.")
                else:
                    await ctx.send("Not a correct reponse. Cancelling command.")
                
        elif setting == 'list':
            if user.id in info['FullAccess']:
                admins = []

                for admin in info['FullAccess']:
                    user = await client.fetch_profile(admin)
                    admins.append(user.display_name)

                await ctx.send(f"The bot has {len(admins)} admins:")

                for admin in admins:
                    await ctx.send(admin)

            else:
                await ctx.send("You don't have permission to this command.")

        else:
            await ctx.send(f"That is not a valid setting. Try: {prefix}admin (add, remove, list) (user)")
            
    elif (setting is not None) and (user is not None):
        user = await client.fetch_profile(user)

        if setting.lower() == 'add':
            if ctx.message.author.id in info['FullAccess']:
                if user.id not in info['FullAccess']:
                    info['FullAccess'].append(user.id)
                    with open('info.json', 'w') as f:
                        json.dump(info, f, indent=4)
                        await ctx.send(f"Correct. Added {user.display_name} as an admin.")
                        print(Fore.GREEN + " [+] " + Fore.LIGHTGREEN_EX + user.display_name + Fore.RESET + " was added as an admin.")
                else:
                    await ctx.send("That user is already an admin.")
            else:
                await ctx.send("You don't have access to add other people as admins. Try just: !admin add")
        elif setting.lower() == 'remove':
            if ctx.message.author.id in info['FullAccess']:
                if user.id in info['FullAccess']:
                    await ctx.send("Password?")
                    response = await client.wait_for('friend_message', timeout=20)
                    content = response.content.lower()
                    if content == data['AdminPassword']:
                        info['FullAccess'].remove(user.id)
                        with open('info.json', 'w') as f:
                            json.dump(info, f, indent=4)
                            await ctx.send(f"{user.display_name} was removed as an admin.")
                            print(Fore.BLUE + " [+] " + Fore.LIGHTBLUE_EX + user.display_name + Fore.RESET + " was removed as an admin.")
                    else:
                        await ctx.send("Incorrect Password.")
                else:
                    await ctx.send("That person is not an admin.")
            else:
                await ctx.send("You don't have permission to remove players as an admin.")
        else:
            await ctx.send(f"Not a valid setting. Try: {prefix}admin (add, remove) (user)")

  
if (data['email'] and data['password']) and (data['email'] != "" and data['password'] != ""):
    try:
        keep_alive()
        client.run()
    except fortnitepy.errors.AuthException as e:
        print(Fore.LIGHTYELLOW_EX + ' [ERROR] ' + Fore.RESET + f'{e}')
    except ModuleNotFoundError:
        print(e)
        print(Fore.LIGHTYELLOW_EX + f'[-] ' + Fore.RESET + 'Failed to import 1 or more modules. Run "INSTALL PACKAGES.bat')
        exit()
else:
    print(Fore.LIGHTYELLOW_EX + ' [ERROR] ' + Fore.RESET + 'Can not log in, as no accounts credentials were provided.') 

