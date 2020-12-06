from bangtal import *
from enum import Enum
from yahtzee import *


setGameOption(GameOption.INVENTORY_BUTTON, 0)
setGameOption(GameOption.ROOM_TITLE, 0)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, 0)
scene1 = Scene('cau미니게임', 'images/배경.png')
scene2 = Scene('오델로', 'images(othello)/오델로배경.png')
scene3 = Scene('mainmap', 'images/yahtzee/scene.png')
scene4 = Scene("Omok", "images/background.png")

title = Object('images/제목.png')
title.locate(scene1, 200, 250)
title.show()

startbutton = Object('images/start.png')
startbutton.locate(scene1, 535, 100)
startbutton.setScale(0.5)
startbutton.show()

game1 = Object('images/오델로.png')
game1.locate(scene1, 140, 280)

game1_title = Object('images/오델로 제목.png')
game1_title.locate(scene1, 190, 250)

game2 = Object('images/야추.jpg')
game2.locate(scene1, 540, 280)

game2_title = Object('images/야추 제목.png')
game2_title.locate(scene1, 570, 250)

game3 = Object('images/오목.png')
game3.locate(scene1, 960, 280)

game3_title = Object('images/오목 제목.png')
game3_title.locate(scene1, 1030, 250)


def startbutton_onMouseAction(x, y, action):
    title.locate(scene1, 420, 550)
    title.setScale(0.5)
    startbutton.hide()
    game1.show()
    game1_title.show()
    game2.show()
    game2_title.show()
    game3.show()
    game3_title.show()


startbutton.onMouseAction = startbutton_onMouseAction


def game1_onMouseAction(x, y, action):  # 오델로
    scene2.enter()


game1.onMouseAction = game1_onMouseAction

yahtplayed =False
def game2_onMouseAction(x, y, action):  # 야추다이스
    global yahtplayed
    scene3.enter()
    if yahtplayed ==False:
        yahtzee(scene3, scene1)
        yahtplayed=True


game2.onMouseAction = game2_onMouseAction


def game3_onMouseAction(x, y, action):  # 오목
    scene4.enter()


game3.onMouseAction = game3_onMouseAction

# 오델로


class State(Enum):
    BLANK = 0
    POSSIBLE = 1
    BLACK = 2
    WHITE = 3


class Turn(Enum):
    BLACK = 1
    WHITE = 2


turn = Turn.BLACK


def setState(x, y, s):
    object = board[y][x]
    object.state = s
    if s == State.BLANK:
        object.setImage("images(othello)/blank.png")
    elif s == State.BLACK:
        object.setImage("images(othello)/black.png")
    elif s == State.WHITE:
        object.setImage("images(othello)/white.png")
    elif turn == Turn.BLACK:
        object.setImage("images(othello)/black possible.png")
    else:
        object.setImage("images(othello)/white possible.png")


def stone_onMouseAction(x, y):
    global turn

    object = board[y][x]
    if object.state == State.POSSIBLE:
        if turn == Turn.BLACK:
            setState(x, y, State.BLACK)
            reverse_xy(x, y)
            turn = Turn.WHITE
        else:
            setState(x, y, State.WHITE)
            reverse_xy(x, y)
            turn = Turn.BLACK

        if not setPossible():
            if turn == Turn.BLACK:
                turn = Turn.WHITE
            else:
                turn = Turn.BLACK

            if not setPossible():
                scorecheck(x, y)
                if countB > countW:
                    showMessage("BLACK WIN")
                elif countB < countW:
                    showMessage("WHITE WIN")
                else:
                    showMessage("draw")
                start = Object('images/yahtzee/end.png')
                start.locate(scene2, 300, 400)
                start.setScale(0.8)
                start.onMouseAction = lambda x, y, action: scene1.enter()
                start.show()


def setPossible_xy_dir(x, y, dx, dy):
    if turn == Turn.BLACK:
        mine = State.BLACK
        other = State.WHITE
    else:
        mine = State.WHITE
        other = State.BLACK

    possible = False
    while True:
        x = x + dx
        y = y + dy

        if x < 0 or x > 7:
            return False
        if y < 0 or y > 7:
            return False

        object = board[y][x]
        if object.state == other:
            possible = True
        elif object.state == mine:
            return possible
        else:
            return False


def setPossible_xy(x, y):
    object = board[y][x]
    if object.state == State.BLACK:
        return False
    if object.state == State.WHITE:
        return False
    setState(x, y, State.BLANK)

    if setPossible_xy_dir(x, y, 0, 1):
        return True
    if setPossible_xy_dir(x, y, 1, 1):
        return True
    if setPossible_xy_dir(x, y, 1, 0):
        return True
    if setPossible_xy_dir(x, y, 1, -1):
        return True
    if setPossible_xy_dir(x, y, 0, -1):
        return True
    if setPossible_xy_dir(x, y, -1, -1):
        return True
    if setPossible_xy_dir(x, y, -1, 0):
        return True
    if setPossible_xy_dir(x, y, -1, 1):
        return True
    return False


def reverse_xy_dir(x, y, dx, dy):
    if turn == Turn.BLACK:
        mine = State.BLACK
        other = State.WHITE
    else:
        mine = State.WHITE
        other = State.BLACK

    possible = False
    while True:
        x = x + dx
        y = y + dy

        if x < 0 or x > 7:
            return
        if y < 0 or y > 7:
            return

        object = board[y][x]
        if object.state == other:
            possible = True
        elif object.state == mine:
            if possible:
                while True:
                    x = x - dx
                    y = y - dy

                    object = board[y][x]
                    if object.state == other:
                        setState(x, y, mine)
                    else:
                        return

        else:
            return


def reverse_xy(x, y):
    reverse_xy_dir(x, y, 0, 1)
    reverse_xy_dir(x, y, 1, 1)
    reverse_xy_dir(x, y, 1, 0)
    reverse_xy_dir(x, y, 1, -1)
    reverse_xy_dir(x, y, 0, -1)
    reverse_xy_dir(x, y, -1, -1)
    reverse_xy_dir(x, y, -1, 0)
    reverse_xy_dir(x, y, -1, 1)


def setPossible():
    possible = False
    for y in range(8):
        for x in range(8):
            if setPossible_xy(x, y):
                setState(x, y, State.POSSIBLE)
                possible = True
    return possible


board = []
for y in range(8):
    board.append([])
    for x in range(8):
        object = Object("images(othello)/blank.png")
        object.locate(scene2, 40 + x * 80, 40 + y * 80)
        object.show()
        object.onMouseAction = lambda mx, my, action, ix = x, iy = y: stone_onMouseAction(
            ix, iy)
        object.state = State.BLANK
        board[y].append(object)

setState(3, 3, State.BLACK)
setState(4, 4, State.BLACK)
setState(3, 4, State.WHITE)
setState(4, 3, State.WHITE)

setPossible()


score1 = Object("images(othello)/L0.png")
score2 = Object("images(othello)/L0.png")
score3 = Object("images(othello)/L0.png")
score4 = Object("images(othello)/L0.png")

countB, countW = 0, 0
countB = int(countB)
countW = int(countW)


def setScore1(s):
    if s == 0:
        score1.setImage("images(othello)/L0.png")
    elif s == 1:
        score1.setImage("images(othello)/L1.png")
    elif s == 2:
        score1.setImage("images(othello)/L2.png")
    elif s == 3:
        score1.setImage("images(othello)/L3.png")
    elif s == 4:
        score1.setImage("images(othello)/L4.png")
    elif s == 5:
        score1.setImage("images(othello)/L5.png")
    elif s == 6:
        score1.setImage("images(othello)/L6.png")
    elif s == 7:
        score1.setImage("images(othello)/L7.png")
    elif s == 8:
        score1.setImage("images(othello)/L8.png")
    elif s == 9:
        score1.setImage("images(othello)/L9.png")


def setScore2(s):
    if s == 0:
        score2.setImage("images(othello)/L0.png")
    elif s == 1:
        score2.setImage("images(othello)/L1.png")
    elif s == 2:
        score2.setImage("images(othello)/L2.png")
    elif s == 3:
        score2.setImage("images(othello)/L3.png")
    elif s == 4:
        score2.setImage("images(othello)/L4.png")
    elif s == 5:
        score2.setImage("images(othello)/L5.png")
    elif s == 6:
        score2.setImage("images(othello)/L6.png")
    elif s == 7:
        score2.setImage("images(othello)/L7.png")
    elif s == 8:
        score2.setImage("images(othello)/L8.png")
    elif s == 9:
        score2.setImage("images(othello)/L9.png")


def setScore3(s):
    if s == 0:
        score3.setImage("images(othello)/L0.png")
    elif s == 1:
        score3.setImage("images(othello)/L1.png")
    elif s == 2:
        score3.setImage("images(othello)/L2.png")
    elif s == 3:
        score3.setImage("images(othello)/L3.png")
    elif s == 4:
        score3.setImage("images(othello)/L4.png")
    elif s == 5:
        score3.setImage("images(othello)/L5.png")
    elif s == 6:
        score3.setImage("images(othello)/L6.png")
    elif s == 7:
        score3.setImage("images(othello)/L7.png")
    elif s == 8:
        score3.setImage("images(othello)/L8.png")
    elif s == 9:
        score3.setImage("images(othello)/L9.png")


def setScore4(s):
    if s == 0:
        score4.setImage("images(othello)/L0.png")
    elif s == 1:
        score4.setImage("images(othello)/L1.png")
    elif s == 2:
        score4.setImage("images(othello)/L2.png")
    elif s == 3:
        score4.setImage("images(othello)/L3.png")
    elif s == 4:
        score4.setImage("images(othello)/L4.png")
    elif s == 5:
        score4.setImage("images(othello)/L5.png")
    elif s == 6:
        score4.setImage("images(othello)/L6.png")
    elif s == 7:
        score4.setImage("images(othello)/L7.png")
    elif s == 8:
        score4.setImage("images(othello)/L8.png")
    elif s == 9:
        score4.setImage("images(othello)/L9.png")


def scorecheck(x, y):
    global countB
    global countW
    for y in range(8):
        for x in range(8):
            object = board[y][x]
            if object.state == State.BLACK:
                countB += 1
            elif object.state == State.WHITE:
                countW += 1

    if countB < 10:
        for i in range(10):
            if countB == i:
                setScore1(countB)
                score1.locate(scene2, 720, 220)
                score1.show()

    elif countB >= 10:
        for i in range(10):
            if countB//10 == i:
                setScore1(countB//10)
                score1.locate(scene2, 720, 220)
                score1.show()

        for i in range(10):
            if countB % 10 == i:
                setScore2(countB % 10)
                score2.locate(scene2, 800, 220)
                score2.show()

    if countW < 10:
        for i in range(10):
            if countW == i:
                setScore3(countW)
                score3.locate(scene2, 1070, 220)
                score3.show()

    elif countW >= 10:
        for i in range(10):
            if countW//10 == i:
                setScore3(countW//10)
                score3.locate(scene2, 1070, 220)
                score3.show()

        for i in range(10):
            if countW % 10 == i:
                setScore4(countW % 10)
                score4.locate(scene2, 1150, 220)
                score4.show()


# 오목
turnOmok = Turn.BLACK


def setStateOmok(x, y, s):
    object = boardOmok[y][x]
    object.state = s
    if s == State.BLANK:
        object.setImage("images/blank.png")
    elif s == State.BLACK:
        object.setImage("images/black.png")
    elif s == State.WHITE:
        object.setImage("images/white.png")


omokstat = 0


def stoneOmok_onMouseAction(x, y):
    global turnOmok
    global omokstat
    object = boardOmok[y][x]
    if object.state == State.BLANK:
        if omokstat == 0:
            if turnOmok == Turn.BLACK:
                setStateOmok(x, y, State.BLACK)
            else:
                setStateOmok(x, y, State.WHITE)
            cal_xy(x, y)
        if wscore >= 5 and omokstat == 0 or omokstat == -1:
            showMessage("흰돌 승")
            start = Object('images/yahtzee/end.png')
            start.locate(scene4, 500, 300)
            start.setScale(0.8)
            start.onMouseAction = lambda x, y, action: scene1.enter()
            start.show()
            omokstat = -1
        elif bscore >= 5 and omokstat == 0 or omokstat == 1:
            showMessage("검돌 승")
            start = Object('images/yahtzee/end.png')
            start.locate(scene4, 500, 400)
            start.setScale(0.8)
            start.onMouseAction = lambda x, y, action: scene1.enter()
            start.show()
            omokstat = 1
        if turnOmok == Turn.BLACK:
            turnOmok = Turn.WHITE
        else:
            turnOmok = Turn.BLACK
    print(wscore)
    print(bscore)


def cal_xy(x, y):
    cal_xy_dir(x, y, 1)
    cal_xy_dir(x, y, 2)
    cal_xy_dir(x, y, 3)
    cal_xy_dir(x, y, 4)
    return False


bscore = 0
wscore = 0


def cal_xy_dir(x, y, direct):
    global bscore
    global wscore
    score = 1
    ax=x
    ay=y
    dx=0
    dy=0
    if turnOmok == Turn.BLACK:
        mine = State.BLACK
        other = State.WHITE
    else:
        mine = State.WHITE
        other = State.BLACK
    if direct==1:
        dx=0
        dy=1
    elif direct==2:
        dx=1
        dy=0
    elif direct==3:
        dx=1
        dy=1
    else:
        dx=-1
        dy=1
    while True:
        ax = ax+dx
        ay = ay+dy

        if ax < 0 or ax > 8:
            break
        if ay < 0 or ay > 8:
            break

        object = boardOmok[ay][ax]
        if object.state == mine:
            score += 1
        else:
            if turnOmok == Turn.BLACK:
                if bscore <= score:
                    bscore = score
            else:
                if wscore <= score:
                    wscore = score
            break
    ax=x
    ay=y
    dx=-dx
    dy=-dy
    while True:
        ax = ax+dx
        ay = ay+dy

        if ax < 0 or ax > 8:
            break
        if ay < 0 or ay > 8:
            break

        object = boardOmok[ay][ax]
        if object.state == mine:
            score += 1
        else:
            if turnOmok == Turn.BLACK:
                if bscore <= score:
                    bscore = score
            else:
                if wscore <= score:
                    wscore = score
            return


boardOmok = []
for y in range(9):
    boardOmok.append([])
    for x in range(9):
        object = Object("images/blank.png")
        object.setScale(1.1)
        object.locate(scene4, 275+80*x, 5+80*y)
        object.show()
        object.onMouseAction = lambda mx, my, action, ix=x, iy=y: stoneOmok_onMouseAction(
            ix, iy)
        object.state = State.BLANK

        boardOmok[y].append(object)


startGame(scene1)
