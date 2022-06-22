"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p1.py 
Author: <Add name here>

Purpose: Part 1 of assignment 09, finding a path to the end position in a maze

Instructions:
- Do not create classes for this assignment, just functions
- Do not use any other Python modules other than the ones included

"""
import math
from screen import Screen
from maze import Maze
import cv2
import sys
import threading

# Include cse 251 common Python files - Dont change
from cse251 import *

SCREEN_SIZE = 600
COLOR = (0, 0, 255)

# TODO add any functions

def check_path(maze,move,path):
    start = move
    moveset = []
    while True:
        if maze.at_end(move[0],move[1]) == True:
            if maze.can_move_here(move[0], move[1]) == True:
                maze.move(move[0],move[1],COLOR)
            path.append(move)
            return path
        else:
            maze.move(move[0],move[1],COLOR)
            moves = maze.get_possible_moves(move[0],move[1])
            for move in moves:
                if maze.can_move_here(move[0], move[1]) == True:
                    pass
                else:
                    moves.remove(move)
            if len(moves) == 1:
                maze.move(move[0], move[1], COLOR)
                moveset.append(move)
            elif len(moves) == 0:
                for move in moveset:
                    maze.restore(move[0],move[1])
                maze.restore(start[0],start[1])
                return path
            else:
                for move in moves:
                    path = check_path(maze,move,path)
                    move = path[-1]
                    if maze.at_end(move[0],move[1]) == True:
                        if maze.can_move_here(move[0], move[1]) == True:
                            maze.move(move[0],move[1],COLOR)
                        path.append(move)
                        return path
            
def solve_path(maze):
    """ Solve the maze and return the path found between the start and end positions.  
        The path is a list of positions, (x, y) """
    # TODO start add code here
    path = []
    start = maze.get_start_pos()
    path.append(start)
    if maze.can_move_here(start[0], start[1]) == True:
        maze.move(start[0], start[1], COLOR)
    move = start
    while True:
        if maze.at_end(move[0],move[1]) == True:
            if maze.can_move_here(move[0], move[1]) == True:
                maze.move(move[0],move[1],COLOR)
            return path
        else:
            moves = maze.get_possible_moves(move[0],move[1])
            for move in moves:
                if maze.can_move_here(move[0], move[1]) == True:
                    pass
                else:
                    moves.remove(move)
            if len(moves) == 1:
                if maze.can_move_here(move[0], move[1]) == True:
                    maze.move(move[0], move[1], COLOR)
            else:
                for move in moves:
                    path = check_path(maze,move,path)
                    move = path[-1]
                    if maze.at_end(move[0],move[1]) == True:
                        if maze.can_move_here(move[0], move[1]) == True:
                            maze.move(move[0],move[1],COLOR)
                        path.append(move)
                        return path

def get_path(log, filename):
    """ Do not change this function """

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename)

    path = solve_path(maze)

    log.write(f'Number of drawing commands for = {screen.get_command_count()}')

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

    return path


def find_paths(log):
    """ Do not change this function """

    files = ('verysmall.bmp', 'verysmall-loops.bmp', 
            'small.bmp', 'small-loops.bmp', 
            'small-odd.bmp', 'small-open.bmp', 'large.bmp', 'large-loops.bmp')

    log.write('*' * 40)
    log.write('Part 1')
    for filename in files:
        log.write()
        log.write(f'File: {filename}')
        path = get_path(log, filename)
        log.write(f'Found path has length          = {len(path)}')
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_paths(log)


if __name__ == "__main__":
    main()