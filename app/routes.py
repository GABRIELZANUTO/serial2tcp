from pages.login import Login
from pages.home import home_page

def get_route(route):
    if route == "/":
        return Login()
    elif route == "/home":
        return home_page()
    else:
        return Login()  # rota default
