import threading
from datetime import datetime
from time import sleep

import requests
from PyQt5 import QtWidgets
from clientui import Ui_MainWindow


class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.send)
        threading.Thread(target=self.refresh).start()

    def send(self):
        text = self.lineEdit.text()
        username = self.lineEdit_2.text()
        password = self.lineEdit_3.text()
        try:
            response = requests.post('http://127.0.0.1:5000/login', json={
                'username': username,
                'password': password
            })
            print(response.text)
            response = requests.post('http://127.0.0.1:5000/send', json={
                'username': username,
                'password': password,
                'text': text
            })
            print(response.text)
        except requests.exceptions.ConnectionError:
            print('Server is not online')
            return
        except:
            print('Unknown error')
            return

        self.lineEdit.setText('')
        self.lineEdit.repaint()

    def refresh(self):
        last_time = 0

        while True:
            try:
                response = requests.get('http://127.0.0.1:5000/messages', params={'after': last_time})
            except:
                print('Error')
                sleep(1)
                continue

            for message in response.json()['messages']:
                formatted_time = datetime.fromtimestamp(message['time'])
                formatted_time = formatted_time.strftime('%H:%M:%S %Y-%m-%d')
                header = message['username'] + ' at ' + formatted_time
                text = message['text']
                self.textBrowser.append(header)
                self.textBrowser.append(text)
                self.textBrowser.append('')

                last_time = message['time']
            sleep(1)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = ExampleApp()
    window.show()
    app.exec_()
