import curses
    
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
        Elements(0, 9,"Documentação", self.stdscr).centralize_X().addstring_list(["Iniciar","Créditos","Documentação"])
        if key == ord("q"):
            exit()

def main(stdscr):
    #configs
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)
    stdscr.clear()
    
    #seta a global que captura as teclas
    global key
    
    #loop principal *limpa a tela *redesenha *recarrega
    while True:
        #deve pegar a tecla primeiro
        key = stdscr.getch()
        stdscr.clear()
        Menus(stdscr,2,5,5).home()
        stdscr.refresh()
        
curses.wrapper(main)
