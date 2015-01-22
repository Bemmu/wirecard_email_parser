# -*- coding: utf-8 -*-

import re
import datetime

# A balance note is a grouping of several invoices and the calculation
# of how that balance is turned from USD to EUR before transfer.
#
# Given a balance note sent as email attachment and converted with pdf2txt
# to a text representation, finds out which invoices it is grouping.
def interpret_balance_note(txt):
	l = txt.splitlines()
	out = {}		

	# Balance Note
	#
	# Settlement ID      <---- list of keys
	# Settlement Date
	# Settlement Period
	# Merchant Name
	#
	# Current Balance
	#
	# 150104-1005001790   <--- list of values
	# 01/04/2015
	# 12/29/2014-01/04/2015
	# TMI Bemmu WDB

	# In the beginning there is a list of keys and then their values
	keys_start = l.index("Balance Note") + 2
	keys_end = l.index("", keys_start) - 1
	keys = l[keys_start:keys_end + 1]
	values = l[keys_end + 4:keys_end + 4 + len(keys)]
	out.update(zip(keys, values))

	i = l.index("Billing Period") + 2
	invoices = []
	while l[i] and l[i+1]:
		s = l[i] + " " + l[i+1]
		i += 2
		m = re.match(r".* (\d+JP\d+) (\d\d/\d\d/\d\d\d\d) - (\d\d/\d\d/\d\d\d\d).*", s).groups()

#		string_to_date = lambda s:datetime.date(int(s.split("/")[2]), int(s.split("/")[0]), int(s.split("/")[1]))
		string_to_date = lambda s:"-".join([s.split("/")[2], s.split("/")[0], s.split("/")[1]])

		invoices.append(
			{
				"Invoice ID" : m[0],
				"Start" : string_to_date(m[1]),
				"End" : string_to_date(m[2])
			}
		)

	out["invoices"] = invoices

	i = l.index("Exchange") + 5

	if l[i] == "USD":
		i += 2

	invoice_i = 0
	while l[i][0] in "0123456789-":
		out["invoices"][invoice_i]["Withheld Reserves"] = l[i].replace(",", "")
		out["invoices"][invoice_i]["Invoice Amount"] = l[i+2].replace(",", "")
		out["invoices"][invoice_i]["Exchange Rate"] = l[i+4]
		out["invoices"][invoice_i]["Amount"] = l[i+8].replace(" *", "").replace(",", "")
		i += 10
		invoice_i += 1

	return out

txt = """Wirecard Bank AG | Einsteinring 35 | 85609 Aschheim

08/22/2013

Balance Note

Settlement ID
Settlement Date
Settlement Period
Merchant Name

Current Balance

130818-1005001140
08/18/2013
08/12/2013-08/18/2013
TMI Bemmu WDB

Merchant Account

Invoice No.

Billing Period

Candyjapan WDB 201334JP00462569 08/12/2013 -
08/18/2013

Withheld
Reserves

Invoice
Amount

Exchange
Rate

Amount

USD

-70.61

1,256.36

0.741906

EUR

932.10 *

Sub total

Total

EUR

932.10

EUR

932.10

*The invoice amount onto the balance note might differ from the original invoice amount

Your banking details:

Account holder
Account number
Routing number
Bank name
Bank location
Swift Code
IBAN
Additional information

Bemmu Sepponen

Sampo Pankki
Finland
DABAFIHHXXX
FI5580001771121028

Wirecard Bank AG | Einsteinring 35 | D-85609 Aschheim, Germany
Phone: +49 (0)89 4424 - 2000 | Fax: +49 (0)89 /4424 - 2100 | Email: info@wirecardbank.com | www.wirecardbank.com
 
Managing Board: Franz Brücklmeier, Burkhard Ley, Rainer Wexeler | Chairman of the Supervisory Board : Wulf Matthias
Registered at Amtsgericht Muenchen | HRB Number: 161178 | VAT: DE 207567674
Bank Details: Commerzbank Munich | Account 512 480 503 | Sort Code 700 400 41 | SWIFT COBADEFF700 | IBAN DE91 7004 0041 0512 4805 03"""

if __name__ == "__main__":
	print interpret_balance_note(txt)