# menu.py

from pgzero.keyboard import keys

menu_options = ["Começar", "Música: Ligada", "Sair"]
selected_option = 0
music_on = True
game_state = "menu"

def draw_menu(screen, WIDTH):
    screen.draw.text("Jogo da Galinha!", center=(WIDTH // 2, 100), fontsize=60, color="white")
    for i, option in enumerate(menu_options):
        color = "yellow" if i == selected_option else "white"
        screen.draw.text(option, center=(WIDTH // 2, 200 + i * 50), fontsize=40, color=color)

def update_menu_input(key, music):
    global selected_option, game_state, music_on

    if key == keys.UP:
        selected_option = (selected_option - 1) % len(menu_options)
    elif key == keys.DOWN:
        selected_option = (selected_option + 1) % len(menu_options)
    elif key == keys.RETURN:
        if selected_option == 0:  # Começar
            game_state = "playing"
            if music_on:
                music.play('background')
        elif selected_option == 1:  # Alternar música
            music_on = not music_on
            if music_on:
                menu_options[1] = "Música: Ligada"
                music.play('background')
            else:
                menu_options[1] = "Música: Desligada"
                music.stop()
        elif selected_option == 2:  # Sair
            exit()
