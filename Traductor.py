from PySide6.QtWidgets import QMainWindow,QApplication, QMessageBox,QButtonGroup, QVBoxLayout, QRadioButton, QHBoxLayout, QWidget, \
    QPushButton, QComboBox, QLabel, QTextEdit, QGridLayout
from PySide6.QtGui import QColor, QPalette, QIcon, QPixmap
from PySide6.QtCore import QSize, QEvent, Qt,Signal
import sys, os, random, requests
import threading
import pyttsx3
from tempfile import NamedTemporaryFile

from deep_translator import GoogleTranslator, MyMemoryTranslator

Basedir = os.path.dirname(__file__)

try:
    from ctypes import windll

    myappid = 'andresCA.traductor.subproduct.0.0.0.1'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


class Color_app(QWidget):
    def __init__(self, Color):
        super().__init__()
        self.setAutoFillBackground(True)
        Palette = self.palette()
        Palette.setColor(QPalette.ColorRole.Window, QColor(Color))
        self.setPalette(Palette)


class Traductor_App(QMainWindow):
    mostrar_mensaje_signal = Signal(str, str)
    mostrar_mensaje_signal_inf = Signal(str, str)
    def __init__(self):
        super().__init__()
        self.DerechaGLayout = QVBoxLayout()
        self.IzquierdaGLayout = QVBoxLayout()
        self.LayoutRadioboton = QHBoxLayout()
        self.translated = ""
        self.LayoutGrid = QGridLayout()
        self.CentroGLayout = QVBoxLayout()
        self.indicador_conversor = "Google"
        self.diccionario_Google = GoogleTranslator().get_supported_languages(True)
        self.diccionario_verificar = self.diccionario_Google
        self.diccionario_voz_equipo={}
        self.diccionario_MyMemory = MyMemoryTranslator(source='acehnese', target='english').get_supported_languages(True)
        self.Configuaracion_ventana_principal()
        self.mostrar_mensaje_signal_inf.connect(self.mostrar_mensaje_dialogo_inf)
        self.mostrar_mensaje_signal.connect(self.mostrar_mensaje_dialogo_cr)
        self.Configuracion_Layouts()
        self.lista_textEdit = []
        self.lista_botones = []
        self.diccionario_traductores = {"Google": "Google_Chrome_icon.svg", "Mymemory": "Mymemory_Translator_icon.svg"}
        self.list_Radioboton = []
        self.Creacion_Botones()

        layoutV = QHBoxLayout()
        layoutV.addLayout(self.IzquierdaGLayout)
        layoutV.addLayout(self.CentroGLayout)
        layoutV.addLayout(self.DerechaGLayout)
        self.LayoutGrid.addLayout(layoutV, 2, 0)
        Componente_principal = Color_app("darkgreen")
        Componente_principal.setLayout(self.LayoutGrid)
        self.setCentralWidget(Componente_principal)

    def Configuracion_Layouts(self):

        self.DerechaGLayout.setContentsMargins(0, 0, 20, 20)
        self.IzquierdaGLayout.setContentsMargins(20, 0, 0, 20)
        self.CentroGLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.DerechaGLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.IzquierdaGLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.CentroGLayout.setContentsMargins(0, 0, 0, 0)
        self.CentroGLayout.setSpacing(15)

    def Click_radiobuton(self, boton):
        Qcombox_1_idioma_actual = self.Qcombox_1.currentText()
        Qcombox_2_idioma_actual = self.Qcombox_2.currentText()

        self.Qcombox_1.clear()
        self.Qcombox_2.clear()

        if boton == "Google":
            self.indicador_conversor = boton
            self.Qcombox_1.addItems(self.diccionario_Google)
            self.Qcombox_2.addItems(self.diccionario_Google)
            self.verificacion_idiomas(Qcombox_1_idioma_actual, Qcombox_2_idioma_actual, self.diccionario_Google)

        else:
            self.indicador_conversor = boton
            self.Qcombox_1.addItems(self.diccionario_MyMemory)
            self.Qcombox_2.addItems(self.diccionario_MyMemory)
            self.verificacion_idiomas(Qcombox_1_idioma_actual, Qcombox_2_idioma_actual, self.diccionario_MyMemory)


    def verificacion_idiomas(self, Qcombox_1_idioma, Qcombox_2_idioma, diccionario):
        lista_idiomas = list(diccionario)
        verificacion_1 = self.Qcombox_1.findText(Qcombox_1_idioma)
        verificacion_2 = self.Qcombox_2.findText(Qcombox_2_idioma)
        if verificacion_1 != -1:
            self.Qcombox_1.setCurrentIndex(verificacion_1)
        else:
            self.Qcombox_1.setCurrentText(random.choice(lista_idiomas))

        if verificacion_2 != -1:
            self.Qcombox_2.setCurrentIndex(verificacion_2)
        else:
            self.Qcombox_2.setCurrentText(random.choice(lista_idiomas))

    def Creacion_configuracion_QComBox(self):
        self.Qcombox_1 = QComboBox()
        self.Qcombox_1.setMaxVisibleItems(10)
        self.Qcombox_2 = QComboBox()
        self.Qcombox_2.setMaxVisibleItems(10)
        self.Qcombox_1.addItems(self.diccionario_Google)
        self.Qcombox_2.addItems(self.diccionario_Google)
        self.Qcombox_1.setCurrentText("spanish")
        self.Qcombox_2.setCurrentText("english")
        self.IzquierdaGLayout.addWidget(self.Qcombox_1)
        self.DerechaGLayout.addWidget(self.Qcombox_2)

    def creacion_radioboton(self):
        GrupoBotones = QButtonGroup(self)
        for Textboton, Iconoboton in self.diccionario_traductores.items():
            boton_Radio = QRadioButton(Textboton)
            self.Configuracion_botones(boton_Radio, Iconoboton, 15, 9, "none")
            self.list_Radioboton.append(boton_Radio)
            GrupoBotones.addButton(boton_Radio)
            self.LayoutRadioboton.addWidget(boton_Radio)

        self.LayoutGrid.addLayout(self.LayoutRadioboton, 1, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.LayoutGrid.setRowStretch(1, 0)
        self.LayoutGrid.setRowStretch(2, 0)
        self.LayoutGrid.setRowStretch(0, 0)
        self.list_Radioboton[0].setChecked(True)
        self.list_Radioboton[0].clicked.connect(lambda: self.Click_radiobuton("Google"))
        self.list_Radioboton[1].clicked.connect(lambda: self.Click_radiobuton("Mymemory"))

    def Creacion_Botones(self):
        self.creacion_radioboton()
        self.Creacion_configuracion_QComBox()
        self.Creacion_Configuracion_Editores_texto()
        for j in range(4):
            boton = QPushButton()
            self.lista_botones.append(boton)
        self.Configuracion_botones(self.lista_botones[0], "exchange_arrows_icon.svg", tamanoIcono=30)
        self.Configuracion_botones(self.lista_botones[1], "translate_icon.svg")
        self.Configuracion_botones(self.lista_botones[2], "sound_speaker_voice.svg", tamanoIcono=30, layout="derecha")
        self.Configuracion_botones(self.lista_botones[3], "sound_speaker_voice.svg", tamanoIcono=30, layout="izquierda")
        self.lista_botones[1].setText("Traducir")
        self.lista_botones[0].clicked.connect(self.Click_Cambiar_textoEdit)
        self.lista_botones[1].clicked.connect(self.Traducir_Idioma)
        self.lista_botones[2].clicked.connect(self.voz_Qcombox_objetivo)
        self.lista_botones[3].clicked.connect(self.voz_Qcombox_fuente)

    def voz_Qcombox_objetivo(self):
        _, objetivo = self.verificador_fuente_objetivo(self.diccionario_verificar)
        self.funcion_voz(self.lista_textEdit[1].toPlainText(),objetivo)

    def voz_Qcombox_fuente(self):
        fuente, _ = self.verificador_fuente_objetivo(self.diccionario_verificar)
        self.funcion_voz(self.lista_textEdit[0].toPlainText(),fuente)
    def Obtener_voz_equipo(self,engine):
        global voz
        if len(self.diccionario_voz_equipo)==0:
            voz = engine.getProperty('voices')
            for j in voz:
                self.diccionario_voz_equipo[j.languages[0].split("-")[0]]=j.languages[0]
        return set(self.diccionario_voz_equipo.keys()),voz

    def funcion_voz_hilo(self, texto,idioma):
        try:
            engine = pyttsx3.init()
            set_voz_equipo,voices=self.Obtener_voz_equipo(engine)
            if idioma in set_voz_equipo:
                idioma_detectado=self.diccionario_voz_equipo[idioma]
                for j in voices:
                    if j.languages[0]==idioma_detectado:
                        engine.setProperty('voice', j.id)
                engine.say(texto)
                engine.runAndWait()
                engine.stop()
                del engine
            else:
                engine.stop()
                del engine

                self.mostrar_mensaje_signal.emit("Idioma", f"No se encontro la voz del idioma selecionado\nlos idiomas disponibles son:\n{"\n".join(list(self.diccionario_voz_equipo.values())).strip()}")
        except Exception as e:
            self.mostrar_mensaje_signal.emit("Reproduccion de voz",f"Error en reproducción de voz: {e}")

    def funcion_voz(self, texto,idioma):
        if texto.strip():
            hilo_voz = threading.Thread(target=lambda:self.funcion_voz_hilo(texto,idioma))
            hilo_voz.daemon = True
            hilo_voz.start()

    def verificador_fuente_objetivo(self, diccionario):
        fuente = diccionario[self.Qcombox_1.currentText()]
        target = diccionario[self.Qcombox_2.currentText()]
        return fuente, target

    def Traducir_Idioma(self):
        try:
            if self.indicador_conversor == "Google":
                fuente, Target = self.verificador_fuente_objetivo(self.diccionario_Google)
                self.translated = GoogleTranslator(source=fuente, target=Target).translate(
                    self.lista_textEdit[0].toPlainText())
                self.lista_textEdit[1].setPlainText(self.translated)
            else:
                fuente, Target = self.verificador_fuente_objetivo(self.diccionario_MyMemory)
                self.translated = MyMemoryTranslator(source=fuente, target=Target).translate(
                    self.lista_textEdit[0].toPlainText())
                self.lista_textEdit[1].setPlainText(self.translated)
        except requests.ConnectionError:
            QMessageBox.critical(self,"Error Conexion" , "Error en la conexion por favor verifica tu conexion a internet")


    def Click_Cambiar_textoEdit(self):
        idioma_1 = self.Qcombox_1.currentText()
        idioma_2 = self.Qcombox_2.currentText()
        self.Qcombox_1.setCurrentText(idioma_2)
        self.Qcombox_2.setCurrentText(idioma_1)
        texto_1 = self.lista_textEdit[0].toPlainText()
        texto_2 = self.lista_textEdit[1].toPlainText()
        self.lista_textEdit[0].setPlainText(texto_2)
        self.lista_textEdit[1].setPlainText(texto_1)

    def Configuracion_botones(self, boton, icono_svg, tamanoIcono=26, tamanoText=10, layout="center"):
        boton.setIcon(QIcon(os.path.join(Basedir, "iconos", icono_svg)))
        boton.setIconSize(QSize(tamanoIcono, tamanoIcono))
        boton.setMaximumSize(100, 50)
        fon = boton.font()
        fon.setFamily("Times New Roman")
        fon.setBold(True)
        fon.setPointSize(tamanoText)
        boton.setFont(fon)
        boton.setContentsMargins(0, 0, 0, 0)
        if layout == "center":
            self.CentroGLayout.addWidget(boton)
        elif layout == "izquierda":
            self.IzquierdaGLayout.addWidget(boton)
        elif layout == "derecha":
            self.DerechaGLayout.addWidget(boton)

    def Creacion_Configuracion_Editores_texto(self):
        for textedit in range(2):
            TextEdi = QTextEdit()
            TextEdi.setMaximumSize(QSize(300, 200))
            TextEdi.setMinimumSize(QSize(280, 180))
            Font = TextEdi.font()
            Font.setPointSize(13)
            Font.setFamily("Times New Roman")
            TextEdi.setFont(Font)
            self.lista_textEdit.append(TextEdi)
        self.IzquierdaGLayout.addWidget(self.lista_textEdit[0])
        self.lista_textEdit[1].setPlaceholderText("Traducción")
        self.lista_textEdit[1].setReadOnly(True)
        self.DerechaGLayout.addWidget(self.lista_textEdit[1])

    def mostrar_mensaje_dialogo_inf(self, titulo, mensaje):

        QMessageBox.information(self, titulo, mensaje)

    def mostrar_mensaje_dialogo_cr(self, titulo, mensaje):

        QMessageBox.critical(self, titulo, mensaje)

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            self.pantalla_completa()
        super().changeEvent(event)

    def pantalla_completa(self):
        if self.isMaximized():
            self.lista_botones[0].setMaximumSize(QSize(500, 90))
            self.lista_botones[1].setMaximumSize(QSize(500, 90))
            self.icono_pantalla.setIconSize(QSize(150, 150))
            self.Configuracion_botones(self.lista_botones[0], "exchange_arrows_icon.svg", 40)
            self.Configuracion_botones(self.lista_botones[1], "translate_icon.svg", 30, 11)
            for textedit in self.lista_textEdit:
                textedit.setMaximumSize(QSize(600, 300))
        else:
            self.lista_botones[0].setMaximumSize(QSize(100, 50))
            self.lista_botones[1].setMaximumSize(QSize(100, 50))
            self.icono_pantalla.setIconSize(QSize(80, 80))
            self.Configuracion_botones(self.lista_botones[0], "exchange_arrows_icon.svg", tamanoIcono=30)
            self.Configuracion_botones(self.lista_botones[1], "translate_icon.svg")

            for textedit in self.lista_textEdit:
                textedit.setMaximumSize(QSize(300, 200))

    def Configuaracion_ventana_principal(self):

        self.setMinimumSize(QSize(800, 500))
        self.setWindowTitle("Traductor")
        self.setWindowIcon(QIcon(os.path.join(Basedir, "iconos", "translation_icon.svg")))
        self.Mostrar_etiqueta_traductor()
        self.Mostrar_icono_ventana_principal()


    def Mostrar_etiqueta_traductor(self):
        label = QLabel("Seleccioné un Traductor :".title())
        font = label.font()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        label.setFont(font)
        label.setContentsMargins(0, 0, 0, 0)
        self.LayoutRadioboton.addWidget(label, stretch=0)

    def Mostrar_icono_ventana_principal(self):
        self.icono_pantalla = QPushButton()
        self.icono_pantalla.setIcon(QIcon(os.path.join(Basedir, "iconos", "translation_icon.svg")))
        self.icono_pantalla.setIconSize(QSize(80, 80))
        self.icono_pantalla.setContentsMargins(0, 0, 0, 0)
        self.icono_pantalla.setFlat(True)
        self.icono_pantalla.setStyleSheet("""
                   QPushButton {
                       border: 12px solid white;
                       border-radius: 30px; 
                       background-color: white;
                       margin: 0px;    
                   }
               """)
        self.LayoutGrid.addWidget(self.icono_pantalla, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    traductor_app = Traductor_App()
    traductor_app.show()
    sys.exit(app.exec())