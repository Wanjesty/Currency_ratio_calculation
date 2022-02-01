import requests
from lxml import objectify

url = 'http://www.cbr.ru/scripts/XML_daily.asp'

def get_request(url): #Получение контента с заданной страницы
    response = requests.request("GET", url)
    return response.content


def str_to_float(value): #Перевод строчного значения в значение с плавающей запятой
    new_value = ""
    for char in value:
        if char == ",":
            new_value += "."
        else:
            new_value += char
    return float(new_value)


def parseXML(xml, first_currency, second_currency): #Парсинг XML и запись нужных валют в словарь
    valutes = {}
    root = objectify.fromstring(xml)
    needed_valute = ""
    for appt in root.getchildren():
        if appt.tag == "Valute":
            for e in appt.getchildren():
                if e.tag == "Name":
                    needed_valute = ""
                    if e.text == first_currency or e.text == second_currency:
                        needed_valute = e.text
                if e.tag == "Value" and needed_valute:
                    valutes[needed_valute] = str_to_float(str(e.text))
    return valutes


def currency_ratio_calculation(first_currency, second_currency): #Получение значения отношения валют друг к другу
    current_valutes = parseXML(get_request(url), first_currency=first_currency, second_currency=second_currency)
    rate = 1 / current_valutes[first_currency] * current_valutes[second_currency]
    return rate


print(currency_ratio_calculation(first_currency="Венгерских форинтов", second_currency="Норвежских крон"))


"""current_valutes = parseXML(get_request(url)) #Получение словаря с нужными валютами
rate = 1 / current_valutes["Венгерских форинтов"] * current_valutes["Норвежских крон"] #Определение отношения валют друг к другу
print(rate)"""