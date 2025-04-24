import flet as ft
from dotenv import load_dotenv
import os


def Login():
    load_dotenv()

    username = ft.TextField(label="Usuário", autofocus=True,width=600)
    password = ft.TextField(label="Senha", password=True,width=600)
    error_text = ft.Text("", color=ft.colors.RED)

    def login_click(e):
        if username.value == os.getenv("USER") and password.value == os.getenv("PASSWORD"):
            e.page.go("/home")
        else:
            error_text.value = "Usuário ou senha inválidos."
            e.page.update()

    return ft.View(
        route="/",
        controls=[
            ft.Column(
                controls=[
                    ft.Text("Login", size=30, weight="bold"),
                    username,
                    password,
                    error_text,
                    ft.ElevatedButton("Entrar", on_click=login_click),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER
    )
