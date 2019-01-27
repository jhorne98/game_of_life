# author Joel Horne

import curses, random #, os, time
from curses import wrapper

stdscr = curses.initscr()

# populates screen with random amounts of █ (ASCII 219), interpreted as a cell
def populateRandom(stdscr, rowsTerm, colsTerm):
    stdscr.erase()
    rows = 0
    cols = 0

    while rows < (rowsTerm):
        while cols < (colsTerm - 1):
            rnd = random.random()
            if rnd > 0.75:
                stdscr.addch(cols, rows, '█')
            cols += 1

        cols = 0
        rows += 1

# creates Bill Gosper's glider gun
def gosper(stdscr):
    stdscr.erase()
    stdscr.addstr(1, 0, "                          █")
    stdscr.addstr(2, 0, "                        █ █")
    stdscr.addstr(3, 0, "              ██      ██            ██")
    stdscr.addstr(4, 0, "             █   █    ██            ██")
    stdscr.addstr(5, 0, "  ██        █     █   ██")
    stdscr.addstr(6, 0, "  ██        █   █ ██    █ █")
    stdscr.addstr(7, 0, "            █     █       █")
    stdscr.addstr(8, 0, "             █   █")
    stdscr.addstr(9, 0, "              ██")

# creates R-Pentomino: smallest methuselah
def rPentomino(stdscr, rowsTerm, colsTerm):
    stdscr.erase()
    midRows = rowsTerm // 2
    midCols = colsTerm // 2

    stdscr.addch(midCols, midRows, '█'); stdscr.addch(midCols - 1, midRows, '█'); stdscr.addch(midCols - 1, midRows + 1, '█'); stdscr.addch(midCols + 1, midRows, '█'); stdscr.addch(midCols, midRows - 1, '█');

# checks if the cell is "live" at row, col
def isLive(stdscr, row, col):
    if stdscr.inch(col, row) == ord('█'):
        return True
    else:
        return False

# totals neighboring live squares
def getNeighbors(stdscr, x, y):
    rows = x - 1
    cols = y - 1
    neighbors = 0

    while rows <= (x + 1):
        while cols <= (y + 1):
            if isLive(stdscr, rows, cols):
                neighbors += 1

            cols += 1

        cols = y - 1
        rows += 1

    if isLive(stdscr, x, y):
        neighbors -= 1

    return neighbors

# implementation of GOL logic: tests each cell and marks for flip
def mark(stdscr, rowsTerm, colsTerm):
    rows = 0
    cols = 0
    coordList = []

    while rows < (rowsTerm):
        while cols < (colsTerm - 1):
            ''' 
            # this could really be one long if-statment rather than three
            if isLive(stdscr, rows, cols) and getNeighbors(stdscr, rows, cols) < 2:
                coordList.append((rows, cols))
            elif isLive(stdscr, rows, cols) and getNeighbors(stdscr, rows, cols) > 3:
                coordList.append((rows, cols))
            elif isLive(stdscr, rows, cols) == False and getNeighbors(stdscr, rows, cols) == 3:
                coordList.append((rows, cols))
            '''

            # good christ
            if (isLive(stdscr, rows, cols) and getNeighbors(stdscr, rows, cols) < 2) or (isLive(stdscr, rows, cols) and getNeighbors(stdscr, rows, cols) > 3) or (isLive(stdscr, rows, cols) == False and getNeighbors(stdscr, rows, cols) == 3):
                coordList.append((rows, cols))

            cols += 1

        cols = 0
        rows += 1

    return coordList

# gets the current state of stdscr in coordList form
def state(stdscr, rowsTerm, colsTerm):
    rows = 0
    cols = 0
    coordList = []

    while rows < (rowsTerm):
        while cols < (colsTerm - 1):
            if isLive(stdscr, rows, cols):
                coordList.append((rows, cols))

            cols += 1

        cols = 0
        rows += 1

    return coordList

# write live cells only based on coordList: use only with state()
def write(stdscr, coordList):
    for i in range(0, len(coordList)):
        (row, col) = coordList[i]

        stdscr.addch(col, row, '█')

# write live and dead cells using coordList from mark()
def update(stdscr, coordList):
     for i in range (0, len(coordList)):
        (row, col) = coordList[i]

        if stdscr.inch(col, row) == ord('█'):
            stdscr.addch(col, row, ' ')
        elif stdscr.inch(col, row) == ord(' '):
            stdscr.addch(col, row, '█')

# replace all char inside border of window with ' '
def clearInside(window):
    (colsWin, rowsWin) = window.getmaxyx()

    for rows in range(1, rowsWin - 1):
        for cols in range(1, colsWin - 1):
            window.addch(cols, rows, ' ')

def main(stdscr):
    #(rowsTerm, colsTerm) = os.get_terminal_size()
    (colsTerm, rowsTerm) = stdscr.getmaxyx()
    coordList = []
    generations = 0
    run = True

    curses.noecho()
    curses.cbreak()
    curses.curs_set(False)

    populateRandom(stdscr, rowsTerm, colsTerm)

    while(run):
        menu = curses.newwin(5, 20, 1, 2)

        stdscr.nodelay(1)
        stdscr.overlay(menu)

        coordList = mark(stdscr, rowsTerm, colsTerm)

        update(stdscr, coordList)

        # realtime tick update
        stdscr.addstr(colsTerm - 1, 0, "Generation:")
        sGen = str(generations)
        stdscr.addstr(colsTerm - 1, 12, sGen)
        generations += 1

        # menu
        if stdscr.getch() == ord('p'):
            stdscr.nodelay(0)
            coordList = state(stdscr, rowsTerm, colsTerm)
            stdscr.erase()

            menu.border(0)
            clearInside(menu)
            menu.addstr(0, 1, "Menu")
            menu.addstr(1, 1, "Resume - p")
            menu.addstr(2, 1, "Initial State - i")
            menu.addstr(3, 1, "Quit - q")
            menu.overlay(stdscr)

            choice = stdscr.getch()
            if choice == ord('q'):
                run = False
                break # enables smooth menu killing
            elif choice == ord('i'):
                clearInside(menu)
                menu.addstr(1, 1, "Random - a")
                menu.addstr(2, 1, "Gosper's Gun - g")
                menu.addstr(3, 1, "Pentomino - e")

                menu.refresh()
                choice = stdscr.getch()

            elif choice == ord('p'):
                pass


            stdscr.clear()

            if choice == ord('a'):
                populateRandom(stdscr, rowsTerm, colsTerm)
                generations = 0
            elif choice == ord('g'):
                gosper(stdscr)
                generations = 0
            elif choice == ord('e'):
                rPentomino(stdscr, rowsTerm, colsTerm)
                generations = 0
            else:
                write(stdscr, coordList)

    curses.nocbreak()
    curses.echo()
    curses.endwin()

    print("Total generations passed:", generations)

#wrapper(main)
main(stdscr)

#TODO figure out rows/cols bullshit
