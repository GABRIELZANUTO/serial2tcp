import flet as ft

class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.bgcolor = ft.colors.BLACK
        self.page.client_storage.set("mode", "Cliente") if self.page.client_storage.get("mode") is None else None
        self.role = self.page.client_storage.get("mode")
        self.new_mode = None
        self.main()

    def main(self):
        self.authmodal() 
        self.page.appbar = self.appbar()
        self.page.dialog = self.auth_dialog  

        self.content = ft.Container()

        layout = ft.ResponsiveRow(
            columns=12,
            controls=[
                self.content,
                self.page.dialog,
            ],
            expand=True
        )
        self.page.add(layout)

    def appbar(self):
        self.switch = ft.Switch(
            value=True if self.role == "Host" else False,
            on_change=self.switchChange
        )
        self.switch_label = ft.Text(self.role)

        switch_row = ft.Row(
            controls=[
                self.switch_label,
                self.switch
            ],
            alignment=ft.MainAxisAlignment.END,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        return ft.AppBar(
            title=ft.Text("Serial2Tcp"),
            center_title=True,
            bgcolor=ft.colors.SURFACE_VARIANT,
            leading=ft.Icon(ft.icons.MENU),
            actions=[switch_row],
        )

    def authmodal(self):
        self.auth_title = ft.Text("Autenticação")  # título como componente separado

        self.username_input = ft.TextField(label="Usuário", autofocus=True)
        self.password_input = ft.TextField(label="Senha", password=True)

        self.auth_dialog = ft.AlertDialog(
            modal=True,
            title=self.auth_title,  # usa o objeto, não uma string direta
            content=ft.Column([
                self.username_input,
                self.password_input
            ], tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=self.cancelAuth),
                ft.ElevatedButton("Confirmar", on_click=self.auth),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def switchChange(self, e):
        self.new_mode = "Host" if e.control.value else "Cliente"
        self.switch.value = not e.control.value
        self.page.dialog.open = True
        self.page.update()

    def auth(self, e):
        user = self.username_input.value
        password = self.password_input.value
        if user == "1" and password == "1":
            self.username_input.value = ''
            self.password_input.value = ''

            self.role = self.new_mode
            self.page.client_storage.set("mode", self.role)
            self.switch_label.value = self.role
            self.switch.value = True if self.role == "Host" else False
            self.auth_title.color = ft.colors.WHITE
            self.auth_title.value = "Autenticação" 
            self.page.dialog.open = False
            
            self.page.update()
        else:
            self.auth_title.value = "Usuário ou senha inválidos!"
            self.auth_title.color = ft.colors.RED
            self.auth_title.update()

    def cancelAuth(self, e):
        self.page.dialog.open = False
        self.page.update()

if __name__ == '__main__':
    ft.app(target=App)
