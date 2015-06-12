This project generates email invoices for Fort Collins Creator Hub membership
fees. It's probably not that useful to anyone else; I'm mainly pushing it out
via git for ease of backup.

Usage notes:

In a web browser, open the membership spreadsheet, and select-all.

Paste it unchanged into a new plain text file e.g. data.txt.

rm *.email
./gen-invoice.py data.txt 'Jul 2015'
git send-email *.email

Give an empty answer to:
Who should the emails be sent to (if any)?
Message-ID to be used as In-Reply-To for the first email (if any)?
