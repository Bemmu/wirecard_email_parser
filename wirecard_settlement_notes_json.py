# Go through gmail looking for wirecard settlement / balance notes and turn them
# into a JSON structure. Also save all source PDF attachments.

import iterate_all_wirecard_settlements
import read_pdf
import interpret_balance_note
import interpret_settlement_note
import json

notes = []

for settlement in iterate_all_wirecard_settlements.iterate_wirecard_settlements():

	# Convert attached pdf to text
	txt = read_pdf.read_pdf(settlement["pdf"])

	# Read from text using suitable function depending on type of note
	if settlement["Subject"].startswith("Settlement"):
		f = interpret_settlement_note.interpret_settlement_note
	else:
		f = interpret_balance_note.interpret_balance_note

	note = f(txt)

	pdf_fn = "settlements/%s.pdf" % note['Settlement ID']
	txt_fn = "settlements/%s.txt" % note['Settlement ID']
	f = open(pdf_fn, "w")
	f.write(settlement["pdf"])
	f.close()
	f = open(txt_fn, "w")
	f.write(txt)
	f.close()

	# Skip duplicates
	is_dupe = note["Settlement ID"] in [n["Settlement ID"] for n in notes]
	if not is_dupe:
		notes.append(note)

print json.dumps(notes)

