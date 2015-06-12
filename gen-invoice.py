#!/usr/bin/env python3

# Copyright (c) 2015, Stephen Warren.  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# Neither the name Stephen Warren, the name Fort Collins Creator Hub, nor the
# names of this software's contributors may be used to endorse or promote
# products derived from this software without specific prior written
# permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from email.message import Message
import sys

app = sys.argv.pop(0)
fni = sys.argv.pop(0)
month = sys.argv.pop(0)

fi = open(fni, 'rt')

# FIXME: We should search for the heading row, not assume it's the second row
cruft_row = fi.readline()
heading_row = fi.readline()
headings = heading_row.split('\t')

COL_NAME = 0
COL_EMAIL = 1
COL_RATE = 2
COL_PAID = 3
col_headings = {
    COL_NAME:  'Name',
    COL_EMAIL: 'Email',
    COL_RATE:  'Monthly rate',
    COL_PAID:  month,
}
col_indices = {}
for (n, heading) in col_headings.items():
    col_indices[n] = headings.index(heading)

def gen_invoice(name, email, rate, fnum):
    msg = Message()
    msg.add_header('From', 'Stephen Warren <swarren@wwwdotorg.org>')
    msg.add_header('To', '"' + name + '" <' + email + '>')
    msg.add_header('Cc', '"FCCH Billing" <billing@fortcollinscreatorhub.org>')
    msg.add_header('Subject', 'Fort Collins Creator Hub ' + month + ' Invoice')
    msg.add_header('Content-type', 'text/plain')
    msg.set_payload('''\
Dear %(name)s,

This is a friendly reminder that your Fort Collins Creator Hub monthly
membership fee of $%(rate)s for %(month)s is due by the first of that month.
If you've already paid, please do accept my apologies.

You can choose to pay by check (or bank billpay) made out to Fort Collins
Creator Hub and sent to:

Fort Collins Creator Hub
PO Box 271094
Fort Collins CO 80527

Or, you can pay by credit card via the Payments page on our website:
http://www.fortcollinscreatorhub.org/

Thanks!
''' % {
    'name': name,
    'rate': rate,
    'month': month,
})

    fon = '%04d-%s.email' % (fnum, name.lower().replace(' ', '-'))
    fo = open(fon, 'wt')
    fo.write(msg.as_string())
    fo.close()

fnum = 0

# FIXME: We should probably persist this in a config file
paid_map = {
    '': False,
}

for value_row in fi.readlines():
    values = value_row.split('\t')
    name = values[col_indices[COL_NAME]].strip()
    email = values[col_indices[COL_EMAIL]].strip()
    rate = values[col_indices[COL_RATE]].strip()
    paid = values[col_indices[COL_PAID]].strip()

    while not paid in paid_map:
        is_paid_text = input('Is "%s" paid? (y/n): ' % paid)
        if is_paid_text == 'y':
            paid_map[paid] = True
        elif is_paid_text == 'n':
            paid_map[paid] = False
        else:
            print('That is not a valid option')
    is_paid = paid_map[paid]
    if is_paid:
        continue

    gen_invoice(name, email, rate, fnum)
    fnum += 1
