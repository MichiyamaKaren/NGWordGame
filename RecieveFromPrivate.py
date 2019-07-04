from nonebot import on_command, CommandSession, permission as perm
from .PlayerList import PlayerList, StorePlayer, LoadPlayer


@on_command('setNG', permission=perm.PRIVATE)
async def SetNG(session: CommandSession):
    playerlist: PlayerList = LoadPlayer()
    setterid = session.ctx['user_id']
    setteri = playerlist.Searchid(setterid)
    text = session.current_arg_text.strip()
    if not playerlist.canset:
        await session.send('现在不能设置NG词')
    elif setteri == -1:
        await session.send('你未注册游戏，不能设置')
    elif not text:
        await session.send('NG词不能为空，请重新设置')
    else:
        seti = (setteri + 1) % playerlist.nplayer
        await session.send('你成功设置{}的NG词为“{}”'.format(playerlist.Players[seti].name, text))
        await session.bot.send_group_msg(group_id=playerlist.groupid, message=playerlist.Players[setteri].name + '完成设置')
        if playerlist.SetNG(seti, text):
            bot = session.bot
            await bot.send_group_msg(group_id=playerlist.groupid, message='已完成所有NG词设置')
        StorePlayer(playerlist)
