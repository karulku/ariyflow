from PySide6.QtCore import QThread
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer
import pymysql
import matplotlib.pyplot as plt

class matThread(QWidget):
    def __init__(self, par):
        self.par = par
        
    def show(self):
        cur = self.par.cur
        
        def get_data():
            cur.execute("""
                SELECT * FROM (
                    SELECT * FROM step_msg ORDER BY date DESC LIMIT 100
                ) AS t ORDER BY date ASC;
            """)
            datas = cur.fetchall()
            tem = [r[1] for r in datas]
            light = [r[2] for r in datas]
            return tem, light

        
        
        data = get_data()
        plt.xlabel("counter")
        plt.ylabel("value")
        plt.plot(data[0], label = "temperature")
        plt.plot(data[1], label = "light")
        plt.legend()
        plt.show()