# Go through all WireCard invoices that appear in email and download all PDF attachments.
# Extract important fields from attachments and output as JSON.

import read_pdf
import iterate_all_wirecard_invoices
import interpret_invoice
import json

invoices = []

for i, invoice in enumerate(iterate_all_wirecard_invoices.iterate_wirecard_invoices()):

	txt = read_pdf.read_pdf(invoice["pdf"])

	# Also save each invoice
	try:
		fields = interpret_invoice.interpret_invoice(txt)
		invoices.append(fields)
		pdf_fn = "invoices/%s.pdf" % fields["Invoice number"]
		txt_fn = "invoices/%s.txt" % fields["Invoice number"]
	except Exception, e:
		pdf_fn = "err.pdf"
		txt_fn = "err.txt"
		print e

	f = open(pdf_fn, "w")
	f.write(invoice["pdf"])
	f.close()

	f = open(txt_fn, "w")
	f.write(txt)
	f.close()

	if txt_fn == "err.txt":
		exit()

print json.dumps(invoices)
