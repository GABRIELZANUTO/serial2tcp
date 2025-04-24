import flet as ft
from .components.navbar import Navbar

def home_page():
    def logout_click(e):
        e.page.go("/")

    # Função chamada sempre que o modo muda
    def handle_mode_change(mode):
        print(f"Modo selecionado: {mode}")
        # Aqui você pode atualizar o estado da página, trocar de layout, etc.

    navbar = Navbar(on_mode_change=handle_mode_change)

    return ft.View(
        "/home",
        [
            navbar,
            ft.Text("Bem-vindo à Home!", size=24),
            ft.ElevatedButton("Sair", on_click=logout_click),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
