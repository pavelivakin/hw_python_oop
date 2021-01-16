import datetime as dt

class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date == None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()

class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = [] #Empty list for new records
    def add_record(self, Record): #Save new record
        self.records.append(Record)
    def get_today_stats(self): #Calculate how much money/calories spent today
        today_count = 0
        for today in self.records:
            if today.date == dt.date.today():
                today_count += today.amount
        return f'Сегодня потрачено: {today_count}'
    def get_week_stats(self): #Stats money/calories for 7 days
        week_count = 0
        seven_days_ago = dt.date.today() - dt.timedelta(days=7)
        for week in self.records:
            if week.date >= seven_days_ago:
                week_count += week.amount
        return f'За неделю потрачено: {week_count}'

class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        calories_today = 0
        calories_left = 0
        for r in self.records:
            if r.date == dt.date.today():
                calories_today += r.amount
        calories_left = self.limit - calories_today
        if calories_today < self.limit:
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей' 
                    'калорийностью не более {calories_left} кКал')
        else:
            return 'Хватит есть!'

class CashCalculator(Calculator):
    def get_today_cash_remained(self, currency):
        USD_RATE = 73.55
        EUR_RATE = 89.25
        self.currency = currency
        cash_today = 0.00
        cash_left = 0.00
        code_currency = ''
        if self.currency == 'usd':
            for i in self.records:
                if i.date == dt.date.today():
                    cash_today += i.amount
            cash_left = round((self.limit - cash_today)/USD_RATE,2)
            code_currency = 'USD'
        elif self.currency == 'eur':
            for i in self.records:
                if i.date == dt.date.today():
                    cash_today += i.amount
            cash_left = round((self.limit - cash_today)/EUR_RATE,2)
            code_currency = 'Euro'
        elif self.currency == 'rub':
            for i in self.records:
                if i.date == dt.date.today():
                    cash_today += i.amount
            cash_left = round(self.limit - cash_today,2)
            code_currency = 'руб.'
        else:
            return 'Неизвестный тип валюты. Выбери rub/usd/eur.'
        if cash_left > 0:
            return f'На сегодня осталось {cash_left} {code_currency}'
        elif cash_left == 0:
            return 'Денег нет, держись'
        else:
            return f'Денег нет, держись: твой долг - {cash_left} {code_currency}'

# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(1000)
        
# дата в параметрах не указана, 
# так что по умолчанию к записи должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment="кофе")) 
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др", date="08.11.2020"))
cash_calculator.add_record(Record(amount=52, comment="общественный транспорт", date="09.01.2021"))
cash_calculator.add_record(Record(amount=436, comment="телефон", date="10.01.2021"))
cash_calculator.add_record(Record(amount=3600, comment="кредит", date="11.01.2021"))
cash_calculator.add_record(Record(amount=100, comment="вафельки", date="12.01.2021"))
cash_calculator.add_record(Record(amount=350, comment="кофе в зерне", date="13.01.2021"))
cash_calculator.add_record(Record(amount=160, comment="такси", date="14.01.2021"))
                
print(cash_calculator.get_today_cash_remained("rub"))
# должно напечататься
# На сегодня осталось 555 руб