# NGWordGame
基于[nonebot](https://github.com/richardchien/nonebot)的QQ机器人插件，在QQ群中实现NG词语游戏。

## NG词语游戏
出自漫画《辉夜大小姐想让我告白～天才们的恋爱头脑战～》，规则为参与游戏的每个玩家为下一个玩家设置一个“NG词”，
设置完成后展示之，使得除了自己的每个人都能知道自己的NG词。之后所有玩家进行自由谈话，说出自己的NG词的玩家判负，退场。直至只剩一人为止。

## 使用
将本项目作为nonebot的插件使用。关于nonebot的使用和插件添加方法，参见其[项目文档](https://none.rclab.tk/)。  
- 注册阶段：由超级用户发出指令`NG词语游戏`（或`NGWordGame`，`ng`）开始游戏，所有参与者回复`sign in`参与游戏，超级用户发出指令`stop signing`停止注册
- 设置阶段：所有玩家使用`setNG`指令和机器人私聊设置下一个玩家的NG词。当所有玩家设置完成时，机器人会自动向群里发送通知，由超级用户发出`check`指令加载所有设置的NG词
- 监听阶段：此时开始机器人对群内聊天信息进行监听，当有玩家触发自己的NG词时发出提醒，直至只剩一位玩家，游戏结束。

注意，由于此功能要求NG词语游戏会话对群内所有人的发言都有响应，需要修改nonebot的`nonebot\command\__init__.py`中525行：
```
ctx_id = context_id(ctx)
```
将其改为：
```
ctx_id = context_id(ctx, mode='group')
```

## 实现
（略）
