import datetime
import os
import requests
import sqlite3
import tempfile
import time
import config

def create_row(date,description,amounts, balance=0.0, debtor=""):
	return {
		'date': str(date),
		'description': description,
		'amounts': amounts,
	}

# TODO: allow diferent input data formats.
def copa():

	result = []
	n_members = len(config.members)

	for column,member in enumerate(config.members):
		
		member_file = tempfile.NamedTemporaryFile(delete=False)
		try:
			u = requests.get(member['url'])
			member_file.write(u.content)
			member_file.close()

			conn = sqlite3.connect(member_file.name)

			for row in conn.execute("select expensed, description, amount, property, category, subcategory  from expense_report %s" % member['sql_filter']):
				date = datetime.date.fromtimestamp(time.mktime(time.gmtime(row[0]//1000)))
				desc = ("%s %s" % ( row[1], row[3] )).strip()
				if not desc:
					desc = ("%s:%s" % ( row[4], row[5] )).strip()
				amount = float(row[2])
				if row[4] == "Income":
					amount = -amount
				amounts = [ 0.0 ] * n_members
				amounts[column] = amount
				result.append(create_row(date, desc,amounts))
	
			conn.close()
		finally:
			os.remove(member_file.name)

	resultS = sorted(result, key=lambda row: row['date'])

	amounts = [ 0.0 ] * n_members
	resultS.insert(0, create_row(resultS[0]['date'], 'Remanider',amounts))

	# Post processing
	balance = [ 0.0 ] * n_members
	for column,member in enumerate(config.members):
		balance[column] = member['initial']

	for row in resultS:
		for column,member in enumerate(config.members):
			balance[column] += row['amounts'][column]
			balance = [ x - row['amounts'][column]  / n_members for x in balance ]
		row['balance'] = balance[:]

	return resultS
