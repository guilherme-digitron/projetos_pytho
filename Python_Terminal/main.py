import curses

class Config:
    
    def __init__(self, stdscr, x, y, y_cursor) -> None:
        self.stdscr = stdscr
        pass
    
    def initial_config(self):
        curses.curs_set(0)
        self.stdscr.nodelay(True)
        self.stdscr.keypad(True)
        while True:
            self.stdscr.clear()
            self.stdscr.refresh()
    

class Elements:
    
    def __init__(self) -> None:
        pass
    
    def text_centralize(self):
        pass
    

class Menus:
    def __init__(self) -> None:
        pass
    
    def home(self):
        pass

def main(stdscr):
    Config().initial_config()
    Menus().home()

curses.wrapper(main)