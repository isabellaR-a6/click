import asyncio
import flet as ft

async def main(page: ft.Page):
    page.on_disconnect = lambda e: print("Jogo encerrado.")
    
    page.title = "Cabo de Guerra Numérico"
    page.padding = 0
    page.spacing = 0
    
    score = 0
    game_started = False
    game_over = False

    score_text = ft.Text(
        "", 
        size=120, 
        weight=ft.FontWeight.BOLD, 
        color=ft.Colors.WHITE,
        text_align=ft.TextAlign.CENTER
    )

    # Lado Vermelho (-) na parte superior
    top_side = ft.Container(
        content=ft.Text("-", size=120, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
        alignment=ft.Alignment(0, 0),
        bgcolor=ft.Colors.RED_700,
        ink=True, 
        expand=5
    )

    # Lado Azul (+) na parte inferior
    bottom_side = ft.Container(
        content=ft.Text("+", size=120, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
        alignment=ft.Alignment(0, 0),
        bgcolor=ft.Colors.BLUE_700,
        ink=True,
        expand=5
    )

    def update_screen_proportions():
        nonlocal score
        
        if score >= 5:
            top_side.visible = False
            bottom_side.visible = True
            bottom_side.expand = 1
        elif score <= -5:
            bottom_side.visible = False
            top_side.visible = True
            top_side.expand = 1
        else:
            top_side.visible = True
            bottom_side.visible = True
            top_side.expand = 5 - score
            bottom_side.expand = 5 + score

    # Handler assíncrono nativo do Flet
    async def start_countdown(e):
        nonlocal game_started
        start_btn.visible = False
        score_text.size = 120
        page.update()
        
        for i in [3, 2, 1]:
            score_text.value = str(i)
            page.update()
            await asyncio.sleep(0.8) # Pausa sem bloquear a interface no Desktop
            
        score_text.value = "JÁ!"
        page.update()
        await asyncio.sleep(0.5)
            
        score_text.value = str(score)
        game_started = True  # Libera os cliques
        page.update()

    def reset_game(e):
        nonlocal score, game_started, game_over
        score = 0
        game_started = False
        game_over = False
        
        top_side.content = ft.Text("-", size=120, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
        bottom_side.content = ft.Text("+", size=120, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
        
        top_side.on_click = btn_minus_click
        bottom_side.on_click = btn_plus_click
        
        restart_btn.visible = False
        start_btn.visible = True
        score_text.value = ""
        
        update_screen_proportions()
        page.update()

    start_btn = ft.ElevatedButton(
        content=ft.Text("Começar Jogo", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
        on_click=start_countdown,
        bgcolor=ft.Colors.WHITE,
    )

    restart_btn = ft.ElevatedButton(
        content=ft.Text("Jogar Novamente", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
        visible=False,
        on_click=reset_game,
        bgcolor=ft.Colors.WHITE,
    )

    def finish_game(winner_team):
        nonlocal game_over, game_started
        game_over = True
        game_started = False
        
        top_side.on_click = None
        bottom_side.on_click = None
        
        top_side.content = None
        bottom_side.content = None
        
        score_text.size = 45
        score_text.value = f"Time {winner_team} ganhou!"
        restart_btn.visible = True

    def btn_minus_click(e):
        nonlocal score, game_started, game_over
        if not game_started or game_over:
            return
            
        score -= 1
        score_text.value = str(score)
        update_screen_proportions()
        
        if score <= -5:
            finish_game("Vermelho")
        page.update()

    def btn_plus_click(e):
        nonlocal score, game_started, game_over
        if not game_started or game_over:
            return
            
        score += 1
        score_text.value = str(score)
        update_screen_proportions()
        
        if score >= 5:
            finish_game("Azul")
        page.update()

    top_side.on_click = btn_minus_click
    bottom_side.on_click = btn_plus_click

    game_board = ft.Column(
        controls=[top_side, bottom_side],
        spacing=0,
        expand=True
    )

    center_panel = ft.Column(
        controls=[start_btn, score_text, restart_btn],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    main_layout = ft.Stack(
        controls=[
            game_board,
            center_panel
        ],
        alignment=ft.Alignment(0, 0),
        expand=True
    )

    page.add(main_layout)

ft.app(target=main)