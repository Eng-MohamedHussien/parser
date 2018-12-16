#!/usr/bin/env python
# coding: utf-8

# In[39]:
import os.path

#to know the place of the character you will deal with it next
index = 0

#reading from file (input.txt)
if os.path.isfile('input.txt'):
    fileHandler = open('input.txt','r')
    input = fileHandler.read()

''''
#writing to file (output.txt)
outFile = open('output.txt','w')
'''

#function declaration that we will use it in parser
def getToken ():
    global index
    global input
    if index == 0:
        fileHandler = open('input.txt','r')
        input = fileHandler.read()
    #declaring our states , special symbols and reserved words in the DFA
    states = ['start', 'inComment', 'inDigit', 'inLetter', 'inAssign', 'done']
    specialSymbols = {'+' : 'plus', '-' : 'minus', '*' : 'multiply', '/' : 'division', '=' : 'equal', '<' : 'less than', '(' : 'openning bracket', ')' : 'closing bracket', ';' : 'semi colon'}
    reservedWords = ['if','then','else','end','repeat','until','read','write']

    while index < len(input):
        #defining my current state and the next one
        currentState = 'start'
        nextState = ''
        change = False

        #variable that will carry the value of the token
        token = ''
        tokenType = ''

        #the DFA process converts to code
        while currentState != 'done':
            if index >= len(input):
                break
            character = input[index]
            change = False
            #case of assign :=
            if currentState == 'start' and character == ':':
                nextState = 'inAssign'
                change = True
            elif currentState == 'inAssign' and character == '=':
                token = ':='
                tokenType = 'assign'
                nextState = 'done'
                change = True
            #case of having letter
            elif currentState == 'start' and character.isalpha():
                nextState = 'inLetter'
                change = True
            elif currentState == 'inLetter' and not(character.isalpha()):
                nextState = 'done'
                change = True
                tokenType = 'letter'
            #case of having numbers
            elif currentState == 'start' and character.isdigit():
                nextState = 'inDigit'
                change = True
            elif currentState == 'inDigit' and not(character.isdigit()):
                nextState = 'done'
                change = True
                tokenType = 'Number'
            #case of special symbols
            elif currentState == 'start' and (character == '+' or character == '-' or character == '/' or character == '*' or character == ';' or character == '(' or character == ')' or character == '=' or character == '<'):
                nextState = 'done'
                change = True
                token = character
                tokenType = 'specialSymbol'
            #handling comments by ignoring them
            elif currentState == 'start' and  character == '{':
                nextState = 'inComment'
                change = True
            elif currentState == 'inComment' and character == '}':
                nextState = 'start'
                change = True
            #handle the delimiter character
            if (nextState == 'done') and (currentState == 'inLetter' or currentState == 'inDigit'):
                index = index -1
            #getting the next character
            index = index + 1
            #if we have transition from one state to another
            if change:
                currentState = nextState
                nextState = ''
            #accumelating the token in case of set of letters and numbers
            if nextState == 'inLetter' or currentState == 'inLetter' or nextState == 'inDigit' or currentState == 'inDigit':
                token = token + character

        #another checks for special symbols , reserved words and identifiers
        if tokenType == 'letter':
            if token in reservedWords:
                tokenType = 'reserved word'
            else:
                tokenType = 'identifier'
        elif tokenType == 'specialSymbol':
            tokenType = specialSymbols[token]
        #handling case of empty token
        if token != '':
            #outFile.write(token + ' , ' + tokenType + '\n')
            #print(token + ' , ' + tokenType + '\n')
            #break
            return(token + ',' + tokenType)
        
    if index >= len(input):
        return('finish')

