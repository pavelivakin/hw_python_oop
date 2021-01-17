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
        return today_count
    def get_week_stats(self): #Stats money/calories for 7 days
        week_count = 0
        seven_days_ago = dt.date.today() - dt.timedelta(days=7)
        for week in self.records:
            if week.date >= seven_days_ago:
                week_count += week.amount
        return week_count

class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)
    def get_calories_remained(self):
        calories_left = 0
        if self.get_today_stats() < self.limit:
            calories_left = self.limit - self.get_today_stats()
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей ' 
                    f'калорийностью не более {calories_left} кКал')
        else:
            return 'Хватит есть!'

class CashCalculator(Calculator):
    USD_RATE = 73.55
    EURO_RATE = 89.25
    RUB_RATE = 1.00
    def __init__(self, limit):
        super().__init__(limit)
    def get_today_cash_remained(self, currency):
        self.currency = currency
        currencies = {
            'eur' : ('Euro' , self.EURO_RATE),
            'usd' : ('USD' , self.USD_RATE),
            'rub' : ('руб' , self.RUB_RATE)
        }
        currency_name = currencies[currency][0]
        currency_rate = currencies[currency][1]
        remained_cash = self.limit - self.get_today_stats()
        remained_cash_in_currency = round(remained_cash / currency_rate, 2)
        if remained_cash > 0:
            return f'На сегодня осталось {remained_cash_in_currency} {currency_name}'
        elif remained_cash == 0:
            return f'Денег нет, держись'
        else:
            remained_cash_in_currency = -remained_cash_in_currency
            return f'Денег нет, держись: твой долг - {remained_cash_in_currency} {currency_name}'

# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(1000)
        
# дата в параметрах не указана, 
# так что по умолчанию к записи должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment="кофе")) 
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др", date="08.11.2020"))
                
print(cash_calculator.get_today_cash_remained("rub"))
# должно напечататься
# На сегодня осталось 555 руб

calories_calculator = CaloriesCalculator(2000)
calories_calculator.add_record(Record(amount=250, comment="пончик"))
calories_calculator.add_record(Record(amount=870, comment="пицца"))
print(calories_calculator.get_calories_remained())