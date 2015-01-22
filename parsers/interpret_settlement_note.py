# -*- coding: utf-8 -*-
import re
import datetime

# A balance note is a grouping of several invoices and the calculation
# of how that balance is turned from USD to EUR before transfer.
#
# Given a balance note sent as email attachment and converted with pdf2txt
# to a text representation, finds out which invoices it is grouping.
def interpret_settlement_note(txt):
	l = txt.splitlines()

	out = {}

	i = l.index("Settlement Note") + 2
	keys = []
	while l[i].endswith(":"):
		keys.append(l[i][0:-1]) # without the colon
		i += 2
	values = []
	for i in range(i, i + len(keys)*2, 2):
		values.append(l[i])

	out.update(zip(keys, values))

	def key_from_value(v):

		k = None

		if v == "":
			pass
		elif "WDB" in v:
			k = "Business Case"
		elif len(v.split(" ")[0]) == 16 and "JP" in v.split(" ")[0]:
			k = "Invoice No."
		elif v[0].isdigit() and "." in v and len(v.split(".")[1]) > 2 and "EUR" in v:
			k = "Exchange Rate"
		elif "*" in v and v[0] in "0123456789-":
			k = "Settlement Amount"
		elif "*" not in v and v[0] in "0123456789-":
			k = "Invoice Amount"
		elif v in ["Reserve payout USD", "USD"]:
			k = "Comment"

		return k

	relevant_lines = l[l.index("Business Case") : l.index("EUR", l.index("Business Case"))]
	row_count = len([x for x in relevant_lines if key_from_value(x) == "Business Case"])
	invoices = []

	i = 0
	while i < len(relevant_lines):

		line = relevant_lines[i]
		k = key_from_value(line)
		#print k, "\t", line

		if not k:
			i += 1
			continue

		if k == "Invoice No.": # Continues to next line
			v = line + " " + relevant_lines[i + 1]
			i += 1
		else:
			v = line

		if k == "Settlement Amount":
			v = v.replace(" *", "")

		if k == "Business Case":
			invoices.append({
				k : v
			})
		else:
			# Set to first invoice which is missing this field.
			for invoice in invoices:
				if k not in invoice:
					invoice[k] = v
					break

		i += 1

	# Line with Invoice No. still has dates attached, move those to dedicated fields.
	for invoice in invoices:
		invoice["Start"], invoice["End"] = invoice["Invoice No."].split(" ", 1)[1].split(" - ")
		invoice["Invoice No."] = invoice["Invoice No."].split(" ")[0]

	out["invoices"] = invoices
	return out

txt = """2012-06-15

Settlement Note

Settlement ID:

Creation Date:

Settlement Period:

Merchant Name:

120610-1005000715

2012-06-10

2012-05-14-2012-06-10

TMI Bemmu WDB

Business Case

Invoice No.

Billing Period

Comment

Invoice Amount Exchange Rate Settlement Amount

Candyjapan WDB

Candyjapan WDB

Candyjapan WDB

Total Payout

Your BankDetails:

Account Name:

Account Number:
Routing Number:

Bank Name:

Bank Location:

Swift Code:

IBAN:

Additional Information:

201221JP00041209 2012-05-14 -
2012-05-20
201223JP00042940 2012-06-01 -
2012-06-03
201224JP00043771 2012-06-04 -
2012-06-10

USD

USD

USD

-0.32

0.776471 EUR

-0.25 *

43.56

0.789222 EUR

34.38 *

173.96

0.789222 EUR

137.29 *

EUR

171.42

Bemmu Sepponen

Sampo Bank

Finland

DABAFIHHXXX

FI5580001771121028

* The amount shown differs from the original invoice amount.

Wirecard Bank AG | Einsteinring 35 | D-85609 Aschheim, Germany
Phone: +49 (0) 89 / 4424 - 0400 | Fax: +49 (0) 89 / 4424 - 0500 | Email: contact@wirecard.com | www.wirecard.de

Board: Dr. Markus Braun, Jan Marsalek, Burkhard Ley | Supervisory Board Chairman: Wulf Matthias
Registered at Amtsgericht München | Commercial Register (Handelsregister) Number: 142 427 | USt-ID.: DE 812 588 608
Bank details: Account number 512 480 503 | Commerzbank München | BLZ 700 400 41 | SWIFT COBADEFF700"""

if __name__ == "__main__":
	print interpret_settlement_note(txt)