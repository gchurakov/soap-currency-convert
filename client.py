from zeep import Client

wsdl_url = 'http://127.0.0.1:5000/?wsdl'
client = Client(wsdl_url)

# Define input parameters for currency conversion
summa = 100
from_currency = 'USD'
to_currency = 'RUB'

# Make a SOAP request to convert the currency
response = client.service.convert(
    summa=summa,
    fromCurrency=from_currency,
    toCurrency=to_currency,
)

# Extract the converted sum from the SOAP response
converted_sum = response.convertResponse.result

print(f"{summa} {from_currency} = {converted_sum} {to_currency}")
