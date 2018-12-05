#!/usr/bin/env python
# coding: utf-8

# In[23]:


from SCANNER import getToken
from graphviz import Digraph
import os
os.environ["PATH"] += os.pathsep + 'C:\Program Files (x86)\Graphviz2.38/bin/'
g = Digraph('G', filename='hello.gv')
currentNode = None
lastNode = None


def getNext ():
    global token
    global tokenType
    fullRecord = getToken()
    if fullRecord == 'finish':
        g.view()
        exit()
    token = fullRecord.split(',')[0]
    tokenType = fullRecord.split(',')[1]
    #print(token,tokenType)
    
getNext()
    
def programe ():
    '''
        we call it only at beginning of programme 
        takes no input and no output 
    '''
    stmt_sequence()
    
def stmt_sequence ():
    global token
    global tokenType
    statement()
    while token == ';':
        match(';','value')
        statement()
        
def statement():
    global token
    global tokenType
    if token == 'if':
        if_stmt()
    elif token == 'repeat':
        repeat_stmt()
    elif token == 'read':
        read_stmt()
    elif token == 'write':
        write_stmt()
    else:
        assign_stmt()

def if_stmt():
    global token
    global tokenType
    match('if','value')
    exp()
    match('then','value')
    stmt_sequence()
    if token == 'else':
        match('else','value')
        stmt_sequence()
    match('end','value')
    
def repeat_stmt():
    match('repeat','value')
    stmt_sequence()
    match('until','value')
    exp()
    
def assign_stmt():
    match('identifier','type')
    match(':=','value')
    exp()
    
def read_stmt():
    global token
    global tokenType
    global currentNode
    global lastNode
    match('read','value')
    g.attr('node',rankdir='LR',shape='box')
    if currentNode == None and lastNode == None:
        currentNode = str('read \n' + '(' + token + ')')
        g.node(currentNode)
    else:
        lastNode = currentNode
        currentNode = str('read \n' + '(' + token +')')
        g.node(currentNode)
        g.edge(lastNode,currentNode)
    match('identifier','type')
    
def write_stmt():
    global token
    global tokenType
    global currentNode
    global lastNode
    g.attr('node',rankdir='LR',shape='box')
    if currentNode == None and lastNode == None:
        currentNode = 'write'
        g.node(currentNode)
    else:
        lastNode = currentNode
        currentNode = 'write'
        g.node(currentNode)
        g.edge(lastNode,currentNode)
    g.attr('node',rankdir='LR',shape='circle')    
    match('write','value')
    exp()
    
def exp():
    global token
    global tokenType
    simple_exp()
    if token == '<' or token == '=':
        comparison_op()
        simple_exp()
        
def comparison_op():
    global token
    global tokenType
    if token == '<':
        match('<','value')
    elif token == '=':
        match('=','value')

def simple_exp():
    global token
    global tokenType
    term()
    while token == '+' or token == '-':
        addop()
        term()
        
def addop():
    global token
    global tokenType
    if token == '+':
        match('+','value')
    elif token == '-':
        match('-','value')
        
def term():
    global token
    global tokenType
    factor()
    while token == '*' or token == '/':
        mulop()
        factor()
        
def mulop():
    global token
    global tokenType
    if token == '*':
        match('*','value')
    elif token == '/':
        match('/','value')
        
def factor():
    global token
    global tokenType
    if token == '(':
        match('(','value')
        exp()
        match(')','value')
    elif tokenType == 'Number':
        match('Number','type')
    elif tokenType == 'identifier':
        match('identifier','type')
    
def match(matched,by):
    '''
    matched string input to check if it's equals to or equivalent to token 
    by to check by value of token or it's type
    '''
    global token 
    global tokenType
    
    if by == 'value':
        if token == matched:
            #print(token+'\n')
            getNext()
            '''
            we have to draw here
            '''
        else:
            pass
            # put here we must declare error 
    elif by == 'type':
        if tokenType == matched:
            getNext()
            '''
            we have to draw here
            '''
        else:
            pass
            # put here we must declare error 


# In[ ]:

programe()



