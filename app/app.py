from routes import get_route

def app(page):
    page.title = "Flet Login App"

    def route_change(e):
        page.views.clear()
        page.views.append(get_route(e.route))
        page.update()  # <- MUITO IMPORTANTE

    page.on_route_change = route_change
    page.go("/")  # navega para a rota inicial
