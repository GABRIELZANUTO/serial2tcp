import flet as ft

def Navbar(on_mode_change=lambda mode: None):
    mode_selector = ft.SegmentedButton(
    segments=[
        ft.Segment(label=ft.Text("Host"), value="host"),
        ft.Segment(label=ft.Text("Cliente"), value="cliente")
    ],
    selected=["host"],
    allow_multiple_selection=False
)

    def mode_changed(e):
        selected_value = next(iter(mode_selector.selected), None)
        on_mode_change(selected_value)

    mode_selector.on_change = mode_changed

    return ft.Container(
        content=ft.Row(
            [
                ft.Text("Modo de Operação:", weight="bold"),
                mode_selector
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        padding=10,
        bgcolor=ft.colors.BLUE_100,
        border_radius=10
    )
