# -*- coding: utf-8 -*-

def interpret_invoice(txt):
	l = txt.splitlines()

	out = {
		"Debit Volume" : 0,
		"Credit Volume" : 0
	}

	# After the line "Invoice" there are some keys and then their values.
	# Then there is yet another similar group of key-value pairs.
	i = l.index("Invoice") + 2

	def kv():
		keys = [x.replace(":", "").strip() for x in l[i:l.index("", i)]]
		values_begin = i + 1 + len(keys)
		values = l[values_begin:values_begin + len(keys)]
		out.update(zip(keys, values))
		return values_begin + len(keys) + 1

	i = kv()
	kv()

	# A list of numbers and a list of explanations of what those numbers are
	# are in two separate parts of the text, but in the same order.	
	i = l.index("Amount") + 1
	j = [k for k, v in enumerate(l) if "the following transactions" in v][0] + 2
	gather = []
	prev = None # sometimes key continues on next line
	while l[i] == "" or l[i][0] in "0123456789-":
		if l[j] != "":
			v = l[i].replace("   USD", "").replace(",", "")
			k = l[j]

			if prev:
				k = prev + " " + k
				prev = None

			if v:
				out[k] = v
			else:
				prev = l[j]

		i += 1
		j += 1
		if l[j] == "The recipient has to account for VAT due":
			j += 1 # skip this line

	# Find the part that lists which numbers will be mentioned.
	matches = [k for k, v in enumerate(l) if "the following transactions" in v]
	assert(len(matches) == 1)
	i = matches[0] + 2
	which_numbers_will_be_mentioned = []
	while True:
		if l[i] == "":
			break
		which_numbers_will_be_mentioned.append(l[i])
		i += 1

	# Total count of previously mentioned values, debit and/or credit volume.
	if which_numbers_will_be_mentioned != ["Number"]: # no transactions?
		prev = None
		for i, k in enumerate(which_numbers_will_be_mentioned):	
			n = l[l.index("Number") + 1 + i]
			if n == "":
				prev = k
				continue

			if prev:
				k = prev + " " + k
				prev = None

			out[k + " count"] = int(n)

	return out

txt = """Wirecard Bank AG | Einsteinring 35 | D-85609 Aschheim, Germany

TMI Bemmu
Koulurinne 17 F
64100 Kristiinankaupunki
Finland
VAT ID: FI18957687

Invoice

Invoice number:
Merchant:
Merchant ID:
Brand:

201227JP00047352
Candyjapan WDB
0000003168323F46
Discover, Visa, Diners, Master Card

Billing period:
Currency:
Product:
Acquirer name:

06/25/2012 - 06/30/2012
USD
Credit Card

Dear Ladies and Gentlemen,

for the billing period 06/25/2012 - 06/30/2012 the following transactions were cleared on your behalf.

Debit Volume

Total Net Turnover
Discount
Transaction Fees

Total Fees without VAT
VAT on Fees

Total Fees
Reserve

Payout Amount

Number
2

Volume
47.90   USD

Rate

0.00%

5.00%

We will wire the according amount to your account stated below.

Account owner:
Account number:
Routing number:
Bank name:
Bank location:
SWIFT code:
IBAN:

With best regards,
Wirecard Bank AG

Bemmu Sepponen
n/a
n/a
Sampo Bank
Helsinki, Finland
DABAFIHHXXX
FI5580001771121028

07/02/2012

Amount
47.90   USD

47.90   USD
1.32   USD
0.62   USD

1.94   USD
0.00   USD

1.94   USD
2.40   USD

43.56   USD

Wirecard Bank AG | Einsteinring 35 | D-85609 Aschheim, Germany
Phone: +49 (0) 89 4424 - 2000 | Fax: +49 (0) 89 4424 - 2100 | Email: info@wirecard.com | www.wirecard.com

Managing Board: Franz Brücklmeier, Burkhard Ley, Rainer Wexeler | Chairman of the Supervisory Board : Wulf Matthias
Registered at Amtsgericht Muenchen | HRB Number: 161178 | VAT: DE 207567674
Bank Details: Commerzbank Munich | Account 512 480 503 | Sort Code 700 400 41 | SWIFT COBADEFF700 | IBAN DE91 7004 0041 0512 4805 03

Discount Overview Master Card

Total

Number
0

Volume
0.00   USD

Discount

Amount
0.00   USD

Discount Overview Diners

Total

Discount Overview Visa

Debit Volume

Total

Discount Overview Discover

Number
0

Volume
0.00   USD

Discount

Amount
0.00   USD

Number
2
2

Volume
47.90   USD
47.90   USD

Discount
2.75%

Amount
1.32   USD
1.32   USD

Total

Number
0

Volume
0.00   USD

Discount

Amount
0.00   USD

Transaction Fee Overview

Sales

Total

Successful Transactions

Number
2
2

Rate
0.31   USD

Amount
0.62   USD
0.62   USD

Unsuccessful Transactions

Number

Rate

Amount

0

0.00   USD

Amount

0.62   USD
0.62   USD

Wirecard Bank AG | Einsteinring 35 | D-85609 Aschheim, Germany
Phone: +49 (0) 89 4424 - 2000 | Fax: +49 (0) 89 4424 - 2100 | Email: info@wirecard.com | www.wirecard.com

Managing Board: Franz Brücklmeier, Burkhard Ley, Rainer Wexeler | Chairman of the Supervisory Board : Wulf Matthias
Registered at Amtsgericht Muenchen | HRB Number: 161178 | VAT: DE 207567674
Bank Details: Commerzbank Munich | Account 512 480 503 | Sort Code 700 400 41 | SWIFT COBADEFF700 | IBAN DE91 7004 0041 0512 4805 03"""

txt2 = """Wirecard Bank AG | Einsteinring 35 | D-85609 Aschheim, Germany

TMI Bemmu
Koulurinne 17 F
64100 Kristiinankaupunki
Finland
VAT ID: FI18957687

Invoice

Invoice number:
Merchant:
Merchant ID:
Brand:

201221JP00041209
Candyjapan WDB
0000003168323F46
Discover, Visa, Diners, Master Card

Billing period:
Currency:
Product:
Acquirer name:

05/14/2012 - 05/20/2012
USD
Credit Card

Dear Ladies and Gentlemen,

for the billing period 05/14/2012 - 05/20/2012 the following transactions were cleared on your behalf.

Number

Volume

Rate

0.00%

Total Net Turnover
Transaction Fees

Total Fees without VAT
VAT on Fees

Total Fees

Payout Amount

We will wire the according amount to your account stated below.

Account owner:
Account number:
Routing number:
Bank name:
Bank location:
SWIFT code:
IBAN:

With best regards,
Wirecard Bank AG

Bemmu Sepponen
n/a
n/a
Sampo Bank
Helsinki, Finland
DABAFIHHXXX
FI5580001771121028

05/21/2012

Amount

0.00   USD
0.32   USD

0.32   USD
0.00   USD

0.32   USD

-0.32   USD

Wirecard Bank AG | Einsteinring 35 | D-85609 Aschheim, Germany
Phone: +49 (0) 89 4424 - 2000 | Fax: +49 (0) 89 4424 - 2100 | Email: info@wirecard.com | www.wirecard.com

Managing Board: Franz Brücklmeier, Burkhard Ley, Rainer Wexeler | Chairman of the Supervisory Board : Wulf Matthias
Registered at Amtsgericht Muenchen | HRB Number: 161178 | VAT: DE 207567674
Bank Details: Commerzbank Munich | Account 512 480 503 | Sort Code 700 400 41 | SWIFT COBADEFF700 | IBAN DE91 7004 0041 0512 4805 03

Discount Overview Master Card

Total

Number
0

Volume
0.00   USD

Discount

Amount
0.00   USD

Discount Overview Diners

Total

Discount Overview Visa

Number
0

Volume
0.00   USD

Discount

Amount
0.00   USD

Total

Number
0

Volume
0.00   USD

Discount

Amount
0.00   USD

Discount Overview Discover

Total

Number
0

Volume
0.00   USD

Discount

Amount
0.00   USD

Transaction Fee Overview

Authorization

Total

Successful Transactions

Number

Rate

Amount

0

0.00   USD

Unsuccessful Transactions

Number
1
1

Rate
0.32   USD

Amount
0.32   USD
0.32   USD

Amount

0.32   USD
0.32   USD

Wirecard Bank AG | Einsteinring 35 | D-85609 Aschheim, Germany
Phone: +49 (0) 89 4424 - 2000 | Fax: +49 (0) 89 4424 - 2100 | Email: info@wirecard.com | www.wirecard.com

Managing Board: Franz Brücklmeier, Burkhard Ley, Rainer Wexeler | Chairman of the Supervisory Board : Wulf Matthias
Registered at Amtsgericht Muenchen | HRB Number: 161178 | VAT: DE 207567674
Bank Details: Commerzbank Munich | Account 512 480 503 | Sort Code 700 400 41 | SWIFT COBADEFF700 | IBAN DE91 7004 0041 0512 4805 03"""

txt3 = """Wirecard Bank AG | Einsteinring 35 | D-85609 Aschheim, Germany

TMI Bemmu
Koulurinne 17 F
64100 Kristiinankaupunki
Finland
VAT ID : FI18957687

Invoice

Invoice number :
Merchant :
Merchant ID :
Brand :

201448JP01059173
Candyjapan WDB
0000003168323F46
Discover, Visa, Diners, Master Card

Billing period :
Currency :
Product :
Acquirer name :

11/17/2014 - 11/23/2014
USD
Credit Card
WDB

Dear Ladies and Gentlemen,

for the billing period 11/17/2014 - 11/23/2014 the following transactions were cleared on your behalf.

Debit Volume
Debit missing Chargebacks for
October 2014
Credit Volume
Chargeback

Total Net Turnover
Discount
Transaction Fees
General Fees

Total Fees without VAT
VAT on Fees
The recipient has to account for VAT due

Total Fees
Reserve

Payout Amount

Number
125

1
6
1

Rate

Volume
3,317.65   USD

25.00   USD
87.50   USD
50.00   USD

0.00 %

5.00 %

We will wire the according amount to your account stated below.

Account owner :
Account number :
Routing number :
Bank name :
Bank location :
SWIFT code :
IBAN :

With best regards,
Wirecard Bank AG

Bemmu Sepponen
n/a
n/a
Sampo Bank
Helsinki, Finland
DABAFIHHXXX
FI5580001771121028

11/24/2014

Amount
3,317.65   USD

-25.00   USD
-87.50   USD
-50.00   USD

3,155.15   USD
91.24   USD
72.37   USD
19.01   USD

182.62   USD
0.00   USD

182.62   USD
165.88   USD

2,806.65   USD

Wirecard Bank AG | Einsteinring 35 | D-85609 Aschheim, Germany
Phone: +49 (0) 89 4424 - 2000 | Fax: +49 (0) 89 4424 - 2100 | Email: info@wirecard.com | www.wirecard.com

Managing Board: Alexander von Knoop, Burkhard Ley, Rainer Wexeler | Chairman of the Supervisory Board : Wulf Matthias
Registered at Amtsgericht Muenchen | HRB Number: 161178 | VAT: DE 207567674
Bank Details: Commerzbank Munich | Account 512 480 503 | Sort Code 700 400 41 | SWIFT COBADEFF700 | IBAN DE91 7004 0041 0512 4805 03

Discount Overview Master Card

Debit Volume
Credit Volume
Chargeback

Total

Discount Overview Diners

Total

Discount Overview Visa

Debit Volume
Credit Volume

Total

Discount Overview Discover

Number
35
4
1
40

Volume
932.55   USD
50.00   USD
50.00   USD
1,032.55   USD

Discount
2.75 %
0.00 %
0.00 %

Amount
25.65   USD
0.00   USD
0.00   USD
25.65   USD

Number
0

Volume
0.00   USD

Discount

Amount
0.00   USD

Number
90
2
92

Volume
2,385.10   USD
37.50   USD
2,422.60   USD

Discount
2.75 %
0.00 %

Amount
65.59   USD
0.00   USD
65.59   USD

Total

Number
0

Volume
0.00   USD

Discount

Amount
0.00   USD

Transaction Fee Overview

Sales
Chargeback
Refund

Total

Successful Transactions

Number
125

Rate
0.31   USD
1 18.74   USD
6
0.31   USD
132

Amount
38.75   USD
18.74   USD
1.86   USD
59.35   USD

Unsuccessful Transactions

Number
42

Rate
0.31   USD

Amount
13.02   USD

42

13.02   USD

General Fee Overview

Debit missing Chargeback fee for October 2014
Total

Amount

51.77   USD
18.74   USD
1.86   USD
72.37   USD

Amount
19.01   USD
19.01   USD

Wirecard Bank AG | Einsteinring 35 | D-85609 Aschheim, Germany
Phone: +49 (0) 89 4424 - 2000 | Fax: +49 (0) 89 4424 - 2100 | Email: info@wirecard.com | www.wirecard.com

Managing Board: Alexander von Knoop, Burkhard Ley, Rainer Wexeler | Chairman of the Supervisory Board : Wulf Matthias
Registered at Amtsgericht Muenchen | HRB Number: 161178 | VAT: DE 207567674
Bank Details: Commerzbank Munich | Account 512 480 503 | Sort Code 700 400 41 | SWIFT COBADEFF700 | IBAN DE91 7004 0041 0512 4805 03
"""

if __name__ == "__main__":
	print interpret_invoice(txt3)
