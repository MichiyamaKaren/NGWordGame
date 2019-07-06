import shelve
from typing import List, Tuple


class Player:
    def __init__(self, sender):
        self.id = sender['user_id']
        if sender['card']:
            self.name = sender['card']
        elif sender['nickname']:
            self.name = sender['nickname']
        else:
            self.name = str(self.id)
        self.NGword = ''
        self.ingame = True


class PlayerList:
    def __init__(self, groupid):
        self.Players: List[Player] = []
        self.nplayer = 0
        self.nset = 0  # number of players with NG word already set
        self.canset = False
        self.groupid = groupid

    def Searchid(self, pid):
        for i, p in enumerate(self.Players):
            if p.id == pid:
                return i
        return -1

    def __getitem__(self, pid):
        index = self.Searchid(pid)
        if index == -1:
            return None
        else:
            return self.Players[index]

    def append(self, player: Player):
        if self[player.id] == -1:
            self.Players.append(player)
        self.nplayer += 1

    # tell Players[i] to set NG word for Players[i+1]
    def SetPrompt(self) -> List[Tuple[int, str]]:
        prompt = []
        for i, p in enumerate(self.Players):
            msgi = '设置{}的NG词，指令：\nsetNG NG词\n可以覆盖设定' \
                .format(self.Players[(i + 1) % self.nplayer].name)
            prompt.append((p.id, msgi))
        return prompt

    # returns True if all players are set
    def SetNG(self, i, NG) -> bool:
        if not self.Players[i].NGword:
            self.nset += 1
        self.Players[i].NGword = NG.lower()
        return self.nset == self.nplayer

    def CheckText(self, pid, text):
        p = self[pid]
        if p and p.ingame and p.NGword in text.lower():
            return p
        else:
            return None

    def ExitGame(self, pid):
        self[pid].ingame = False
        self.nplayer -= 1

    def Winner(self):
        for p in self.Players:
            if p.ingame:
                return p
        # 只有一个人玩时会出现此状况，debug用
        return Player({'user_id': 0, 'card': 'nobody'})

    def PrintPlayers(self, seperate: str = '\n') -> str:
        return seperate.join([p.name for p in self.Players])

    def PrintNG(self, mask=-1) -> str:
        return '\n'.join(p.name + '：' + p.NGword for i, p in enumerate(self.Players) if i != mask)


def StorePlayer(playerlist: PlayerList):
    players = shelve.open('plugins/NGWordGame/players')
    players['playerlist'] = playerlist
    players.close()


def LoadPlayer() -> PlayerList:
    players = shelve.open('plugins/NGWordGame/players')
    playerlist = players['playerlist']
    players.close()
    return playerlist
