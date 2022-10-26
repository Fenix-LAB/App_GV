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
        self.indicator_temp(0.5)
        self.indicator_humedad(0.7)
        self.indicator_luz(0.1)
        self.indicator_ph(0.6)
        self.indicator_conductividad(0.98)
        self.indicator_lvl_agua(0.75)
        self.indicator_t_agua(0.3)
        self.indicator_lvl_ph_mas(0.26)
        self.indicator_lvl_ph_menos(0.88)
        self.indicator_lvl_nut(0.5)
        #QTimer.SigleShot(20, self.show_indicator())

    def indicator_temp(self, val):
        # Indicador de temperatura
        estilo_temp =  """QFrame{
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(17, 17, 17, 255), 
        stop:{stop1} rgba(17, 17, 17, 255), 
        stop:{stop2} rgba(180, 10, 10, 255), stop:1 rgba(180, 10, 10, 255));
        }"""
        # Indicadores de 0 a 1
        # Stop1 es el valor al que se coloca el indicador
        stop1 = val
        stop2 = stop1+0.01
        Sstop1 = str(stop1)
        Sstop2 = str(stop2)
        nuevo_estilo = estilo_temp.replace('{stop1}', Sstop1).replace('{stop2}', Sstop2)
        self.ind_temp.setStyleSheet(nuevo_estilo)

    def indicator_humedad(self, val):
        # Indicador de humedad
        estilo_temp =  """QFrame{
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(17, 17, 17, 255), stop:{stop1} rgba(17, 17, 17, 255), stop:{stop2} rgba(0, 30, 255, 180), stop:1 rgba(0, 30, 180, 255));
        }"""
        # Indicadores de 0 a 1
        # Stop1 es el valor al que se coloca el indicador
        stop1 = val
        stop2 = stop1+0.01
        Sstop1 = str(stop1)
        Sstop2 = str(stop2)
        nuevo_estilo = estilo_temp.replace('{stop1}', Sstop1).replace('{stop2}', Sstop2)
        self.ind_humedad.setStyleSheet(nuevo_estilo)

    def indicator_luz(self, val):
        # Indicador de humedad
        estilo_temp =  """QFrame{
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(17, 17, 17, 255), stop:{stop1} rgba(17, 17, 17, 255), stop:{stop2} rgba(150, 150, 0, 255), stop:1 rgba(150, 150, 0, 255));
        }"""
        # Indicadores de 0 a 1
        # Stop1 es el valor al que se coloca el indicador
        stop1 = val
        stop2 = stop1+0.01
        Sstop1 = str(stop1)
        Sstop2 = str(stop2)
        nuevo_estilo = estilo_temp.replace('{stop1}', Sstop1).replace('{stop2}', Sstop2)
        self.ind_luz.setStyleSheet(nuevo_estilo)

    def indicator_ph(self, val):
        # Indicador de temperatura
        estilo_temp =  """QFrame{
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(17, 17, 17, 255), stop:{stop1} rgba(17, 17, 17, 255), stop:{stop2} rgba(160, 0, 180, 255), stop:1 rgba(160, 0, 180, 255));
        }"""
        # Indicadores de 0 a 1
        # Stop1 es el valor al que se coloca el indicador
        stop1 = val
        stop2 = stop1+0.01
        Sstop1 = str(stop1)
        Sstop2 = str(stop2)
        nuevo_estilo = estilo_temp.replace('{stop1}', Sstop1).replace('{stop2}', Sstop2)
        self.ind_ph.setStyleSheet(nuevo_estilo)

    def indicator_conductividad(self, val):
        # Indicador de temperatura
        estilo_temp =  """QFrame{
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(17, 17, 17, 255), stop:{stop1} rgba(17, 17, 17, 255), stop:{stop2} rgba(2, 180, 190, 255), stop:1 rgba(2, 180, 190, 255));
        }"""
        # Indicadores de 0 a 1
        # Stop1 es el valor al que se coloca el indicador
        stop1 = val
        stop2 = stop1+0.01
        Sstop1 = str(stop1)
        Sstop2 = str(stop2)
        nuevo_estilo = estilo_temp.replace('{stop1}', Sstop1).replace('{stop2}', Sstop2)
        self.ind_conductividad.setStyleSheet(nuevo_estilo)

    def indicator_t_agua(self, val):
        # Indicador de temperatura
        estilo_temp =  """QFrame{
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(17, 17, 17, 255), stop:{stop1} rgba(17, 17, 17, 255), stop:{stop2} rgba(190, 0, 60, 255), stop:1 rgba(190, 0, 60, 255));
        }"""
        # Indicadores de 0 a 1
        # Stop1 es el valor al que se coloca el indicador
        stop1 = val
        stop2 = stop1+0.01
        Sstop1 = str(stop1)
        Sstop2 = str(stop2)
        nuevo_estilo = estilo_temp.replace('{stop1}', Sstop1).replace('{stop2}', Sstop2)
        self.ind_t_agua.setStyleSheet(nuevo_estilo)

    def indicator_lvl_agua(self, val):
        # Indicador de temperatura
        estilo_temp =  """QFrame{
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(17, 17, 17, 255), stop:{stop1} rgba(17, 17, 17, 255), stop:{stop2} rgba(0, 0, 255, 255), stop:1 rgba(0, 0, 255, 255));
        }"""
        # Indicadores de 0 a 1
        # Stop1 es el valor al que se coloca el indicador
        stop1 = val
        stop2 = stop1+0.01
        Sstop1 = str(stop1)
        Sstop2 = str(stop2)
        nuevo_estilo = estilo_temp.replace('{stop1}', Sstop1).replace('{stop2}', Sstop2)
        self.ind_lvl_agua.setStyleSheet(nuevo_estilo)

    def indicator_lvl_ph_mas(self, val):
        # Indicador de temperatura
        estilo_temp =  """QFrame{
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(17, 17, 17, 255), stop:{stop1} rgba(17, 17, 17, 255), stop:{stop2} rgba(17, 190, 0, 255), stop:1 rgba(17, 190, 0, 255));
        }"""
        # Indicadores de 0 a 1
        # Stop1 es el valor al que se coloca el indicador
        stop1 = val
        stop2 = stop1+0.01
        Sstop1 = str(stop1)
        Sstop2 = str(stop2)
        nuevo_estilo = estilo_temp.replace('{stop1}', Sstop1).replace('{stop2}', Sstop2)
        self.ind_lvl_ph_mas.setStyleSheet(nuevo_estilo)

    def indicator_lvl_ph_menos(self, val):
        # Indicador de temperatura
        estilo_temp =  """QFrame{
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(17, 17, 17, 255), stop:{stop1} rgba(17, 17, 17, 255), stop:{stop2} rgba(190, 0, 170, 255), stop:1 rgba(190, 0, 170, 255));
        }"""
        # Indicadores de 0 a 1
        # Stop1 es el valor al que se coloca el indicador
        stop1 = val
        stop2 = stop1+0.01
        Sstop1 = str(stop1)
        Sstop2 = str(stop2)
        nuevo_estilo = estilo_temp.replace('{stop1}', Sstop1).replace('{stop2}', Sstop2)
        self.ind_lvl_ph_menos.setStyleSheet(nuevo_estilo)

    def indicator_lvl_nut(self, val):
        # Indicador de temperatura
        estilo_temp =  """QFrame{
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(17, 17, 17, 255), stop:{stop1} rgba(17, 17, 17, 255), stop:{stop2} rgba(255, 0, 0, 255), stop:1 rgba(255, 0, 0, 255));
        }"""
        # Indicadores de 0 a 1
        # Stop1 es el valor al que se coloca el indicador
        stop1 = val
        stop2 = stop1+0.01
        Sstop1 = str(stop1)
        Sstop2 = str(stop2)
        nuevo_estilo = estilo_temp.replace('{stop1}', Sstop1).replace('{stop2}', Sstop2)
        self.ind_lvl_nut.setStyleSheet(nuevo_estilo)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MyApp()
    window.show()
    app.exec_()