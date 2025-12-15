import curses

global key
    
class Elements:
    
    def __init__(self, stdscr, x, y, y_cursor) -> None:
        self.stdscr = stdscr
        self.x = x
        self.y = y
        self.y_cursor = y_cursor
    
    def text_centralize(self):
        pass
    

class Menus:
    def __init__(self, stdscr, x, y, y_cursor) -> None:
        self.stdscr = stdscr
        self.x = x
        self.y = y
        self.y_cursor = y_cursor
    
    def home(self):
        
        self.stdscr.addstr(self.y, self.x, "Creditos")

def main(stdscr):
    #configs
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)
    stdscr.clear()

    while True:
        Menus(stdscr,2,5,5).home()
        
        

curses.wrapper(main)