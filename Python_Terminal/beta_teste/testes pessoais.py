import curses
from curses.textpad import Textbox

def main(stdscr):
    curses.curs_set(1)        # mostra o cursor
    stdscr.clear()
    curses.start_color()

    # cor branca (texto padrão)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    altura, largura = 3, 40
    y, x = 5, 10

    # janela com borda
    win = curses.newwin(altura, largura, y, x)
    win.attron(curses.color_pair(1) | curses.A_BOLD)
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
