import sys
import json

from PyQt5 import QtCore, QtWidgets, QtNetwork
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.initUI()
        self.loadStats()
        self.loadTestResults()

    def updateStatsTable(self, response):
        er = response.error()
        if er == QtNetwork.QNetworkReply.NoError:
            data = json.loads(str(response.readAll(), 'utf-8'))
            self.stats_table.setRowCount(len(data))
            for row_id, row_data in enumerate(data):
                for cell_id, cell_data in enumerate(row_data.values()):
                    self.stats_table.setItem(row_id, cell_id, QtWidgets.QTableWidgetItem(str(cell_data)))
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText(str(er))
            msg.exec()

    def loadStats(self):
        url = "http://127.0.0.1:8000/api_v1/stat"
        request = QtNetwork.QNetworkRequest(QtCore.QUrl(url))

        self.stats_nam = QtNetwork.QNetworkAccessManager()
        self.stats_nam.finished.connect(self.updateStatsTable)
        self.stats_nam.get(request)
        print('stats loaded')

    def updateTestResultsTable(self, response):
        er = response.error()
        if er == QtNetwork.QNetworkReply.NoError:
            data = json.loads(str(response.readAll(), 'utf-8'))
            self.test_results_table.setRowCount(len(data))
            for row_id, row_data in enumerate(data):
                for cell_id, cell_data in enumerate(row_data.values()):
                    self.test_results_table.setItem(row_id, cell_id, QtWidgets.QTableWidgetItem(str(cell_data)))
            print('results updated')
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText(str(er))
            msg.exec()

    def deleteTestResult(self, db_id):
        url = f"http://127.0.0.1:8000/api_v1/test_result/{db_id}"
        request = QtNetwork.QNetworkRequest(QtCore.QUrl(url))

        self.delete_nam = QtNetwork.QNetworkAccessManager()
        self.delete_nam.finished.connect(self.deleteTestResultFinished)
        self.delete_nam.deleteResource(request)

    def deleteTestResultFinished(self, response):
        er = response.error()
        if er == QtNetwork.QNetworkReply.NoError:
            self.loadTestResults()
            self.loadStats()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText(str(er))
            msg.exec()

    def loadTestResults(self):
        url = "http://127.0.0.1:8000/api_v1/test_results"
        request = QtNetwork.QNetworkRequest(QtCore.QUrl(url))

        self.results_nam = QtNetwork.QNetworkAccessManager()
        self.results_nam.finished.connect(self.updateTestResultsTable)
        self.results_nam.get(request)
        print('results loaded')

    def addTestResult(self):
        url = f"http://127.0.0.1:8000/api_v1/test_result"
        request = QtNetwork.QNetworkRequest(
            QtCore.QUrl(url)
        )

        self.delete_nam = QtNetwork.QNetworkAccessManager()
        self.delete_nam.finished.connect(self.addTestResultFinished)
        self.delete_nam.post(request, bytes(json.dumps({
                "device_type": "Motion Cam",
                "time": "2020-05-10 01:59:34",
                "operator": "Jack",
                "success": True
            }), encoding='utf-8'))

    def addTestResultFinished(self, response):
        er = response.error()
        if er == QtNetwork.QNetworkReply.NoError:
            self.loadTestResults()
            self.loadStats()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText(str(er))
            msg.exec()



    def initUI(self):
        self.setGeometry(200, 200, 500, 800)
        self.setWindowTitle("Ajax Device Tests")

        # TABLE WITH TEST RESULTS
        self.test_results_table = QtWidgets.QTableWidget(self)
        self.test_results_table.move(0, 60)
        self.test_results_table.setColumnCount(5)
        self.test_results_table.setHorizontalHeaderLabels(
            ["id", "Тип Датчика", "Оператор", "Час", "Результат"]
        )
        self.test_results_table.setMinimumSize(400, 400)

        # TABLE WITH STATS
        self.stats_table = QtWidgets.QTableWidget(self)
        self.stats_table.move(0, 460)
        self.stats_table.setColumnCount(4)
        self.stats_table.setHorizontalHeaderLabels(
            ["Тип Датчика", "Всього тестів", "Успішних тестів", "Неуспішних тестів"]
        )
        self.stats_table.setMinimumSize(400, 400)

        # ADD NEW TEST RESULT
        self.label = QtWidgets.QLabel("add default row")
        self.label.setText("add default row")

        self.add_button = QtWidgets.QPushButton(self)
        self.add_button.move(300, 0)
        self.add_button.setText("Add")
        self.add_button.clicked.connect(self.addTestResult)

        # DELETE TEST RESULT PART
        self.delete_button = QtWidgets.QPushButton(self)
        self.delete_button.setText("Delete")
        self.delete_button.move(0, 30)
        self.delete_button.clicked.connect(self.delete)


    # def add_record(self):
    #     self.test_results_table.insertRow(0)

    def delete(self):
        selected = self.test_results_table.selectedItems()[0]
        db_id = selected.text()
        self.deleteTestResult(db_id)


def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    window()
