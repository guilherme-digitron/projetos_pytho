"""#libs
import curses

#globais
tela = 1
options = 1

#config inicial
class Config:
    def __init__(self, stdscr, y,x, y_cursor, texto):
        self.stdscr = stdscr
        self.y = y
        self.x = x
        self.y_cursor = y_cursor
        self.texto = texto
        
    def screen_config(self):  
        curses.curs_set(0)
        self.stdscr.nodelay(True)
        self.stdscr.keypad(True)
        
    def X_middle(self):
        self.x = int((curses.COLS//2) - (len(self.texto)//2))
        return self.x
    
    def Y_middle(self):
        self.y = int((curses.LINES//2) - (len(self.texto)//2))
        return self.y
    
    def Text(self):
        return self.texto
    
    
    def X(self):
        return self.x
    
    def Y(self):
        return self.y
    
    def Y_cursor(self):
        return self.y_cursor

        
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
        option1 = Config(self.stdscr,self.y,self.x,self.y_cursor,"Créditos")
        self.x = option1.X_middle()
        self.y = option1.Y_middle()
        self.y_cursor = option1.Y_cursor()
        Config(self.stdscr,0,0,0,0).screen_config()
        while True:
            self.stdscr.clear()
            self.stdscr.addstr(self.y,self.x, "Créditos")
            self.stdscr.refresh()
            self.move_cursor()
        

def main(stdscr):
    global tela
    while tela == 1:
        Menu(stdscr,5,2,2,4).inicial()
        
curses.wrapper(main)"""
import curses
from curses.textpad import Textbox

def main(stdscr):
    curses.curs_set(1)        # mostra o cursor
    stdscr.clear()
    curses.start_color()

    # cor branca (texto padrão)
    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    altura, largura = 3, 40
    y, x = 5, 10

    # janela com borda
    win = curses.newwin(altura, largura, y, x)
    win.attron(curses.color_pair(1))
    win.box()
    win.refresh()

    # área interna para digitar
    input_win = win.derwin(1, largura - 2, 1, 1)
    textbox = Textbox(input_win)

    # digitação (ENTER envia)
    texto = textbox.edit().strip()

    # mostrar o que foi digitado
    stdscr.addstr(10, 10, f"Texto digitado: {texto}")
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)
