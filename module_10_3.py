# Блокировки и обработка ошибок
import threading, random, time
from time import sleep


class Bank:
    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()

    def deposit(self):
        for i in range(100):
            current_deposit = random.randint(50, 500)
            self.balance += current_deposit
            print(f'Пополнение: {current_deposit}. Баланс: {self.balance}')
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
            sleep(.001)

    def take(self):
        for i in range(100):
            current_take = random.randint(50, 500)
            print(f'Запрос на {current_take}')
            if current_take <= self.balance:
                self.balance -= current_take
                print(f'Снятие: {current_take}. Баланс: {self.balance}')
            else:
                print('Запрос отклонён, недостаточно средств')
                self.lock.acquire()
            sleep(.001)



bk = Bank()

th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')