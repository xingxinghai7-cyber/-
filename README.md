# Flappy Bird

一个基于 Pygame 开发的 Flappy Bird 游戏。

## 功能特性

- **两种游戏模式**：
  - **普通模式**：经典玩法，控制小鸟飞行穿过管道得分
  - **拓展模式**：包含普通模式所有内容，并增加多种buff道具

- **游戏特色**：
  - 收集金币获得额外分数
  - 多种buff道具（减速、冲刺、清屏）
  - 支持暂停功能
  - 高分记录系统
  - 新纪录提示

## 操作说明

- **空格键**：跳跃
- **P键**：暂停/继续游戏
- **鼠标点击**：选择按钮、开始游戏

## 游戏规则

### 普通模式
1. 按空格键控制小鸟飞行
2. 穿过管道获得分数
3. 收集金币获得额外分数
4. 避开管道，不要撞到上下管道或落地

### 拓展模式
除普通模式规则外，还包含：
- **减速buff**：管道速度减慢，持续5秒
- **冲刺buff**：管道速度加快，撞碎管道不会判负，结束时自动清屏
- **清屏buff**：消除前方最多3个管道，每个+2分
- **双倍积分buff**：获得的分数翻倍，包括过管道、吃金币、撞管道得分，持续5秒

## 项目结构

```
Flappy Bird/
├── main.py          # 游戏主入口
├── game.py          # 游戏核心逻辑
├── bird.py          # 小鸟类
├── pipe.py          # 管道类
├── ui.py            # 界面UI类
├── coin.py          # 金币生成器
├── settings.py      # 游戏配置
└── assets/          # 资源文件目录
    ├── bird.png
    ├── pipe_top.png
    ├── pipe_bottom.png
    ├── coin.png
    └── ...
```

## 运行方式

### 开发环境

```bash
pip install pygame
python main.py
```

### 打包成EXE

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "FlappyBird" --add-data "assets;assets" main.py
```

生成的EXE文件位于 `dist/FlappyBird.exe`

## 技术栈

- Python 3.13+
- Pygame 2.6+

## 开发说明

游戏状态包括：menu（菜单）、countdown（倒计时）、playing（游戏中）、paused（暂停）、game_over（游戏结束）、help（帮助）

## 截图

游戏包含以下界面：
- 主菜单：选择游戏模式
- 倒计时：3秒准备时间
- 游戏界面：显示分数、金币、buff状态
- 暂停界面：可继续或返回菜单
- 游戏结束界面：显示得分和最高分
- 帮助界面：游戏说明

## 许可证

MIT License
