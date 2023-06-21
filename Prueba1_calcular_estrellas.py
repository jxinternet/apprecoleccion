import mysql.connector
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=[100, 100], spacing=20)
        self.lbl_username = Label(text="Username")
        self.txt_username = TextInput(multiline=False)
        self.lbl_password = Label(text="Password")
        self.txt_password = TextInput(multiline=False, password=True)
        self.btn_login = Button(text="Login")
        self.btn_login.bind(on_press=self.login)
        self.layout.add_widget(self.lbl_username)
        self.layout.add_widget(self.txt_username)
        self.layout.add_widget(self.lbl_password)
        self.layout.add_widget(self.txt_password)
        self.layout.add_widget(self.btn_login)
        self.add_widget(self.layout)

    def login(self, instance):
        try:
            # Conectar a la base de datos MySQL
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="reciclaje",
            )

            # Crear un cursor para ejecutar consultas
            cursor = connection.cursor()

            # Consultar la tabla de usuarios
            query = "SELECT * FROM user WHERE usuario = %s AND password = %s"
            cursor.execute(query, (self.txt_username.text, self.txt_password.text))

            # Obtener el resultado de la consulta
            result = cursor.fetchone()

            if result:
                sm.current = "success"  # Cambiar a la pantalla de éxito
            else:
                print("Nombre de usuario o contraseña incorrectos")

            # Cerrar la conexión y liberar recursos
            cursor.close()
            connection.close()

        except mysql.connector.Error as error:
            print("Error al conectarse a la base de datos:", error)


class SuccessScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=[100, 100], spacing=20)
        self.lbl_success = Label(text="Inicio de sesión exitoso")
        self.layout.add_widget(self.lbl_success)
        self.add_widget(self.layout)
        self.btn_back = Button(text="Estrellas")
        self.btn_back.bind(on_press=self.go_to_star)
        self.layout.add_widget(self.btn_back)
        self.btn_back = Button(text="Reciclar")
        self.btn_back.bind(on_press=self.go_to_reciclar)
        self.layout.add_widget(self.btn_back)

    def go_to_reciclar(self, instance):
        sm.current = "reciclar"

    def go_to_star(self, instance):
        sm.current = "star"


class StarScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=[100, 100], spacing=20)
        self.lbl_success = Label(text="Aqui puedes ver las estrellas que has acumulado")
        self.layout.add_widget(self.lbl_success)
        self.add_widget(self.layout)
        self.btn_back = Button(text="Regresar")
        self.btn_back.bind(on_press=self.go_to_success)
        self.layout.add_widget(self.btn_back)

    def go_to_success(self, instance):
        sm.current = "success"


class ReciclarScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=[100, 100], spacing=20)
        self.lbl_success = Label(text="Ingresa los datos de tu reciclaje")
        self.lbl_peso = Label(text="Peso")
        self.txt_peso = TextInput(multiline=False)
        self.lbl_result = Label(text="Resultado:")
        self.btn_calcular = Button(text="Calcular estrellas")
        self.btn_calcular.bind(on_press=self.calcular_estrellas)
        self.btn_back = Button(text="Regresar")
        self.btn_back.bind(on_press=self.go_to_success)

        self.layout.add_widget(self.lbl_success)
        self.layout.add_widget(self.lbl_peso)
        self.layout.add_widget(self.txt_peso)
        self.layout.add_widget(self.lbl_result)
        self.layout.add_widget(self.btn_back)
        self.add_widget(self.layout)
        self.layout.add_widget(self.btn_calcular)

    def calcular_estrellas(self, instance):
        try:
            input_text = self.txt_peso.text
            calcular_estrellas = float(input_text) * 0.7
            resultado = int(calcular_estrellas)

            self.lbl_result.text = f"Las estrellas que acumularias serian: {resultado}"
        except ValueError:
            self.lbl_result.text = "Error: No es un nùmero valido"

    def go_to_success(self, instance):
        sm.current = "success"


class LoginApp(App):
    def build(self):
        global sm
        sm = ScreenManager()
        login_screen = LoginScreen(name="login")
        success_screen = SuccessScreen(name="success")
        star_screen = StarScreen(name="star")
        reciclar_screen = ReciclarScreen(name="reciclar")
        sm.add_widget(login_screen)
        sm.add_widget(reciclar_screen)
        sm.add_widget(success_screen)
        sm.add_widget(star_screen)
        return sm


if __name__ == "__main__":
    LoginApp().run()
