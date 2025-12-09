#libs
import curses

#globais
tela = 1
options = 1

#config inicial
class Config:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        
    def screen_config(self):  
        curses.curs_set(0)
        self.stdscr.nodelay(True)
        self.stdscr.keypad(True)
        
#menus e funcoes base de menus
class Menu:
    def __init__(self, stdscr, x, y, y_cursor, options):
        self.x = x
        self.y = y
        self.y_cursor = y_cursor
        self.stdscr = stdscr
        self.options_max = options
    
    def move_cursor(self):
        global tela
        global options
        key = self.stdscr.getch()

        if (key == curses.KEY_UP or key == ord("w")) and options > 1 :
            self.y_cursor -= 1
            options -=1

        if (key == curses.KEY_DOWN or key == ord("s")) and options < self.options_max:
            self.y_cursor += 1
            options += 1

        if key == ord("q"):
            tela = False
        
    
    def inicial(self):
        Config(self.stdscr).screen_config()
        while True:
            self.stdscr.clear()
            self.stdscr.addstr(self.y,self.x, "novo jogo")
            self.stdscr.addstr(self.y_cursor,self.x-2, ">")
            self.stdscr.addstr(self.y+1,self.x, "continuar")
            self.stdscr.addstr(self.y+2,self.x, "documentação")
            self.stdscr.addstr(self.y+3,self.x, "créditos")
            self.stdscr.refresh()
            self.move_cursor()
        

def main(stdscr):
    global tela
    while tela == 1:
        Menu(stdscr,5,2,2,4).inicial()
        
curses.wrapper(main)
