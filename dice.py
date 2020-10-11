# -*- coding: utf-8 -*-
from parse import parse
import numpy as np
import json

class Dice():
    def __init__(self):
        self.json_read = open('config.json','r')
        self.botmessage = json.load(self.json_read)['messages']
        self.botText = '\n'.join(self.botmessage['command_error'])
        self.diceCount = 0
        self.diceSize = 0
        self.numberCompared = 0

    def roleDice(self, diceSize):
        result = np.random.randint(1,int(diceSize))
        return result

    def roleSomeDice(self, diceCount, diceSize, correction):
        diceValue = np.array([], dtype=np.int64)
        for i in range(diceCount):
            diceValue = np.append(diceValue, self.roleDice(diceSize))
        diceSum = np.sum(diceValue)
        if correction == 0: message = self.botmessage['dice_roll'] + str(diceSum) + " = " + str(diceValue)
        else:
            message = self.botmessage['result'] + str(diceSum+correction) + self.botmessage['dice_roll'] + str(diceSum)+ " = " + str(diceValue)+ self.botmessage['correction'] +str(correction)
            diceSum =  diceSum + correction 
        return message, diceSum

    def roleD66Dice(self, sort):
        diceValue = np.array([], dtype=np.int64)
        diceValue = np.append(diceValue, self.roleDice(6))
        diceValue = np.append(diceValue, self.roleDice(6))
        np.sort(diceValue)
        if sort == 'up':
            d66 = diceValue[0] * 10 + diceValue[1]
            massage = '出目: ' + str(d66)
        elif sort == 'down':
            d66 = diceValue[1] * 10 + diceValue[0]
            massage = '出目: ' + str(d66)
        return massage

    def compareDice(self,info,correction):
        if '<=' in info[2] or '=<' in info[2]:
            if info[0].isdecimal() and info[3].isdecimal():
                resultmessage,diceSum = self.roleSomeDice(int(info[0]),int(info[1]),correction)
                if diceSum <= int(info[3]):
                    self.botText = self.botmessage['success'] + resultmessage
                else:
                    self.botText = self.botmessage['failure'] + resultmessage

        elif '<' in info[2]:
            if info[0].isdecimal() and info[3].isdecimal():
                resultmessage,diceSum = self.roleSomeDice(int(info[0]),int(info[1]),correction)
                if diceSum < int(info[3]):
                    self.botText = self.botmessage['success'] + resultmessage
                else:
                    self.botText = self.botmessage['failure'] + resultmessage

        elif '>=' in info[2] or '=>' in info[2]:
            if info[0].isdecimal() and info[3].isdecimal():
                resultmessage,diceSum = self.roleSomeDice(int(info[0]),int(info[1]),correction)
                if diceSum >= int(info[3]):
                    self.botText = self.botmessage['success'] + resultmessage
                else:
                    self.botText = self.sbotmessage['failure'] + resultmessage
                    
        elif '>' in info[2]:
            if info[0].isdecimal() and info[3].isdecimal():
                resultmessage,diceSum = self.roleSomeDice(int(info[0]),int(info[1]),correction)
                if diceSum > int(info[3]):
                    self.botText = self.botmessage['success'] + resultmessage
                else:
                    self.botText = self.botmessage['failure'] + resultmessage
        
        return self.botText

    def isCorrection(self,diceSize):
        correction = parse('{}+{}', diceSize)
        if correction:
            if correction[0].isdecimal() and correction[1].isdecimal():
                return True
        
        correction = parse('{}-{}', diceSize)
        if correction:
            if correction[0].isdecimal() and correction[1].isdecimal():
                return True
        return False

    def selectRollType(self,message):
        info = parse('dice d66 {}', message)
        if info:
            if info[0].lower() == 'up' or info[0].lower() == 'down':
                self.botText = self.roleD66Dice(info[0].lower())
            
        info = parse('dice {}d{}', message)
        if info:
            if info[0].isdecimal() and info[1].isdecimal():
                resultmessage, _ = self.roleSomeDice(int(info[0]),int(info[1]),0)
                self.botText = resultmessage

            correction = parse('{}+{}', info[1])
            if correction:
                if correction[0].isdecimal() and correction[1].isdecimal():
                    info = [info[0],correction[0]]
                    print
                    resultmessage, _ = self.roleSomeDice(int(info[0]),int(info[1]),int(correction[1]))
                    self.botText = resultmessage
            
            correction = parse('{}-{}', info[1])
            if correction:
                if correction[0].isdecimal() and correction[1].isdecimal():
                    info = [info[0],correction[0]]
                    resultmessage, _ = self.roleSomeDice(int(info[0]),int(info[1]),int(correction[1])*-1)
                    self.botText = resultmessage

        info = parse('dice {}d{} {} {}', message)
        if info:
            if info[1].isdecimal():
                self.compareDice(info,0)

            correction = parse('{}+{}', info[1])
            if correction:
                if correction[0].isdecimal() and correction[1].isdecimal():
                    info = [info[0],correction[0],info[2],info[3]]
                    self.botText = self.compareDice(info,int(correction[1]))

            correction = parse('{}-{}', info[1])
            if correction:
                if correction[0].isdecimal() and correction[1].isdecimal():
                    info = [info[0],correction[0],info[2],info[3]]
                    self.botText = self.compareDice(info,int(correction[1])*-1)

        return self.botText