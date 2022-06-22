"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p2.py 
Author: <Add name here>

Purpose: Part 2 of assignment 09, finding the end position in the maze

Instructions:
- Do not create classes for this assignment, just functions
- Do not use any other Python modules other than the ones included
- Each thread requires a different color by calling get_color()


This code is not interested in finding a path to the end position,
However, once you have completed this program, describe how you could 
change the program to display the found path to the exit position.

What would be your strategy?  

<Answer here>


Why would it work?

<Answer here>

"""
import math
import threading

from cv2 import fastNlMeansDenoising 
from screen import Screen
from maze import Maze
import sys
import cv2

# Include cse 251 common Python files - Dont change
from cse251 import *

SCREEN_SIZE = 600
COLOR = (0, 0, 255)
COLORS = (
    (255,0,0),
    (0,255,0),
    (255,0,0),
    (255,255,0),
    (0,255,255),
    (255,0,255),
    (128,0,0),
    (128,128,0),
    (0,128,0),
    (128,0,128),
    (0,128,128),
    (0,0,128),
    (72,61,139),
    (143,143,188),
    (226,138,43),
    (128,114,250)
)

# Globals
current_color_index = 0
thread_count = 0
stop = False

def get_color():
    """ Returns a different color when called """
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color

def solve_thread(maze, move, path, end, falses):
    old_falses = falses
    searching = False
    complete = False
    moveset = []
    thread_list = []
    color = get_color()
    maze.move(move[0],move[1],color)
    moveset.append(move)
    false_count = 0
    while end[0] == False:
        possible_moves = maze.get_possible_moves(move[0],move[1])
        if len(possible_moves) == 1:
            move = possible_moves[0]
            moveset.append(move)
            maze.move(move[0],move[1], color)
        elif len(possible_moves) == 0:
            complete = True
            if maze.at_end(move[0],move[1]) == True:
                for move in moveset:
                    path.append(move)
                    end.pop()
                    end.append(True)
                searching = True
            else:
                falses.append(False)
                for move in moveset:
                    maze.restore(move[0],move[1])
                for move in moveset:
                    moveset.remove(move)
                break
        else:
            falses = []
            for x in possible_moves:
                move = x
                thread = threading.Thread(target = solve_thread, args=(maze, move, moveset, end, falses))
                thread_list.append(thread)
                false_count += 1
            for t in thread_list:
                t.start()
            for t in thread_list:
                t.join()
            complete = True
            searching = True
            if false_count == len(falses):
                for move in moveset:
                    maze.restore(move[0],move[1])
                falses = old_falses
                falses.append(False)
            break
    if searching == False:
        for move in moveset:
            maze.restore(move[0],move[1])
    if complete == False:
        falses.append(False)

def solve_find_end(maze):
    """ finds the end position using threads.  Nothing is returned """
    # When one of the threads finds the end position, stop all of them
    path = []
    thread_list = []
    end = [False]
    falses = []
    start = maze.get_start_pos()
    path.append(start)
    maze.move(start[0],start[1],COLOR)
    move = start
    while end[0] == False:
        possible_moves = maze.get_possible_moves(move[0],move[1])
        print(possible_moves)
        if len(possible_moves) == 1:
            move = possible_moves[0]
            path.append(move)
            maze.move(move[0],move[1], COLOR)
        elif len(possible_moves) == 0:
            if maze.at_end(move[0],move[1]) == True:
                end == True
            else:
                for move in path:
                    maze.restore(move[0],move[1])
        else:
            for x in possible_moves:
                move = x
                thread = threading.Thread(target = solve_thread, args=(maze, move, path, end, falses))
                thread_list.append(thread)
            for t in thread_list:
                t.start()
            for t in thread_list:
                t.join()
            break


def find_end(log, filename, delay):
    """ Do not change this function """

    global thread_count

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    solve_find_end(maze)

    log.write(f'Number of drawing commands = {screen.get_command_count()}')
    log.write(f'Number of threads created  = {thread_count}')

    done = False
    speed = 1
    while not done:
        if screen.play_commands(speed): 
            key = cv2.waitKey(0)
            if key == ord('+'):
                speed = max(0, speed - 1)
            elif key == ord('-'):
                speed += 1
            elif key != ord('p'):
                done = True
        else:
            done = True



def find_ends(log):
    """ Do not change this function """

    files = (
        ('verysmall.bmp', True),
        ('verysmall-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False)
    )

    log.write('*' * 40)
    log.write('Part 2')
    for filename, delay in files:
        log.write()
        log.write(f'File: {filename}')
        find_end(log, filename, delay)
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_ends(log)



if __name__ == "__main__":
    main()