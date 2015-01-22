# WireCard email parser

WireCard is a payment gateway. Periodically they send you important email concerning money that
has been processed through them. What if later on you find a need to do something with that
information? You would have to go through all emails and attached PDFs and manually do
data entry to extract all that data.

Another option would be to write some software to go through those emails, download each
attached PDF and then parse them. That is the aim of the scripts here.

![parsed pdf](https://github.com/Bemmu/wirecard_email_parser/raw/master/screenshot.png)

## Supported messages

Currently two types of messages are supported:

* Settlement notes / balance notes
* Invoices

Each invoice is a set of credit card transactions that WireCard processed for you. Each
settlement note / balance note describes a remittance of money to your bank account and
it is comprised of several invoices bundled together.

## Assumptions made

I wrote this purely for my own use, so there is **no guarantee that it will work for you**.
In particular I assumed that credit cards are charged in USD but remittances are made in EUR.
If this is not the case the parser will most likely break.

Another assumption is that in a settlement note your Business Case must include the word "WDB".
The Python version I used was 2.7.8.

## Structure

The parsers directory contains scripts that can extract fields from WireCard PDFs that
have first been turned into text files.

[Pdfminer](http://www.unixuser.org/~euske/python/pdfminer/) is a project by Yusuke Shinyama. It turns PDFs into text files. It has a lot of options, but here only the default PDF -> TEXT conversion is used. To make things easier, I embedded the whole project
(also MIT licensed) here. I added read_pdf.py, a simplified function for using pdfminer to do the default conversion.

## Email access

In order to find messages from WireCard and download the attached PDFs, email access
is needed. The scripts browse your email over imap. I have only tested this with gmail.
The code will look for messages from noreply@wirecard.com and invoice@wirecard.com and
download the attached PDFs. Set your email address and password in the environment
variables wirecard_email and wirecard_email_password.

For example to test in Mac OS X command line:

    export WIRECARD_EMAIL=me@bemmu.com
    export WIRECARD_EMAIL_PASSWORD=foobar
    python iterate_all_wirecard_invoices.py
