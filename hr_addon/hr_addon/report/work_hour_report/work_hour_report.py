# Copyright (c) 2022, Jide Olayinka and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = [], []
	condition_date,condition_employee = "",""
	if filters.date_from_filter and filters.date_to_filter :
		if filters.date_from_filter == None:
			filters.date_from_filter = frappe.datetime.get_today()
		if filters.date_to_filter == None:
			filters.date_to_filter = frappe.datetime.get_today()
		condition_date = "AND log_date BETWEEN '"+ filters.date_from_filter + \
        "' AND '" + filters.date_to_filter + "'"

	if filters.get("employee_id"):
		empid = filters.get("employee_id")
		condition_employee += f" AND employee = '{empid}'"
	# #{'fieldname':'employee','label':'Employee','width':160},
	# {'fieldname':'target_hours','label':'Target Hours','width':80},
	columns = [		
		{'fieldname':'log_date','label':'Date','width':110},		
		{'fieldname':'employee','label':'Employee',  "fieldtype": "Link", "options": "Employee", 'width':200,},		
		{'fieldname':'name','label':'Work Day',  "fieldtype": "Link", "options": "Workday", 'width':200,},		
		{'fieldname':'status','label':'Status', "width": 80},
		{'fieldname':'total_work_seconds','label':_('Work Hours'), "width": 110, },
		{'fieldname':'total_break_seconds','label':_('Break Hours'), "width": 110, },
		{'fieldname':'total_target_seconds','label':'Target Seconds','width':80},
		{'fieldname':'diff_log','label':'Diff','width':90},
		{'fieldname':'first_in','label':'First Checkin','width':100},
		{'fieldname':'last_out','label':'Last Checkout','width':100},
		{'fieldname':'attendance','label':'Attendance','width': 160},
		
	]
	work_data = frappe.db.sql(
		"""		
		SELECT name,log_date,employee,attendance ,status,total_work_seconds,total_break_seconds,
		target_hours, total_target_seconds, (total_work_seconds - total_target_seconds) as diff_log,
		TIME(first_checkin) as first_in,TIME(last_checkout) as last_out 
		FROM `tabWorkday` 
		WHERE docstatus < 2 %s %s 
		ORDER BY log_date ASC
		"""%( condition_date, condition_employee),as_dict=1,
	)
	
	data = work_data

	return columns, data