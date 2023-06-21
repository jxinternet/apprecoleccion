import mysql.connector
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.config import Config
from datetime import datetime
from kivy.core.window import Window

Config.set("graphics", "width", "500")
Config.set("graphics", "height", "800")


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=[100, 100], spacing=20)

        # Cambiar el fondo a blanco
        Window.clearcolor = (1, 1, 1, 1)
        # Agregar un icono de referencia de reciclaje centrado y arriba
        self.icon = Image(source="recycle_icon.png", size_hint=(1, None), height=50)
        self.layout.add_widget(self.icon)

        self.lbl_title = Label(
            text="APP_Recicladora",
            font_size=40,
            size_hint=(1, None),
            height=100,
            color=(0, 0, 0, 1),
        )
        self.lbl_username = Label(text="Username", color=(0, 0, 0, 1), font_size=18)
        self.txt_username = TextInput(multiline=False, size_hint=(1, None), height=40)
        self.lbl_password = Label(text="Password", color=(0, 0, 0, 1), font_size=18)
        self.txt_password = TextInput(
            multiline=False, password=True, size_hint=(1, None), height=40
        )
        self.btn_login = Button(
            text="Login", background_color=[0, 0.5, 0.5, 1], color=(1, 1, 1, 1)
        )
        self.btn_login.bind(on_press=self.login)
        self.btn_registro = Button(
            text="Registrarse", background_color=[0, 0.5, 0.5, 1], color=(1, 1, 1, 1)
        )
        self.btn_registro.bind(on_press=self.go_to_registro)

        self.layout.add_widget(self.lbl_title)
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
                host="sql9.freesqldatabase.com",
                user="sql9619927",
                password="N3mkJevWzy",
                database="sql9619927",
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
                self.txt_password.text = ""
                self.txt_username.text = ""
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
        self.lbl_name = Label(text="Nombre", color=(0, 0, 0, 1))
        self.layout.add_widget(self.lbl_name)
        self.txt_name = TextInput(multiline=False)
        self.layout.add_widget(self.txt_name)
        self.lbl_lastname = Label(text="Apellido", color=(0, 0, 0, 1))
        self.layout.add_widget(self.lbl_lastname)
        self.txt_lastname = TextInput(multiline=False)
        self.layout.add_widget(self.txt_lastname)
        self.lbl_phone = Label(text="Telefono", color=(0, 0, 0, 1))
        self.layout.add_widget(self.lbl_phone)
        self.txt_phone = TextInput(multiline=False)
        self.layout.add_widget(self.txt_phone)
        self.lbl_address = Label(text="Direccion", color=(0, 0, 0, 1))
        self.layout.add_widget(self.lbl_address)
        self.txt_address = TextInput(multiline=False)
        self.layout.add_widget(self.txt_address)
        self.lbl_user = Label(text="Usuario", color=(0, 0, 0, 1))
        self.layout.add_widget(self.lbl_user)
        self.txt_user = TextInput(multiline=False)
        self.layout.add_widget(self.txt_user)
        self.lbl_password = Label(text="Contraseña", color=(0, 0, 0, 1))
        self.layout.add_widget(self.lbl_password)
        self.txt_password = TextInput(multiline=False, password=True)
        self.layout.add_widget(self.txt_password)
        self.lbl_confirmacion = Label(text="Confirmacion", color=(0, 0, 0, 1))
        self.layout.add_widget(self.lbl_confirmacion)
        self.txt_confirmacion = TextInput(multiline=False, password=True)
        self.layout.add_widget(self.txt_confirmacion)
        self.btn_registrar = Button(text="Registrarse")
        self.btn_registrar.bind(on_press=self.show_popup)
        self.layout.add_widget(self.btn_registrar)

        self.btn_regresar = Button(text="Regresar al Login")
        self.btn_regresar.bind(on_press=self.go_to_login)
        self.layout.add_widget(self.btn_regresar)

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
                host="sql9.freesqldatabase.com",
                user="sql9619927",
                password="N3mkJevWzy",
                database="sql9619927",
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
            popupLabel = "Error: No es un número válido"

        popupLabel = Label(text="Registro Exitoso", color=(0, 0, 0, 1))
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

    def go_to_login(self, instance):
        sm.current = "login"


class SuccessScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=[100, 100], spacing=20)
        self.lbl_success = Label(text="Inicio de sesión exitoso", color=(0, 0, 0, 1))
        self.layout.add_widget(self.lbl_success)
        self.add_widget(self.layout)
        self.btn_back = Button(text="Estrellas")
        self.btn_back.bind(on_press=self.go_to_star)
        self.layout.add_widget(self.btn_back)
        self.btn_back = Button(text="Reciclar")
        self.btn_back.bind(on_press=self.go_to_reciclar)
        self.layout.add_widget(self.btn_back)
        self.btn_rewards = Button(text="Premios")
        self.btn_rewards.bind(on_press=self.go_to_rewards)
        self.layout.add_widget(self.btn_rewards)
        self.btn_sesion = Button(text="Cerrar Sesion")
        self.btn_sesion.bind(on_press=self.go_to_sesion)
        self.layout.add_widget(self.btn_sesion)

    def go_to_rewards(self, instance):
        sm.current = "rewards"

    def go_to_sesion(self, instance):
        sm.current = "login"

    def go_to_reciclar(self, instance):
        sm.current = "reciclar"

    def go_to_star(self, instance):
        sm.current = "star"


class StarScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=[100, 100], spacing=20)
        self.lbl_success = Label(
            text="Aqui puedes ver las estrellas que has acumulado", color=(0, 0, 0, 1)
        )
        self.lbl_star = Label(
            text="Tus estrellas son: ", color=(0, 0, 0, 1), font_size=18
        )
        self.layout.add_widget(self.lbl_success)
        self.layout.add_widget(self.lbl_star)
        self.add_widget(self.layout)

        self.btn_consultar = Button(text="Consultar")
        self.btn_consultar.bind(on_press=self.go_to_consulta)
        self.layout.add_widget(self.btn_consultar)

        self.btn_back = Button(text="Regresar")
        self.btn_back.bind(on_press=self.go_to_success)
        self.layout.add_widget(self.btn_back)

    def go_to_consulta(self, instance):
        try:
            connection = mysql.connector.connect(
                host="sql9.freesqldatabase.com",
                user="sql9619927",
                password="N3mkJevWzy",
                database="sql9619927",
                port=3306,
            )
            cursor = connection.cursor()
            cursor2 = connection.cursor()

            consultaquery = "SELECT estrellas FROM persona WHERE idpersona = %s"
            cursor2.execute(consultaquery, (id,))
            estrellasResultado = cursor2.fetchone()
            estrellasTotal = estrellasResultado[0]
            self.lbl_star.text = f"Tus estrellas son: {estrellasTotal}"
            self.lbl_star.color = (0, 0, 0, 1)

        except ValueError:
            popupLabel = "Error: No es un número válido"

    def go_to_success(self, instance):
        sm.current = "success"


class RewardsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=[100, 100], spacing=20)

        self.btn_pen = Button(text="Lapicero (10 estrellas)")
        self.btn_pen.custom_valor = 10  # Valor personalizado para cada botón
        self.btn_pen.bind(on_press=self.show_popup)

        self.btn_pop = Button(text="Popsocket (20 estrellas)")
        self.btn_pop.custom_valor = 20  # Valor personalizado para cada botón
        self.btn_pop.bind(on_press=self.show_popup)

        self.btn_back = Button(text="Regresar")
        self.btn_back.bind(on_press=self.go_to_success)

        self.layout.add_widget(self.btn_pen)
        self.layout.add_widget(self.btn_pop)
        self.layout.add_widget(self.btn_back)

        self.add_widget(self.layout)

    def show_popup(self, button):
        layout = GridLayout(cols=1, padding=10)
        try:
            connection = mysql.connector.connect(
                host="sql9.freesqldatabase.com",
                user="sql9619927",
                password="N3mkJevWzy",
                database="sql9619927",
                port=3306,
            )
            cursor = connection.cursor()
            cursor2 = connection.cursor()
            valor = button.custom_valor

            consultaquery = "SELECT estrellas FROM persona WHERE idpersona = %s"
            cursor2.execute(consultaquery, (id,))
            estrellasResultado = cursor2.fetchone()
            estrellasTotal = estrellasResultado[0] - valor
            print(id)

            query2 = "UPDATE persona SET estrellas = %s WHERE idpersona = %s"
            cursor.execute(query2, (estrellasTotal, id))
            connection.commit()

            cursor.close()
            connection.close()

        except ValueError:
            popupLabel = "Error: No es un número válido"

        popupLabel = Label(text=f"Se te restarán {valor} estrellas")
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


class ReciclarScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=[100, 100], spacing=20)
        self.lbl_success = Label(
            text="Ingresa los datos de tu reciclaje", color=(0, 0, 0, 1)
        )
        self.lbl_peso = Label(text="Peso", color=(0, 0, 0, 1), font_size=18)

        self.txt_peso = TextInput(multiline=False, size_hint=(1, None), height=40)
        self.lbl_direccion = Label(text="Direccion", color=(0, 0, 0, 1), font_size=18)
        self.txt_direccion = TextInput(multiline=False, size_hint=(1, None), height=40)
        self.btn_back = Button(text="Regresar")
        self.btn_back.bind(on_press=self.go_to_success)
        self.btn_send = Button(text="Realizar pedido")
        self.btn_send.bind(on_press=self.show_popup)
        self.btn_gps = Button(text="Obtener ubicación")
        self.btn_gps.bind(on_press=self.on_button_press)

        self.layout.add_widget(self.lbl_success)
        self.layout.add_widget(self.lbl_peso)
        self.layout.add_widget(self.txt_peso)
        self.layout.add_widget(self.lbl_direccion)
        self.layout.add_widget(self.txt_direccion)
        self.layout.add_widget(self.btn_gps)
        self.layout.add_widget(self.btn_send)
        self.layout.add_widget(self.btn_back)

        self.add_widget(self.layout)

    def on_button_press(self, instance):
        location = self.obtener_ubicacion()
        if location:
            self.txt_direccion.text = f"Ubicación: {location}"
        else:
            self.txt_direccion.text = "No se pudo obtener la ubicación"

    def obtener_ubicacion(self):
        try:
            # Hacer una solicitud a la API de geolocalización basada en IP
            response = requests.get("https://ipapi.co/json/")
            data = response.json()

            # Extraer la ubicación de la respuesta JSON
            if "city" in data and "country_name" in data:
                city = data["city"]
                country = data["country_name"]
                return f"{city}, {country}"
            else:
                return None
        except Exception:
            return None

    def show_popup(self, button):
        layout = GridLayout(cols=1, padding=10)
        try:
            direccion = self.txt_direccion.text
            input_text = self.txt_peso.text
            error = int(input_text)
            calcular_estrellas = float(input_text) * 0.7
            if error > 25:
                resultado = int(calcular_estrellas)

                fechaActual = datetime.now()
                fecha = datetime.strftime(fechaActual, "%Y%m%d")

                connection = mysql.connector.connect(
                    host="sql9.freesqldatabase.com",
                    user="sql9619927",
                    password="N3mkJevWzy",
                    database="sql9619927",
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
                self.lbl_error = ""

                cursor.close()
                connection.close()

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

            else:
                popupLabel = Label(text="El peso debe ser mayor de 25Kg")
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
                self.txt_peso.text = ""
                self.txt_direccion.text = ""

        except ValueError:
            popupLabel = "Error: No es un número válido"

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
        rewards_screen = RewardsScreen(name="rewards")
        sm.add_widget(login_screen)
        sm.add_widget(reciclar_screen)
        sm.add_widget(success_screen)
        sm.add_widget(star_screen)
        sm.add_widget(registro_screen)
        sm.add_widget(rewards_screen)
        return sm


if __name__ == "__main__":
    LoginApp().run()
