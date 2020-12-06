import glob
import os
import random
from ctypes import *
from random import choice
from time import sleep

from bangtal import *
from pyhtzee import Pyhtzee
from pyhtzee.classes import Category, Rule
from pyhtzee.utils import category_to_action_map, dice_roll_to_action_map

setGameOption(GameOption.INVENTORY_BUTTON, 0)
setGameOption(GameOption.ROOM_TITLE, 0)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, 0)
basepath = 'images/yahtzee/'


class yahtzee():
    dicelist = []
    checklist = []
    curplayer = 0
    turn = 1
    yahtzee_list = []
    rerollcount = 0
    totalturn = 0   
    turnstart = True
    lowerscore = [0, 0]
    upperscore = [0, 0]

    def __init__(self,scene,scene2):
        self.mainmap = scene
        self.endscene = scene2
        self.start = Object(basepath+'start.png')
        self.start.locate(self.mainmap, 670, 300)
        self.start.setScale(0.8)
        self.start.onMouseAction = lambda x, y, action: self.startYahtzee()
        self.start.show()

    def startYahtzee(self):
        self.start.hide()
        self.roll = Object(basepath+'roll.png')
        self.roll.locate(self.mainmap, 1000, 100)
        self.roll.onMouseAction = lambda x, y, action: self.reRoll()
        self.roll.setScale(0.2)
        self.roll.show()
        self.uppersection = [[Object(basepath+'0.png'), Object(basepath+'0.png'), Object(basepath+'0.png')], [
            Object(basepath+'0.png'), Object(basepath+'0.png'), Object(basepath+'0.png')]]
        self.uppertotalsection = [[Object(basepath+'0.png'), Object(basepath+'0.png'), Object(basepath+'0.png')], [
            Object(basepath+'0.png'), Object(basepath+'0.png'), Object(basepath+'0.png')]]
        self.lowersection = [[Object(basepath+'0.png'), Object(basepath+'0.png'), Object(basepath+'0.png')], [
            Object(basepath+'0.png'), Object(basepath+'0.png'), Object(basepath+'0.png')]]
        self.upperlowersection = [[Object(basepath+'0.png'), Object(basepath+'0.png'), Object(basepath+'0.png')], [
            Object(basepath+'0.png'), Object(basepath+'0.png'), Object(basepath+'0.png')]]
        self.totalsection = [[Object(basepath+'0.png'), Object(basepath+'0.png'), Object(basepath+'0.png')], [
            Object(basepath+'0.png'), Object(basepath+'0.png'), Object(basepath+'0.png')]]
        for k in range(6):
            self.checklist.append(Object(basepath+'check.png'))
            self.checklist[k].locate(self.mainmap, 210, 625-k*30)
            self.checklist[k].setScale(0.03)
            self.checklist[k].onMouseAction = lambda x, y, action, checknum = k: self.checkStatus(
                checknum)
            self.checklist[k].checked = False
            self.checklist[k].show()
        for k in range(7):
            self.checklist.append(Object(basepath+'check.png'))
            self.checklist[k+6].locate(self.mainmap, 210, 315-k*30)
            self.checklist[k+6].setScale(0.03)
            self.checklist[k+6].onMouseAction = lambda x, y, action, checknum = k + \
                6: self.checkStatus(checknum)
            self.checklist[k+6].checked = False
            self.checklist[k+6].show()

        for k in range(1, 6):
            self.dicelist.append(Object(basepath+'dice'+str(k)+'.png'))
            self.dicelist[k-1].checked = False
            self.dicelist[k-1].imageName = 'dice'+str(k)
            self.dicelist[k -
                          1].onMouseAction = lambda x, y, action, dice = k: self.diceStatus(dice)
            self.dicelist[k-1].locate(self.mainmap, 600+k*70, 400)
            self.dicelist[k-1].setScale(0.4)

        self.done = Object(basepath+'done.png')
        self.done.locate(self.mainmap, 1100, 100)
        self.done.setScale(0.6)
        self.done.onMouseAction = lambda x, y, action: self.doneRound()

        self.done.show()

        self.player = Object(basepath+'player'+str(self.curplayer)+'.png')
        self.player.locate(self.mainmap, 1000, 500)
        self.player.setScale(0.4)
        self.player.show()
        self.yahtzee_list.append(Pyhtzee(rule=Rule.YAHTZEE))
        self.yahtzee_list.append(Pyhtzee(rule=Rule.YAHTZEE))
        showMessage('player'+str(int(self.curplayer == True)+1)+"'s turn")

    def play(self):
        curdice = self.yahtzee_list[self.curplayer].dice
        self.show_dice(curdice)

    def checkStatus(self, checknum):
        if self.checklist[checknum].checked == False:
            self.checklist[checknum].checked = True
            self.checklist[checknum].setImage(basepath+'check.png')
            self.checklist[checknum].setScale(0.03)

        for num in range(13):
            if checknum != num:
                self.checklist[num].checked = False
                self.checklist[num].setImage(basepath+'square1.png')
                self.checklist[num].setScale(0.7)
        for k in range(6):
            self.checklist[k].locate(self.mainmap, 210, 625-k*30)
        for k in range(7):
            self.checklist[k+6].locate(self.mainmap, 210, 315-k*30)

    def diceStatus(self, dicenum):
        self.dicelist[dicenum-1].checked = not self.dicelist[dicenum-1].checked
        if self.dicelist[dicenum-1].checked == 0:
            self.dicelist[dicenum -
                          1].setImage(self.dicelist[dicenum-1].imageName+'.png')
        else:
            self.dicelist[dicenum -
                          1].setImage(self.dicelist[dicenum-1].imageName+'_.png')

    def reRoll(self):
        if self.turnstart:
            self.play()
            self.turnstart = False
        else:
            if set([dice.checked for dice in self.dicelist]) != {False}:
                if self.rerollcount < 2:
                    self.rerollcount += 1
                    action = dice_roll_to_action_map[tuple(
                        [dice.checked for dice in self.dicelist])]
                    self.yahtzee_list[self.curplayer].take_action(action)
                    self.play()
                else:
                    showMessage('you can"t reroll more')
            else:
                showMessage('you should check dice to reroll')

    def show_dice(self, dicenum):
        for k, num in zip(range(1, 6), dicenum):
            self.dicelist[k-1].setImage(basepath+'dice'+str(num)+'.png')
            self.dicelist[k-1].imageName = 'dice'+str(num)
            self.dicelist[k-1].checked = False
            self.dicelist[k-1].show()

    def doneRound(self):
        # select from board
        if self.turnstart:
            showMessage('please roll dice first')
        else:
            selected_idx = None
            for idx, check in enumerate(self.checklist):
                if check.checked:
                    selected_idx = idx
                    break
            cat = [Category.ACES, Category.TWOS, Category.THREES, Category.FOURS, Category.FIVES, Category.SIXES, Category.THREE_OF_A_KIND,
                   Category.FOUR_OF_A_KIND, Category.FULL_HOUSE, Category.SMALL_STRAIGHT, Category.LARGE_STRAIGHT, Category.YAHTZEE, Category.CHANCE]
            if selected_idx != None:
                selected_cat = cat[selected_idx]
                if selected_cat in self.yahtzee_list[self.curplayer].scores.keys():
                    showMessage('please select different category')
                else:
                    action = category_to_action_map[selected_cat]
                    reward = self.yahtzee_list[self.curplayer].take_action(
                        action)
                    showMessage(str(self.yahtzee_list[self.curplayer].scores))
                    print(self.yahtzee_list[self.curplayer].scores)
                    self.setScore(reward, selected_idx)
                    self.changePlayer()
                    self.totalturn += 1
                    if int(self.totalturn/25) == 1:
                        self.scoreView(sum(self.yahtzee_list[self.curplayer].scores.values()), 250+self.curplayer*70, 315-10*30,
                                       self.totalsection[self.curplayer])
                    if self.totalturn == 26:
                        showMessage('game is over winner is player' +
                                    str(int(self.player == True)))
                        self.start = Object(basepath+'end.png')
                        self.start.locate(self.mainmap, 670, 300)
                        self.start.setScale(0.8)
                        self.start.onMouseAction = lambda x, y, action: self.endscene.enter()
                        self.start.show()
                    else:
                        showMessage('you gain '+str(reward)+'\nplayer' +
                                str(int(self.curplayer == True)+1)+"'s turn")
            else:
                showMessage('please select category first')

    def changePlayer(self):
        self.curplayer = not self.curplayer
        for k in range(1, 6):
            self.dicelist[k-1].hide()
        self.player.setImage(basepath+'player'+str(int(self.curplayer == True))+'.png')
        self.rerollcount = 0
        self.turnstart = True
        for num in range(13):
            self.checklist[num].checked = False
            self.checklist[num].setImage(basepath+'check.png')
            self.checklist[num].setScale(0.03)
        for k in range(6):
            self.checklist[k].locate(self.mainmap, 210, 625-k*30)
        for k in range(7):
            self.checklist[k+6].locate(self.mainmap, 210, 315-k*30)

    def setScore(self, score, position):
        xpos = 250+self.curplayer*70
        if position in range(6):
            ypos = 625-position*30
            self.upperscore[self.curplayer] += score
            self.scoreView(self.upperscore[self.curplayer], xpos, 625-6*30,
                           self.uppersection[self.curplayer])
            self.scoreView(self.upperscore[self.curplayer], xpos, 315-9*29,
                           self.upperlowersection[self.curplayer])

        elif position in range(6, 14):
            ypos = 315-(position-6)*30
            self.lowerscore[self.curplayer] += score
            self.scoreView(self.lowerscore[self.curplayer], xpos, 315-8*30,
                           self.lowersection[self.curplayer])

        if Category.UPPER_SECTION_BONUS in self.yahtzee_list[self.curplayer].scores.keys():
            bonus = self.yahtzee_list[self.curplayer].scores[Category.UPPER_SECTION_BONUS]
            self.scoreView(bonus, xpos, 625-7*29)
            self.scoreView(self.upperscore[self.curplayer]+bonus, xpos,
                           625-6*29, self.uppertotalsection[self.curplayer])
            self.scoreView(self.upperscore[self.curplayer], xpos, 625-8*28,
                           self.uppertotalsection[self.curplayer])
            self.scoreView(self.upperscore[self.curplayer], xpos, 315-9*29,
                           self.upperlowersection[self.curplayer])

        if Category.YAHTZEE_BONUS in self.yahtzee_list[self.curplayer].scores.keys():
            bonus = self.yahtzee_list[self.curplayer].scores[Category.YAHTZEE_BONUS]
            self.scoreView(bonus, xpos, 315-7*30)
            self.scoreView(self.lowerscore[self.curplayer]+bonus, xpos,
                           315-8*30, self.lowersection[self.curplayer])

        self.scoreView(score, xpos, ypos)

    def scoreView(self, score, xpos, ypos, section=None):
        print(score)
        if section:
            hund = section[0]
            hund.setImage(basepath+str(int(score/100))+'.png')
            ten = section[1]
            ten.setImage(basepath+str(int((score % 100)/10))+'.png')
            one = section[2]
            one.setImage(basepath+str(score % 10)+'.png')
        else:
            hund = Object(basepath+str(int(score/100))+'.png')
            ten = Object(basepath+str(int((score % 100)/10))+'.png')
            one = Object(basepath+str(score % 10)+'.png')
        if int(score/100):
            hund.locate(self.mainmap, xpos, ypos)
            ten.locate(self.mainmap, xpos+10, ypos)
            one.locate(self.mainmap, xpos+20, ypos)
            hund.setScale(0.8)
            ten.setScale(0.8)
            one.setScale(0.8)
            hund.show()
            ten.show()
            one.show()
        elif int(score/10):
            ten.locate(self.mainmap, xpos, ypos)
            one.locate(self.mainmap, xpos+10, ypos)
            ten.setScale(0.8)
            one.setScale(0.8)
            ten.show()
            one.show()
        else:
            one.locate(self.mainmap, xpos, ypos)
            one.setScale(0.8)
            one.show()