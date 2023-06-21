import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview import RecycleView

kivy.require('2.0.0')


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.name = 'login'

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        layout.add_widget(Label(text="Nombre de usuario:"))
        self.username_input = TextInput(multiline=False)
        layout.add_widget(self.username_input)

        layout.add_widget(Label(text="Contraseña:"))
        self.password_input = TextInput(multiline=False, password=True)
        layout.add_widget(self.password_input)

        login_button = Button(text="Iniciar sesión")
        login_button.bind(on_press=self.login_user)
        layout.add_widget(login_button)

        self.add_widget(layout)

    def login_user(self, instance):
        # Aquí puedes verificar las credenciales del usuario
        # y pasar a la siguiente pantalla si las credenciales son correctas.
        pass


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.name = 'main'

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Aquí puedes agregar los elementos de la interfaz de usuario
        # para las características principales de la aplicación.

        self.add_widget(layout)


class PaperRecyclingApp(App):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(LoginScreen())
        screen_manager.add_widget(MainScreen())

        return screen_manager


if __name__ == "__main__":
    PaperRecyclingApp().run()
