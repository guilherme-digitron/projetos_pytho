import curses
from curses.textpad import Textbox
    
class Elements:
    
    def __init__(self, x, y, texto,stdscr) -> None:
        self.x = x
        self.y = y
        self.texto = texto
        self.stdscr = stdscr
    
    #formatacao
    
    def centralize_X(self):
        self.x = (curses.COLS//2) - (len(self.texto)//2)
        return self

    def centralize_Y(self):
         self.y = (curses.LINES//2)
         return self
    
    #elementos
    def addstring (self):
        self.stdscr.addstr(self.y, self.x, self.texto)
        
    def addstring_list (self, list_):
        for i in list_:
            self.stdscr.addstr(self.y, self.x, i)
            self.y += 1   
            
    def addinput(self, alt, lar):
        
        #crio a janela para o input e estilizo ela
        my_win = curses.newwin(alt, lar, self.y, self.x)
        my_win.attron(curses.color_pair(1))
        my_win.box()
        my_win.refresh()
        
        #crio o input
        my_input = Textbox(my_win.derwin(1,lar-2,1,1)).edit().strip()
        
        self.stdscr.addstr(10,10,f"{my_input}")

class Menus:
    def __init__(self, stdscr, x, y, y_cursor) -> None:
        self.stdscr = stdscr
        self.x = x
        self.y = y
        self.y_cursor = y_cursor
    
    def home(self):
        
    #logo do jogo
    # Note o \ no começo para ignorar a primeira quebra de linha do código
        logo_bb = [
        "██████╗             ██████╗ ",
        "██╔══██╗    &       ██╔══██╗",
        "██████╔╝  █████╗    ██████╔╝",
        "██╔══██╗  ╚════╝    ██╔══██╗",
        "██████╔╝            ██████╔╝",
        "╚═════╝             ╚═════╝ "
    ]
        #chama os objetos
        Elements(0, 2,logo_bb[1], self.stdscr).centralize_X().addstring_list(logo_bb)
        Elements(0, 9,"9 - Teste", self.stdscr).centralize_X().addstring_list(["1 - Teste","2 - Teste","3 - Teste","4 - Teste","5 - Teste","6 - Teste","7 - Teste","8 - Teste","9 - Teste"])

def main(stdscr):
    #configs
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.nodelay(True)
    curses.start_color()
    stdscr.clear()
    
    #Inicia um conjunto de cores
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    
    #Principal - ondes menus e objetos sao chmados
    stdscr.clear()
    Menus(stdscr,2,5,5).home()
    stdscr.refresh()
    #desenha o input
    stdscr.nodelay(False)
    Elements(curses.COLS//2 - 20, 15,"", stdscr).addinput(3,40) 
    stdscr.refresh()
    stdscr.getch()
    
curses.wrapper(main)
