from backend.app.app import App
from frontend.interface import run_gui

if __name__ == "__main__":
    app = App()
    run_gui(app) 