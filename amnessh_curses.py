#!/usr/bin/env python

import curses
import sys
import os
import ConfigParser

class AmneSsh:
    DOWN = 1
    UP = -1
    SPACE_KEY = 32
    ENTER_KEY = 10
    TAB_KEY = 9
    ESC_KEY = 27

    config = ConfigParser.RawConfigParser() # global configurator
    config_filepath = os.getenv("HOME") + "/.amnessh.cfg" # settings' file path
    servers = [] # server list

    screen = None

    def __init__(self):
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(1)
        self.screen.border(0)
        self.topLineNum = 0
        self.highlightLineNum = 0
        self.getServers()
        self.run()

    def run(self):
        while True:
            self.displayScreen()
            # get user command
            c = self.screen.getch()
            if c == curses.KEY_UP:
                self.updown(self.UP)
            elif c == curses.KEY_DOWN:
                self.updown(self.DOWN)
            elif c == self.ENTER_KEY:
                self.execCommand()
            else:
                self.exit()

    def execCommand(self):
        linenum = self.topLineNum + self.highlightLineNum
        command = self.servers[linenum][1]
        self.screen.erase()
        self.screen.addstr(0, 0, "connecting...")
        self.screen.refresh()
        os.system(command)
        self.exit()

    def getServers(self):
        if not os.path.isfile(self.config_filepath): # if there's no setttings file create it
            self.config.add_section('Servers')
            with open(self.config_filepath, 'wb') as configfile:
                self.config.write(configfile)
                configfile.close()
        else: # otherwise read it
            self.config.read(self.config_filepath)
            self.servers = self.config.items('Servers')

        self.nservers = len(self.servers)
        print self.servers

    def displayScreen(self):
        # clear screen
        self.screen.erase()

        # now paint the rows
        top = self.topLineNum
        bottom = self.topLineNum+curses.LINES
        for (index,line,) in enumerate(self.servers[top:bottom]):
            line = '%s - %s' % (self.servers[index][0], line[1],)

            # highlight current line
            if index != self.highlightLineNum:
                self.screen.addstr(index, 0, line)
            else:
                self.screen.addstr(index, 0, line, curses.A_BOLD)
        self.screen.refresh()

    # move highlight up/down one line
    def updown(self, increment):
        nextLineNum = self.highlightLineNum + increment

        # paging
        if increment == self.UP and self.highlightLineNum == 0 and self.topLineNum != 0:
            self.topLineNum += self.UP
            return
        elif increment == self.DOWN and nextLineNum == curses.LINES and (self.topLineNum+curses.LINES) != self.nservers:
            self.topLineNum += self.DOWN
            return

        # scroll highlight line
        if increment == self.UP and (self.topLineNum != 0 or self.highlightLineNum != 0):
            self.highlightLineNum = nextLineNum
        elif increment == self.DOWN and (self.topLineNum+self.highlightLineNum+1) != self.nservers and self.highlightLineNum != curses.LINES:
            self.highlightLineNum = nextLineNum

    def restoreScreen(self):
        curses.initscr()
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    # catch any weird termination situations
    def __del__(self):
        self.restoreScreen()


if __name__ == '__main__':
    ih = AmneSsh()
