#!/usr/bin/env python
from __future__ import absolute_import

import cgitb, cgi
cgitb.enable()

import lib.template as template, lib.SQL as SQL, lib.amalgutils as amalgutils

form = cgi.FieldStorage()


# TODO: This has massive overlap with updatesentence, refactor em 

sesskey = form.getfirst("sesskey")
sentenceid = form.getfirst("sentenceid")
errors = []
conn = SQL.get_conn()
cursor = SQL.get_cursor(conn)
userid = None

if not sesskey:
	errors.append("No session key.")
if not sentenceid:
	errors.append("No sentence chosen to vote for.")

if not errors:
	cursor.execute("SELECT id FROM users WHERE sesskey = %s LIMIT 1", sesskey)
	row = cursor.fetchone()
	if not row:
		errors.append("Invalid session key.")
	else:
		userid = row['id']

roundid = amalgutils.get_current_round_id(cursor)
if not roundid:
	errors.append("There does not appear to be a round.")

voteid = None
if not errors:
	cursor.execute("SELECT userid FROM sentences WHERE id = %s", sentenceid)
	row = cursor.fetchone()
	if not row:
		errors.append("Invalid sentence ID.")
	else:
		voteid = row["userid"]

if not errors:
	cursor.execute('DELETE FROM votes WHERE userid = %s AND roundid = %s',
		(userid, roundid))
	cursor.execute(
		'INSERT INTO votes (userid, voteid, roundid) VALUES (%s, %s, %s)',
		(userid, voteid, roundid))

result = {}
if errors:
	result['status'] = 'Error'
	result['errors'] = errors
else:
	result['status'] = 'OK'

template.output_json(result)