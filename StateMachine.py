from enum import Enum
from .PlayerList import Player, PlayerList, StorePlayer, LoadPlayer
from typing import List

states = Enum('gamestate', ['signing', 'settingNG', 'listening'])


class NGFSM:
    class replymsg:
        def __init__(self, msg: str = '', at_sender: bool = False, pause: bool = True):
            self.msg = msg
            self.at_sender = at_sender
            self.pause = pause

    class privatemsg:
        def __init__(self, user_id, msg):
            self.user_id = user_id
            self.msg = msg

    def __init__(self, groupid):
        self.state = states.signing
        self.playerlist = PlayerList(groupid)
        self.reply: List[NGFSM.replymsg] = \
            [self.replymsg(msg='NG词语游戏\n请有意参加的成员回复\'sign in\'')]
        self.private: List[NGFSM.privatemsg] = []

    def ClearReply(self):
        for i in range(len(self.reply)):
            del self.reply[0]
        for i in range(len(self.private)):
            del self.private[0]

    def RecieveInput(self, sender, text):
        self.ClearReply()

        if text == 'stop' and sender['isSU']:
            self.reply = [self.replymsg(msg=self.playerlist.PrintNG()),
                          self.replymsg(msg='游戏强制终止', pause=False)]
            return

        if self.state == states.signing:
            if text == 'sign in':
                self.playerlist.append(Player(sender))
                self.reply = [self.replymsg(msg='成功注册', at_sender=True)]
            elif text == 'stop signing' and sender['isSU']:
                self.reply = [self.replymsg('玩家注册阶段结束，已注册的玩家有：\n' + self.playerlist.PrintPlayers()),
                              self.replymsg('开始私聊设置NG词')]
                self.private = [self.privatemsg(user_id=pid, msg=msg) for pid, msg in self.playerlist.SetPrompt()]
                self.playerlist.canset = True
                StorePlayer(self.playerlist)
                self.state = states.settingNG
            else:
                pass

        elif self.state == states.settingNG:
            if text == 'check' and sender['isSU']:
                self.playerlist = LoadPlayer()
                self.playerlist.canset = False
                StorePlayer(self.playerlist)

                self.reply = [self.replymsg('所有NG词已设置完成，请各位自由谈话')]
                self.private = \
                    [self.privatemsg(user_id=p.id,
                                     msg='除你以外所有人的NG词是：\n' +
                                         self.playerlist.PrintNG(mask=i))
                     for i, p in enumerate(self.playerlist.Players)]

                self.state = states.listening
            else:
                pass

        elif self.state == states.listening:
            p = self.playerlist.CheckText(sender['user_id'], text)
            if p:
                self.reply = [self.replymsg('触发了NG词“{}”，退出游戏'.format(p.NGword), at_sender=True)]
                self.playerlist.ExitGame(p.id)
                if self.playerlist.nplayer <= 1:
                    winner = self.playerlist.Winner()
                    self.reply.append(
                        self.replymsg('游戏结束，{}胜利，ta的NG词是“{}”'.format(winner.name, winner.NGword), pause=False))
                else:
                    self.reply = [self.replymsg('游戏继续，还有{:d}位玩家'.format(self.playerlist.nplayer))]
            else:
                pass
