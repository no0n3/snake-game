#!/usr/bin/python

import threading
import time
import os
import sys
import msvcrt
import random

N = 30
directions = {'LEFT': 'left', 'RIGHT': 'right', 'TOP': 'top', 'BOTTOM': 'bottom'}
direction = directions['TOP']

running = True
v = ''

class myThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      global v
      global running

      while running: 
          v = msvcrt.getch().decode("utf-8").lower()

inpT = myThread(1, "Thread-1", 1)
inpT.start()

def addToSnake(x, y):
    global snake
    snake.insert(0, {'x': x, 'y': y})

dot = {'x': 4, 'y': 4}
snake = []
addToSnake(7, 10)
addToSnake(7, 9)
addToSnake(7, 8)

def moveSnake():
    global direction
    global snake
    global N
    global running

    if 'w' == v and direction != directions['BOTTOM']:
        direction = directions['TOP']
    elif 's' == v and direction != directions['TOP']:
        direction = directions['BOTTOM']
    elif 'a' == v and direction != directions['RIGHT']:
        direction = directions['LEFT']
    elif 'd' == v and direction != directions['LEFT']:
        direction = directions['RIGHT']

    f = snake[0]
    tx = f['x']
    ty = f['y']

    if direction == directions['TOP']:
        ty = f['y'] - 1
    elif direction == directions['BOTTOM']:
        ty = f['y'] + 1
    elif direction == directions['LEFT']:
        tx = f['x'] - 1
    elif direction == directions['RIGHT']:
        tx = f['x'] + 1

    if onSnake(tx, ty, 1) or tx < 0 or tx >= N or ty < 0 or ty >= N:
        running = False
        return

    addToSnake(tx, ty)
    if tx == dot['x'] and ty == dot['y']:
        if len(snake) == N * N:
            running = False
            return

        setNewDotPos()
    else:
        snake.pop()

def renderMap():
    global snake

    print (' ', end = '')
    for i in range(N):
        print ('_', end = '')
    print ('')
    for i in range(N):
        print('|', end = '')
        for j in range(N):
            s = ' '
            if onSnake(j, i):
                s = '*'
            elif dot['x'] == j and dot['y'] == i:
                s = '#'
            print (s, end = '')
        print('|', end = '\n')
    print (' ', end = '')
    for i in range(N):
        print ('-', end = '')
    print ('')

def onSnake(x, y, f = 0):
    global snake
    i = f
    while i < len(snake):
        if (snake[i]['x'] == x and snake[i]['y'] == y):
            return 1
        i += 1
    return 0

def setNewDotPos():
    global dot
    global N
    nx = random.randint(0, N - 1)
    ny = random.randint(0, N - 1)
    while onSnake(nx, ny):
        nx = random.randint(0, N - 1)
        ny = random.randint(0, N - 1)

    dot['x'] = nx
    dot['y'] = ny

def setDotPos(x, y):
    global dot
    dot['x'] = x
    dot['y'] = y

lt = int(time.time() * 1000)
while running:
    ct = int(time.time() * 1000)
    if (ct - lt < 150):
        continue
    os.system('cls')
    lt = ct

    moveSnake()
    renderMap()

print ('\nGAME OVER\n')
