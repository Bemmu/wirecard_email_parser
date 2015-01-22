# WireCard email parser

WireCard is a payment gateway. Periodically they send you important email concerning money that
has been processed through them. What if later on you find a need to do something with that
information? You would have to go through all emails and attached PDFs and manually do
data entry to extract all that data.

Another option would be to write some software to go through those emails, download each
attached PDF and then parse them. That is the aim of the scripts here. 

## Supported messages

Currently two types of messages are supported:

* Settlement notes / balance notes
* Invoices

Each invoice is a set of credit card transactions that WireCard processed for you. Each
settlement note / balance note describes a remittance of money to your bank account and
it is comprised of several invoices bundled together.

I wrote this purely for my own use, so there is **no guarantee that it will work for you**.
In particular I assumed that credit cards are charged in USD but remittances are made in EUR.
If this is not the case the parser will most likely break.

## Structure

The parsers directory contains scripts that can extract fields from WireCard PDFs that
have first been turned into text using pdf2txt with default settings.

