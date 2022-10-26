from PyQt5.QtCore import *
from gui_design import *
from PyQt5.QtGui import *
import pyqtgraph as pg

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        # Usamos la funcion QPoint() para guardar la posicion del mouse
        self.click_position = QPoint()
        # Se configura la ventana
        self.btn_normal.hide()
        self.btn_min.clicked.connect(lambda: self.showMinimized())
        self.btn_cerrar.clicked.connect(self.control_btn_cerrar)
        self.btn_normal.clicked.connect(self.control_btn_normal)
        self.btn_max.clicked.connect(self.control_btn_maximizar)
        self.btn_menu.clicked.connect(self.mover_menu)

        #Conexion botones
        self.btn_inicio.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_deteccion))
        self.btn_basedatos.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_base_datos))
        self.btn_ajustes.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_ajustes))

        # Se elimina la barra de titulo por default
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Size grip
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)

        # Movimiento de la ventana
        self.frame_superior.mouseMoveEvent = self.mover_ventana

        # Creacion de la grafica
        pg.setConfigOption('background', '#2c2c2c')
        pg.setConfigOption('foreground', '#ffffff')
        self.plt = pg.PlotWidget(title='')
        self.graph_main.addWidget(self.plt)

        self.show_indicator()
        #self.act_leds.setChecked(1)
        self.main_pump(1)
        self.mix_pump(0)
        self.water_pump(1)
        self.Leds(0)
        self.ph_pump_mas(1)
        self.ph_pump_menos(1)
        self.nut_pump(0)
        self.heater(0)

    def mover_menu(self):
        if True:
            width = self.frame_menu.width()
            normal = 0
            if width == 0:
                extender = 250
            else:
                extender = normal
            self.animacion = QPropertyAnimation(self.frame_menu, b'minimumWidth')
            self.animacion.setDuration(300)
            self.animacion.setStartValue(width)
            self.animacion.setEndValue(extender)
            self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animacion.start()

    def control_btn_cerrar(self):
        self.close()

    def control_btn_normal(self):
        self.showNormal()
        self.btn_normal.hide()
        self.btn_max.show()

    def control_btn_maximizar(self):
        self.showMaximized()
        self.btn_max.hide()
        self.btn_normal.show()

    def resizeEvent(self, event):
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)

    def mousePressEvent(self, event):
        self.click_posicion = event.globalPos()

    def mover_ventana(self, event):
        if self.isMaximized() == False:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.click_posicion)
                self.click_posicion = event.globalPos()
                event.accept()
        if event.globalPos().y() <= 5 or event.globalPos().x() <= 5:
            self.showMaximized()
            self.btn_max.hide()
            self.btn_normal.show()
        else:
            self.showNormal()
            self.btn_normal.hide()
            self.btn_max.show()

    # Aqui graficas variables
    #def graph(self):
        # print(x)
        # self.y = self.y[1:]
        # self.y.append(x)
        # self.plt.clear()
        # self.plt.plot(self.x, self.y, pen=pg.mkPen('#da0037', width=2))

    def show_indicator(self):
        # indicator(cantidad de color {0 - 1}, valor númerico {numero real})
        self.indicator_temp(0.5, 21)
        self.indicator_humedad(0.1, 80)
        self.indicator_luz(0.1, 90)
        self.indicator_ph(0.6, 5)
        self.indicator_conductividad(0.98, 1)
        self.indicator_lvl_agua(0.75, 20)
        self.indicator_t_agua(0.3, 30)
        self.indicator_lvl_ph_mas(0.26, 2)
        self.indicator_lvl_ph_menos(0.88, 13)
        self.indicator_lvl_nut(0.5, 50)
        #QTimer.SigleShot(20, self.show_indicator())

    def indicator_temp(self, val, num):
        # Indicador de temperatura
        estilo_temp =  """QFrame{
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(17, 17, 17, 255), 
        stop:{stop1} rgba(17, 17, 17, 255), 
        stop:{stop2} rgba(180, 10, 10, 255), stop:1 rgba(180, 10, 10, 255));
        }"""
        # Indicadores de 0 a 1
        # Stop1 es el valor al que se coloca el indicador
        self.val_temp.setText(str(num))
        stop1 = val
        stop2 = stop1+0.01
        Sstop1 = str(stop1)
        Sstop2 = str(stop2)
        nuevo_estilo = estilo_temp.replace('{stop1}', Sstop1).replace('{stop2}', Sstop2)
        self.ind_temp.setStyleSheet(nuevo_estilo)

    def indicator_humedad(self, val, num):
        # Indicador de humedad
        estilo_temp =  """QFrame{
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(17, 17, 17, 255), stop:{stop1} rgba(17, 17, 17, 255), stop:{stop2} rgba(0, 30, 255, 180), stop:1 rgba(0, 30, 180, 255));
        }"""
        # Indicadores de 0 a 1
        # Stop1 es el valor al que se coloca el indicador
        self.val_humedad.setText(str(num))
        stop1 = val
        stop2 = stop1+0.01
        Sstop1 = str(stop1)
        Sstop2 = str(stop2)
        nuevo_estilo = estilo_temp.replace('{stop1}', Sstop1).replace('{stop2}', Sstop2)
        self.ind_humedad.setStyleSheet(nuevo_estilo)

    def indicator_luz(self, val, num):
        # Indicador de humedad
        estilo_temp =  """QFrame{
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(17, 17, 17, 255), stop:{stop1} rgba(17, 17, 17, 255), stop:{stop2} rgba(150, 150, 0, 255), stop:1 rgba(150, 150, 0, 255));
        }"""
        # Indicadores de 0 a 1
        # Stop1 es el valor al que se coloca el indicador
        self.val_luz.setText(str(num))
        stop1 = val
        stop2 = stop1+0.01
        Sstop1 = str(stop1)
        Sstop2 = str(stop2)
        nuevo_estilo = estilo_temp.replace('{stop1}', Sstop1).replace('{stop2}', Sstop2)
        self.ind_luz.setStyleSheet(nuevo_estilo)

    def indicator_ph(self, val, num):
        # Indicador de temperatura
        estilo_temp =  """QFrame{
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(17, 17, 17, 255), stop:{stop1} rgba(17, 17, 17, 255), stop:{stop2} rgba(160, 0, 180, 255), stop:1 rgba(160, 0, 180, 255));
        }"""
        # Indicadores de 0 a 1
        # Stop1 es el valor al que se coloca el indicador
        self.val_ph.setText(str(num))
        stop1 = val
        stop2 = stop1+0.01
        Sstop1 = str(stop1)
        Sstop2 = str(stop2)
        nuevo_estilo = estilo_temp.replace('{stop1}', Sstop1).replace('{stop2}', Sstop2)
        self.ind_ph.setStyleSheet(nuevo_estilo)

    def indicator_conductividad(self, val, num):
        # Indicador de temperatura
        estilo_temp =  """QFrame{
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(17, 17, 17, 255), stop:{stop1} rgba(17, 17, 17, 255), stop:{stop2} rgba(2, 180, 190, 255), stop:1 rgba(2, 180, 190, 255));
        }"""
        # Indicadores de 0 a 1
        # Stop1 es el valor al que se coloca el indicador
        self.val_conductividad.setText(str(num))
        stop1 = val
        stop2 = stop1+0.01
        Sstop1 = str(stop1)
        Sstop2 = str(stop2)
        nuevo_estilo = estilo_temp.replace('{stop1}', Sstop1).replace('{stop2}', Sstop2)
        self.ind_conductividad.setStyleSheet(nuevo_estilo)

    def indicator_t_agua(self, val, num):
        # Indicador de temperatura
        estilo_temp =  """QFrame{
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(17, 17, 17, 255), stop:{stop1} rgba(17, 17, 17, 255), stop:{stop2} rgba(190, 0, 60, 255), stop:1 rgba(190, 0, 60, 255));
        }"""
        # Indicadores de 0 a 1
        # Stop1 es el valor al que se coloca el indicador
        self.val_t_agua.setText(str(num))
        stop1 = val
        stop2 = stop1+0.01
        Sstop1 = str(stop1)
        Sstop2 = str(stop2)
        nuevo_estilo = estilo_temp.replace('{stop1}', Sstop1).replace('{stop2}', Sstop2)
        self.ind_t_agua.setStyleSheet(nuevo_estilo)

    def indicator_lvl_agua(self, val, num):
        # Indicador de temperatura
        estilo_temp =  """QFrame{
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(17, 17, 17, 255), stop:{stop1} rgba(17, 17, 17, 255), stop:{stop2} rgba(0, 0, 255, 255), stop:1 rgba(0, 0, 255, 255));
        }"""
        # Indicadores de 0 a 1
        # Stop1 es el valor al que se coloca el indicador
        self.val_lvl_agua.setText(str(num))
        stop1 = val
        stop2 = stop1+0.01
        Sstop1 = str(stop1)
        Sstop2 = str(stop2)
        nuevo_estilo = estilo_temp.replace('{stop1}', Sstop1).replace('{stop2}', Sstop2)
        self.ind_lvl_agua.setStyleSheet(nuevo_estilo)

    def indicator_lvl_ph_mas(self, val, num):
        # Indicador de temperatura
        estilo_temp =  """QFrame{
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(17, 17, 17, 255), stop:{stop1} rgba(17, 17, 17, 255), stop:{stop2} rgba(17, 190, 0, 255), stop:1 rgba(17, 190, 0, 255));
        }"""
        # Indicadores de 0 a 1
        # Stop1 es el valor al que se coloca el indicador
        self.val_lvl_ph_mas.setText(str(num))
        stop1 = val
        stop2 = stop1+0.01
        Sstop1 = str(stop1)
        Sstop2 = str(stop2)
        nuevo_estilo = estilo_temp.replace('{stop1}', Sstop1).replace('{stop2}', Sstop2)
        self.ind_lvl_ph_mas.setStyleSheet(nuevo_estilo)

    def indicator_lvl_ph_menos(self, val, num):
        # Indicador de temperatura
        estilo_temp =  """QFrame{
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(17, 17, 17, 255), stop:{stop1} rgba(17, 17, 17, 255), stop:{stop2} rgba(190, 0, 170, 255), stop:1 rgba(190, 0, 170, 255));
        }"""
        # Indicadores de 0 a 1
        # Stop1 es el valor al que se coloca el indicador
        self.val_lvl_ph_menos.setText(str(num))
        stop1 = val
        stop2 = stop1+0.01
        Sstop1 = str(stop1)
        Sstop2 = str(stop2)
        nuevo_estilo = estilo_temp.replace('{stop1}', Sstop1).replace('{stop2}', Sstop2)
        self.ind_lvl_ph_menos.setStyleSheet(nuevo_estilo)

    def indicator_lvl_nut(self, val, num):
        # Indicador de temperatura
        estilo_temp =  """QFrame{
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(17, 17, 17, 255), stop:{stop1} rgba(17, 17, 17, 255), stop:{stop2} rgba(255, 0, 0, 255), stop:1 rgba(255, 0, 0, 255));
        }"""
        # Indicadores de 0 a 1
        # Stop1 es el valor al que se coloca el indicador
        self.val_lvl_nut.setText(str(num))
        stop1 = val
        stop2 = stop1+0.01
        Sstop1 = str(stop1)
        Sstop2 = str(stop2)
        nuevo_estilo = estilo_temp.replace('{stop1}', Sstop1).replace('{stop2}', Sstop2)
        self.ind_lvl_nut.setStyleSheet(nuevo_estilo)

    def main_pump(self, val):
        estilo_temp = """QFrame{
        background-color:{color};
        }"""
        rojo = "rgb(255, 0, 0);"
        verde = "rgb(0, 255, 0);"
        if val == True:
            nuevo_estilo = estilo_temp.replace('{color}', verde)
            self.act_main_pump.setStyleSheet(nuevo_estilo)
        else:
            nuevo_estilo = estilo_temp.replace('{color}', rojo)
            self.act_main_pump.setStyleSheet(nuevo_estilo)

    def Leds(self, val):
        estilo_temp = """QFrame{
        background-color:{color};
        }"""
        rojo = "rgb(255, 0, 0);"
        verde = "rgb(0, 255, 0);"
        if val == True:
            nuevo_estilo = estilo_temp.replace('{color}', verde)
            self.act_leds.setStyleSheet(nuevo_estilo)
        else:
            nuevo_estilo = estilo_temp.replace('{color}', rojo)
            self.act_leds.setStyleSheet(nuevo_estilo)

    def ph_pump_mas(self, val):
        estilo_temp = """QFrame{
        background-color:{color};
        }"""
        rojo = "rgb(255, 0, 0);"
        verde = "rgb(0, 255, 0);"
        if val == True:
            nuevo_estilo = estilo_temp.replace('{color}', verde)
            self.act_ph_mas_pump.setStyleSheet(nuevo_estilo)
        else:
            nuevo_estilo = estilo_temp.replace('{color}', rojo)
            self.act_ph_mas_pump.setStyleSheet(nuevo_estilo)

    def ph_pump_menos(self, val):
        estilo_temp = """QFrame{
        background-color:{color};
        }"""
        rojo = "rgb(255, 0, 0);"
        verde = "rgb(0, 255, 0);"
        if val == True:
            nuevo_estilo = estilo_temp.replace('{color}', verde)
            self.act_ph_menos_pump.setStyleSheet(nuevo_estilo)
        else:
            nuevo_estilo = estilo_temp.replace('{color}', rojo)
            self.act_ph_menos_pump.setStyleSheet(nuevo_estilo)

    def nut_pump(self, val):
        estilo_temp = """QFrame{
        background-color:{color};
        }"""
        rojo = "rgb(255, 0, 0);"
        verde = "rgb(0, 255, 0);"
        if val == True:
            nuevo_estilo = estilo_temp.replace('{color}', verde)
            self.act_nut_pump.setStyleSheet(nuevo_estilo)
        else:
            nuevo_estilo = estilo_temp.replace('{color}', rojo)
            self.act_nut_pump.setStyleSheet(nuevo_estilo)

    def heater(self, val):
        estilo_temp = """QFrame{
        background-color:{color};
        }"""
        rojo = "rgb(255, 0, 0);"
        verde = "rgb(0, 255, 0);"
        if val == True:
            nuevo_estilo = estilo_temp.replace('{color}', verde)
            self.act_heater.setStyleSheet(nuevo_estilo)
        else:
            nuevo_estilo = estilo_temp.replace('{color}', rojo)
            self.act_heater.setStyleSheet(nuevo_estilo)

    def water_pump(self, val):
        estilo_temp = """QFrame{
        background-color:{color};
        }"""
        rojo = "rgb(255, 0, 0);"
        verde = "rgb(0, 255, 0);"
        if val == True:
            nuevo_estilo = estilo_temp.replace('{color}', verde)
            self.act_water_pump.setStyleSheet(nuevo_estilo)
        else:
            nuevo_estilo = estilo_temp.replace('{color}', rojo)
            self.act_water_pump.setStyleSheet(nuevo_estilo)

    def mix_pump(self, val):
        estilo_temp = """QFrame{
        background-color:{color};
        }"""
        rojo = "rgb(255, 0, 0);"
        verde = "rgb(0, 255, 0);"
        if val == True:
            nuevo_estilo = estilo_temp.replace('{color}', verde)
            self.act_mix_pump.setStyleSheet(nuevo_estilo)
        else:
            nuevo_estilo = estilo_temp.replace('{color}', rojo)
            self.act_mix_pump.setStyleSheet(nuevo_estilo)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MyApp()
    window.show()
    app.exec_()