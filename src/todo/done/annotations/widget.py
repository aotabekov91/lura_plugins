from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice

class PieChart(QChart):

    def create_piechart(self):

        series = QPieSeries()
        series.append("Python", 80)
        series.append("C++", 70)
        series.append("Java", 50)
        series.append("C#", 40)
        series.append("PHP", 30)

        #adding slice
        slice = QPieSlice()
        slice = series.slices()[2]
        slice.setExploded(True)
        slice.setLabelVisible(True)
        slice.setPen(QPen(Qt.darkGreen, 2))
        slice.setBrush(Qt.green)

        self.setup(series)

    def setup(self, series=None):

        self.legend().hide()
        if series: self.addSeries(series)
        self.createDefaultAxes()
        self.setAnimationOptions(QChart.SeriesAnimations)

        self.legend().setVisible(False)
        self.legend().setAlignment(Qt.AlignBottom)

        selfview = QChartView(self)
        selfview.setRenderHint(QPainter.Antialiasing)
