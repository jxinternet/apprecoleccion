import mysql.connector
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
from datetime import datetime

Config.set("graphics", "whith", "500")
Config.set("graphics", "height", "800")


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=[100, 100], spacing=20)
        self.lbl_username = Label(text="Username")
        self.txt_username = TextInput(multiline=False)
        self.lbl_password = Label(text="Password")
        self.txt_password = TextInput(multiline=False, password=True)
        self.btn_login = Button(text="Login")
        self.btn_login.bind(on_press=self.login)
        self.btn_registro = Button(text="Registrarse")
        self.btn_registro.bind(on_press=self.go_to_registro)
        self.layout.add_widget(self.lbl_username)
        self.layout.add_widget(self.txt_username)
        self.layout.add_widget(self.lbl_password)
        self.layout.add_widget(self.txt_password)
        self.layout.add_widget(self.btn_login)
        self.layout.add_widget(self.btn_registro)
        self.add_widget(self.layout)

    def login(self, instance):
        try:
            # Conectar a la base de datos MySQL
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="reciclaje",
                port=3306,
            )

            # Crear un cursor para ejecutar consultas
            cursor = connection.cursor()
            cursor2 = connection.cursor()

            consultaquery = (
                "SELECT idpersona FROM user WHERE usuario = %s AND password = %s"
            )
            cursor2.execute(
                consultaquery, (self.txt_username.text, self.txt_password.text)
            )
            idresult = cursor2.fetchone()

            global id
            id = idresult[0]

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

    def go_to_registro(self, instance):
        sm.current = "registro"


class RegistroScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=[50, 50], spacing=10)
        self.lbl_name = Label(text="Nombre")
        self.layout.add_widget(self.lbl_name)
        self.txt_name = TextInput(multiline=False)
        self.layout.add_widget(self.txt_name)
        self.lbl_lastname = Label(
            text="Apellido",
        )
        self.layout.add_widget(self.lbl_lastname)
        self.txt_lastname = TextInput(multiline=False)
        self.layout.add_widget(self.txt_lastname)
        self.lbl_phone = Label(text="Telefono")
        self.layout.add_widget(self.lbl_phone)
        self.txt_phone = TextInput(multiline=False)
        self.layout.add_widget(self.txt_phone)
        self.lbl_address = Label(text="Direccion")
        self.layout.add_widget(self.lbl_address)
        self.txt_address = TextInput(multiline=False)
        self.layout.add_widget(self.txt_address)
        self.lbl_user = Label(text="Usuario")
        self.layout.add_widget(self.lbl_user)
        self.txt_user = TextInput(multiline=False)
        self.layout.add_widget(self.txt_user)
        self.lbl_password = Label(text="Contraseña")
        self.layout.add_widget(self.lbl_password)
        self.txt_password = TextInput(multiline=False, password=True)
        self.layout.add_widget(self.txt_password)
        self.lbl_confirmacion = Label(text="Confirmacion")
        self.layout.add_widget(self.lbl_confirmacion)
        self.txt_confirmacion = TextInput(multiline=False, password=True)
        self.layout.add_widget(self.txt_confirmacion)
        self.btn_registrar = Button(text="Registrarse")
        self.btn_registrar.bind(on_press=self.show_popup)
        self.layout.add_widget(self.btn_registrar)
        self.add_widget(self.layout)

    def show_popup(self, button):
        layout = GridLayout(cols=1, padding=10)
        try:
            name = self.txt_name.text
            lastname = self.txt_lastname.text
            phone = int(self.txt_phone.text)
            address = self.txt_address.text
            user = self.txt_user.text
            password = self.txt_password.text
            confirmacion = self.txt_confirmacion.text
            star = 0

            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="reciclaje",
                port=3306,
            )

            cursor = connection.cursor()
            cursor2 = connection.cursor()
            cursor3 = connection.cursor()

            consultaquery = "INSERT INTO persona (nombre,apellido,telefono,direccion,estrellas) VALUES (%s,%s,%s,%s,%s)"
            cursor2.execute(consultaquery, (name, lastname, phone, address, star))
            connection.commit()

            query = "SELECT idpersona FROM persona WHERE nombre = %s AND apellido = %s"
            cursor.execute(query, (name, lastname))
            result = cursor.fetchone()
            idresult = result[0]

            query3 = "INSERT INTO user (usuario,password,idpersona) VALUES (%s,%s,%s)"
            cursor3.execute(query3, (user, password, idresult))

            if password == confirmacion:
                connection.commit()
                sm.current = "login"

            else:
                print("Contraseña y confirmacion son diferentes")

            # Cerrar la conexión y liberar recursos
            cursor.close()
            connection.close()

        except ValueError:
            popupLabel = "Error: No es un nùmero valido"

        popupLabel = Label(text="Registro Exitoso")
        closeButton = Button(text="Cerrar mensaje")
        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)

        popup = Popup(
            title="Registro",
            content=layout,
            size_hint=(None, None),
            size=(500, 200),
        )

        popup.open()
        closeButton.bind(on_press=popup.dismiss)


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
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="reciclaje",
                port=3306,
            )
            print(id)
            cursor2 = connection.cursor()
            consultaquery = "SELECT estrellas FROM persona WHERE idpersona = %s"
            cursor2.execute(consultaquery, (id,))
            estrellasResultado = cursor2.fetchone()
            estrellasTotal = estrellasResultado[0]

        except ValueError:
            print("error")

        self.lbl_star = Label(text=f"{estrellasTotal}")
        self.layout.add_widget(self.lbl_star)
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
        self.lbl_direccion = Label(text="Direccion")
        self.txt_direccion = TextInput(multiline=False)
        self.btn_back = Button(text="Regresar")
        self.btn_back.bind(on_press=self.go_to_success)
        self.btn_send = Button(text="Realizar pedido")
        self.btn_send.bind(on_press=self.show_popup)

        self.layout.add_widget(self.lbl_success)
        self.layout.add_widget(self.lbl_peso)
        self.layout.add_widget(self.txt_peso)
        self.layout.add_widget(self.lbl_direccion)
        self.layout.add_widget(self.txt_direccion)
        self.layout.add_widget(self.btn_back)
        self.layout.add_widget(self.btn_send)
        self.add_widget(self.layout)

    def show_popup(self, button):
        layout = GridLayout(cols=1, padding=10)
        try:
            direccion = self.txt_direccion.text
            input_text = self.txt_peso.text
            calcular_estrellas = float(input_text) * 0.7
            resultado = int(calcular_estrellas)
            fechaActual = datetime.now()
            fecha = datetime.strftime(fechaActual, "%Y%m%d")

            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="reciclaje",
                port=3306,
            )
            cursor = connection.cursor()
            cursor2 = connection.cursor()

            consultaquery = "SELECT estrellas FROM persona WHERE idpersona = %s"
            cursor2.execute(consultaquery, (id,))
            estrellasResultado = cursor2.fetchone()
            estrellasTotal = estrellasResultado[0] + resultado
            print(id)
            query = "INSERT INTO Pedidos (peso,direccion,idpersona,fecha) VALUES (%s,%s,%s,%s)"
            cursor.execute(query, (input_text, direccion, id, fecha))
            connection.commit()
            query2 = "UPDATE persona SET estrellas = %s WHERE idpersona = %s"
            cursor.execute(query2, (estrellasTotal, id))
            connection.commit()
            self.txt_peso.text = ""
            self.txt_direccion.text = ""

            cursor.close()
            connection.close()

        except ValueError:
            popupLabel = "Error: No es un nùmero valido"

        popupLabel = Label(text=f"Estrellas obtenidas: {resultado}")
        closeButton = Button(text="Cerrar mensaje")
        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)

        popup = Popup(
            title="Mensaje Emergente",
            content=layout,
            size_hint=(None, None),
            size=(500, 200),
        )

        popup.open()
        closeButton.bind(on_press=popup.dismiss)

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
        registro_screen = RegistroScreen(name="registro")
        sm.add_widget(login_screen)
        sm.add_widget(reciclar_screen)
        sm.add_widget(success_screen)
        sm.add_widget(star_screen)
        sm.add_widget(registro_screen)
        return sm


if __name__ == "__main__":
    LoginApp().run()
