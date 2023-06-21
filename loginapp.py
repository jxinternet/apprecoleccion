import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
import sqlite3
from sqlite3 import Error

kivy.require('1.11.1')

    
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('myapp.db')
    except Error as e:
        print(e)

    return conn

def init_db():
    conn = create_connection()  # Utilizar create_connection() en lugar de connect_db()
    if conn is None:
        print("No se pudo conectar con la base de datos para inicializarla.")
        return

    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            address TEXT,
            phone TEXT
        )
    ''')

    conn.commit()
    conn.close()

def check_credentials(username, password):
    conn = create_connection()
    cursor = conn.cursor()

    # Utilizar una consulta SQL preparada para buscar un usuario en la base de datos
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return False
    else:
        return True


def register_user(username, password, address, phone):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO users (username, password, address, phone) VALUES (?, ?, ?, ?)
        ''', (username, password, address, phone))

        conn.commit()

        # Verificar las credenciales del usuario recién registrado
        if check_credentials(username, password):
            return True
        else:
            return False

    except sqlite3.IntegrityError:
        print("Error: El nombre de usuario ya existe.")
        return False

    finally:
        conn.close()




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

        register_button = Button(text="Registrarse")
        register_button.bind(on_press=self.go_to_register)
        layout.add_widget(register_button)

        self.login_status_label = Label(text="")
        layout.add_widget(self.login_status_label)

        self.add_widget(layout)

    def login_user(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if check_credentials(username, password):
            self.manager.current = 'register'
            self.login_status_label.text = ""
        else:
            self.login_status_label.text = "Nombre de usuario o contraseña incorrectos"

    def go_to_register(self, instance):
        register_screen = None
        for screen in self.manager.screens:
            if screen.name == 'register':
                register_screen = screen
                break

        if register_screen is None:
            register_screen = RegisterScreen()
            self.manager.add_widget(register_screen)

        self.manager.current = register_screen.name



class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        self.name = 'register'

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        layout.add_widget(Label(text="Nombre de usuario:"))
        self.username_input = TextInput(multiline=False)
        layout.add_widget(self.username_input)

        layout.add_widget(Label(text="Contraseña:"))
        self.password_input = TextInput(multiline=False, password=True)
        layout.add_widget(self.password_input)

        layout.add_widget(Label(text="Dirección:"))
        self.address_input = TextInput(multiline=False)
        layout.add_widget(self.address_input)

        layout.add_widget(Label(text="Número de teléfono:"))
        self.phone_input = TextInput(multiline=False)
        layout.add_widget(self.phone_input)

        register_button = Button(text="Registrarse")
        register_button.bind(on_press=self.register_user)
        layout.add_widget(register_button)

        back_button = Button(text="Regresar")
        back_button.bind(on_press=self.back_to_login)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def register_user(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        address = self.address_input.text
        phone = self.phone_input.text
    
        # Llamar a la función para registrar un usuario en la base de datos
        register_user(username, password, address, phone)

        # Cambiar a la pantalla de inicio de sesión.
        self.manager.current = 'login'


    def back_to_login(self, instance):
        self.manager.current = 'login'



class MyApp(App):
    def build(self):
        init_db()

        screen_manager = ScreenManager()
        screen_manager.add_widget(LoginScreen())
        screen_manager.add_widget(RegisterScreen())

        return screen_manager


if __name__ == '__main__':
    MyApp().run()
