#!/usr/bin/env python
# coding: utf-8

# In[23]:


from SCANNER import getToken
from graphviz import Digraph

g = Digraph('G', filename='hello')
g.format = 'png'
g.attr('node',rankdir='LR',shape='box')
currentNode = None
lastNode = None
lastNode_val = None
index = 0
Temp = None

class Error(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message
        
def getNext ():
    global token
    global tokenType
    fullRecord = getToken()
    if fullRecord == 'finish':
        g.view()
    else :
        token = fullRecord.split(',')[0]
        tokenType = fullRecord.split(',')[1]
    

    
def programe ():
    '''
        we call it only at beginning of programme 
        takes no input and no output 
    '''
    getNext() 
    stmt_sequence()
    
def stmt_sequence ():
    global token
    global tokenType
    st1 = statement()
    while token == ';':
        match(';','value')
        statement()
    return st1
        
def statement():
    global token
    global tokenType
    if token == 'if':
        if_stmt()
    elif token == 'repeat':
        repeat_stmt()
    elif token == 'read':
        return read_stmt()
    elif token == 'write':
        return write_stmt()
    else:
        return assign_stmt()

def if_stmt():
    global token
    global tokenType
    global currentNode
    global lastNode
    global lastNode_val
    match('if','value')
    
    if currentNode == None and lastNode == None:
        currentNode = str('if')
        g.node(currentNode)
    else:
        lastNode = currentNode
        currentNode = str('if')
        g.node(currentNode)
        if lastNode_val == 'if' or lastNode_val == 'repeat':
            g.edge(lastNode,currentNode)
        else:
            g.edge(lastNode,currentNode, constraint='false')
        lastNode_val = 'if'
            
    g.edge(currentNode,exp())
    match('then','value')
    g.edge(currentNode,stmt_sequence())
    
    if token == 'else':
        match('else','value')
        g.edge(currentNode,stmt_sequence())
        
    match('end','value')
    
def repeat_stmt():
    global token
    global tokenType
    global currentNode
    global lastNode
    global index
    global Temp
    global lastNode_val
    
    g.attr('node',shape='box')
    if currentNode == None and lastNode == None:
        currentNode = str('n' + str(index))
        g.node(str('n' + str(index)),'repeat')
        index = index + 1
    else:
        lastNode = currentNode
        currentNode = str('n' + str(index))
        g.node(str('n' + str(index)),'repeat')
        index = index + 1
        if lastNode_val == 'if' or lastNode_val == 'repeat':
            pass
        else:
            g.edge(lastNode,currentNode, constraint='false')
        lastNode_val = 'repeat'
    match('repeat','value')
    g.attr('node',rankdir='LR')
    g.edge(currentNode,stmt_sequence())
    match('until','value')
    currentNode = Temp
    g.edge(currentNode,exp())
    
def assign_stmt():
    global token
    global tokenType
    global currentNode
    global lastNode
    global index
    global Temp
    global lastNode_val
    
    tempId = token 
    match('identifier','type')
    g.attr('node',shape='box')
    if currentNode == None and lastNode == None:
        currentNode = str('n' + str(index))
        g.node(str('n' + str(index)),str('assign \n' + '(' + tempId + ')'))
        index = index + 1
    else:
        lastNode = currentNode
        currentNode = str('n' + str(index))
        g.node(str('n' + str(index)),str('assign \n' + '(' + tempId +')'))
        index = index + 1
        if lastNode_val == 'if' or lastNode_val == 'repeat':
            Temp = lastNode
            lastNode_val = None
        else:
            g.edge(lastNode,currentNode, constraint='false')
    match(':=','value')
    g.edge(currentNode,exp())
    return currentNode
    
def read_stmt():
    global token
    global tokenType
    global currentNode
    global lastNode
    global index
    global Temp
    global lastNode_val
    
    match('read','value')
    if currentNode == None and lastNode == None:
        currentNode = str('n' + str(index))
        g.node(str('n' + str(index)),str('read \n' + '(' + token + ')'))
        index = index + 1
    else:
        lastNode = currentNode
        currentNode = str('n' + str(index))
        g.node(str('n' + str(index)),str('read \n' + '(' + token +')'))
        index = index + 1
        if lastNode_val == 'if' or lastNode_val == 'repeat':
            Temp = lastNode
            lastNode_val = None
        else:
            g.edge(lastNode,currentNode, constraint='false')
    match('identifier','type')
    return currentNode

def write_stmt():
    global token
    global tokenType
    global currentNode
    global lastNode
    global index
    global Temp
    global lastNode_val
    
    g.attr('node',rankdir='LR',shape='box')
    if currentNode == None and lastNode == None:
        currentNode = str('n' + str(index))
        g.node(str('n' + str(index)),'write')
        index = index + 1
    else:
        lastNode = currentNode
        currentNode = str('n' + str(index))
        g.node(str('n' + str(index)),'write')
        index = index + 1
        if lastNode_val == 'if' or lastNode_val == 'repeat':
            Temp = lastNode
            lastNode_val = None
        else:
            g.edge(lastNode,currentNode, constraint='false')   
    match('write','value')
    g.attr('node',shape='circle')
    g.edge(currentNode,exp())
    return currentNode
    
def exp():
    global token
    global tokenType
    tokenTempCh1 = simple_exp()
    
    if token == '<' or token == '=':
        tokenTempP = comparison_op()
        g.attr('node',rankdir='TB',shape='circle')
        g.edge(tokenTempP,tokenTempCh1)
        g.edge(tokenTempP,simple_exp())
        
        return tokenTempP
    return tokenTempCh1
        
def comparison_op():
    global token
    global tokenType
    global index
    
    if token == '<':
        tokenTemp = str('n' + str(index))
        g.attr('node',shape='circle')
        g.node(str('n' + str(index)),str('op \n' + '(' + token + ')'))
        index = index + 1
        match('<','value')
        return tokenTemp
    elif token == '=':
        tokenTemp = str('n' + str(index))
        g.attr('node',shape='circle')
        g.node(str('n' + str(index)),str('op \n' + '(' + token + ')'))
        index = index + 1
        match('=','value')
        return tokenTemp
    
def simple_exp():
    global token
    global tokenType
    tokenTemp = term()
    while token == '+' or token == '-':
        tokenTemp1 = addop()
        g.edge(tokenTemp1,tokenTemp)
        g.edge(tokenTemp1,term())
        return tokenTemp1
    
    return tokenTemp
        
def addop():
    global token
    global tokenType
    global index
    
    if token == '+':
        tokenTemp = str('n' + str(index))
        g.attr('node',shape='circle')
        g.node(str('n' + str(index)),str('op \n' + '(' + token + ')'))
        index = index + 1
        match('+','value')
        return tokenTemp
    elif token == '-':
        tokenTemp = str('n' + str(index))
        g.attr('node',shape='circle')
        g.node(str('n' + str(index)),str('op \n' + '(' + token + ')'))
        index = index + 1
        match('-','value')
        return tokenTemp
        
def term():
    global token
    global tokenType
    tokenTemp = factor()
    
    while token == '*' or token == '/':
        tokenTemp1 = mulop()
        g.edge(tokenTemp1,tokenTemp)
        g.edge(tokenTemp1,factor())
        return tokenTemp1   
    return tokenTemp
        
def mulop():
    global token
    global tokenType
    global index
    if token == '*':
        tokenTemp = str('n' + str(index))
        g.attr('node',shape='circle')
        g.node(str('n' + str(index)),str('op \n' + '(' + token + ')'))
        index = index + 1
        match('*','value')
        return tokenTemp
    elif token == '/':
        tokenTemp = str('n' + str(index))
        g.attr('node',shape='circle')
        g.node(str('n' + str(index)),str('op \n' + '(' + token + ')'))
        index = index + 1
        match('/','value')
        return tokenTemp
        
def factor():
    global token
    global tokenType
    global index
    if token == '(':
        match('(','value')
        exp()
        match(')','value')
    elif tokenType == 'Number':
        tokenTemp = str('n' + str(index))
        g.attr('node',shape='circle')
        g.node(str('n' + str(index)),str('const \n' + '(' + token + ')'))
        index = index + 1
        match('Number','type')
        return tokenTemp
    elif tokenType == 'identifier':
        tokenTemp = str('n' + str(index))
        g.attr('node',shape='circle')
        g.node(str('n' + str(index)),str('id \n' + '(' + token + ')'))
        index = index + 1
        match('identifier','type')
        
        return tokenTemp
    
def match(matched,by):
    '''
    matched string input to check if it's equals to or equivalent to token 
    by to check by value of token or it's type
    '''
    global token 
    global tokenType
    if by == 'value':
        if token == matched:
            getNext()
        else:
            raise Error('error : missmatching value of token check it again it excepted to be ' + matched)
                               
    elif by == 'type':
        if tokenType == matched:
            getNext()
        else:
            raise Error('error : missmatching type of token check it again it excepted to be ' + matched)       

# In[ ]:
#programe ()




