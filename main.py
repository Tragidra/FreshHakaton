import requests
import xml.etree.ElementTree as ET
import re
class GetCourses(object):

    def __init__(self):
        self.run()

    def run(self):
        print('Добрый день, вас приветсвует консольная программа для получения котировок различных валют от ЦБ РФ. ')
        while True:
            date = self.get_date_from_user()
            uniq_code, valute_name, iso = self.get_uniq_code_with_valute_name()
            url_params = {'date_req1': date, 'date_req2': date, 'VAL_NM_RQ': uniq_code}
            try:
                r = requests.get('http://www.cbr.ru/scripts/XML_dynamic.asp', params=url_params)
                root = ET.fromstring(r.text)
            except:
                print('В ходе работы программы произошёл сбой, возможно, API Центрального Банка Российской Федерации'
                      'на данный момент недоступен. Пожалуйста, попробуйте позже.')
                break
            try:
                valute_value = root.find(".//Value").text
                print(iso + ' (' + valute_name + ')' + ' : ' + valute_value)
            except:
                print('Данные о курсе выбранной вами валюты в указанную дату не найдены.')
            print(
                'Если вы хотите завершить работу программы, то введите слово Стоп. Если же вы хотите получить другие котировки,'
                'то оставьте поле ввода пустым и нажмите Enter или же введите любую другую комбинацию.')
            a = input()
            if a == 'Стоп':
                break
            else:
                continue
    def getCodeWithISO(self, uniq_code):
        response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        data = response.json()
        for currency_code, currency_info in data["Valute"].items():
            if currency_info["CharCode"] == uniq_code:
                return currency_info["ID"], currency_info['Name']
        return 0

    def get_date_from_user(self):
        while True:
            print(
                'Пожалуйста, введите дату, на которую вы хотите получить курсы валют. Дата должно иметь вид YYYY-MM-DD, например, 2023-07-22 - '
                'это 22-ое июля 2023-ого года. Введите дату:')
            input_date = input()
            correct_date = r'^\d{4}-\d{2}-\d{2}$'
            if re.match(correct_date, input_date):
                break
            else:
                print('Введённая вами дата имеет некорректный формат. Пожалуйста, перепроверьте её и введите ещё раз:')
        year, month, day = input_date.split('-')
        date = f"{day}/{month}/{year}"
        return date

    def get_uniq_code_with_valute_name(self):
        while True:
            print(
                'Пожалуйста, введите код нужной вам валюты в формате ISO 4217. Код валюты имеет вид набора символов, например, уникальный '
                'код доллара США - USD. Введите код:')
            try:
                iso = input()
                uniq_code, valute_name = self.getCodeWithISO(iso)
                break
            except:
                print(
                    'Введённый вами код валюты не соответствует ни одной известной мировой валюте. Пожалуйста, перепроверьте код и'
                    'попробуйте ввести его ещё раз:')
        return uniq_code, valute_name, iso

GetCourses = GetCourses()
