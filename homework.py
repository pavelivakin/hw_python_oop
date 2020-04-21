import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record): 
        self.records.append(record)

    def get_today_stats(self):
        today = dt.datetime.now().date()
        sum_amount = 0
        for record in self.records:
            if record.date == today:
                sum_amount += record.amount
        return sum_amount

    def get_week_stats(self):
        today = dt.datetime.now().date()
        one_week_ago = today - dt.timedelta(days=7)
        sum_amount = 0
        for record in self.records:
            if one_week_ago <= record.date <= today:
                sum_amount += record.amount
        return sum_amount


class CashCalculator(Calculator):
    EURO_RATE = float(85)
    USD_RATE = float(75)
    
    def convert_table(self, currency):
        _convert_table = {
        'rub': (1.0, 'руб'),
        'руб': (1.0, 'руб'),
        'eur': (self.EURO_RATE, 'Euro'),
        'usd': (self.USD_RATE, 'USD'),
        }
        return _convert_table[currency]

    def get_today_cash_remained(self, currency):
        currency_rate, currency_name = self.convert_table(currency)
        currency_name = self.convert_table(currency)[1]
        cash_balance = self.limit - self.get_today_stats()
        cash_balance_converted = round(cash_balance / currency_rate, 2)
        if cash_balance_converted == 0:
            return  "Денег нет, держись"
        elif cash_balance_converted < 0:
            return  f"Денег нет, держись: твой долг - {abs(cash_balance_converted)} {currency_name}"   
        else:
            cash_balance_converted <= self.limit
            return f"На сегодня осталось {cash_balance_converted} {currency_name}"


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        cal_balance = self.limit - self.get_today_stats()
        if cal_balance > 0:
            return f"Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {cal_balance} кКал"
        else: 
            cal_balance <= 0
            return "Хватит есть!"


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if not date:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, "%d.%m.%Y").date()


# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(1000)

# для CashCalculator
r1 = Record(amount=145, comment="Безудержный кутеж", date="08.03.2019")
r2 = Record(amount=1568, comment="Наполнение потребительской корзины", date="09.03.2019")
r3 = Record(amount=691, comment="Катание на такси", date="08.03.2019")

# для CaloriesCalculator
r4 = Record(amount=1186, comment="Кусок тортика. И ещё один.", date="24.02.2019")
r5 = Record(amount=84, comment="Йогурт.", date="23.02.2019")
r6 = Record(amount=1140, comment="Баночка чипсов.", date="24.02.2019")

calc = Calculator(1000)
calc.add_record(r1)
print(calc.get_today_stats())

# пытался дать многострочный комментарий при комите, судя по всему не получилось
