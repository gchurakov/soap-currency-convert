from flask import Flask, request, render_template
from zeep import Client
from zeep.transports import Transport
from datetime import datetime
import requests

app = Flask(__name__)


@app.route('/')
def index():
    # Fetch the list of available currencies
    currencies_url = 'https://www.cbr.ru/scripts/XML_val.asp?d=0'
    response = requests.get(currencies_url)

    # Extract currency codes and names from the response
    currencies = {}
    xml_data = response.text
    start = xml_data.find('<Item ID="R01235">')
    end = xml_data.find('</ValCurs>')
    xml_data = xml_data[start:end]

    while '<Item' in xml_data:
        code_start = xml_data.find('ID="') + 4
        code_end = xml_data.find('">', code_start)
        code = xml_data[code_start:code_end]

        name_start = xml_data.find('<Name>') + 6
        name_end = xml_data.find('</Name>', name_start)
        name = xml_data[name_start:name_end]

        currencies[code] = name
        xml_data = xml_data[name_end:]

    return render_template('index.html', currencies=currencies)


@app.route('/convert', methods=['POST'])
def convert():
    wsdl_url = 'https://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL'
    client = Client(wsdl_url)

    amount = float(request.form['amount'])
    source_currency = request.form['source_currency']
    target_currency = request.form['target_currency']

    result = client.service.GetCursOnDate(
        on_date='2023-06-20',
        valuta_code=source_currency + target_currency
    )

    exchange_rate_source = float(result.GetCursOnDateResult.VizicCurs.ValuteCursOnDate[0].Vcurs)
    exchange_rate_target = float(result.GetCursOnDateResult.VizicCurs.ValuteCursOnDate[1].Vcurs)

    converted_amount = (amount / exchange_rate_source) * exchange_rate_target

    return render_template('result.html', amount=amount, source_currency=source_currency,
                           target_currency=target_currency, converted_amount=converted_amount)


if __name__ == '__main__':
    app.run(debug=True)
