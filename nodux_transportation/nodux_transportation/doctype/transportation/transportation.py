# -*- coding: utf-8 -*-
# Copyright (c) 2015, NODUX and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import re

class Transportation(Document):
	def before_save(self):
		self.validate_email(self.email)
		tax_id = self.tax_id.replace(".", "").replace(" ", "")
		if self.type_document == "":
			pass
		elif self.type_document == "Pasaporte":
			pass
		elif self.type_document == "RUC":
			self.compute_check_digit(tax_id)
		elif self.type_document == "Cedula":
			self.compute_check_digit(tax_id)
		elif self.type_document == "Consumidor Final":
			self.tax_id = "9999999999999"

	def compute_check_digit(self, raw_number):
		factor = 2
		x = 0
		set_check_digit = None
		if self.type_document == 'RUC':
			if int(raw_number[2]) < 6:
				type_party="persona_natural"
			if int(raw_number[2]) == 6:
				type_party="entidad_publica"
			if int(raw_number[2]) == 9:
				type_party="persona_juridica"

			if type_party == 'persona_natural':
				if len(raw_number) != 13 or int(raw_number[2]) > 5 or raw_number[-3:] != '001':
					frappe.throw("Número RUC no válido")
				number = raw_number[:9]
				set_check_digit = raw_number[9]
				for n in number:
					y = int(n) * factor
					if y >= 10:
						y = int(str(y)[0]) + int(str(y)[1])
					x += y
					if factor == 2:
						factor = 1
					else:
						factor = 2
				res = (x % 10)

				if res ==  0:
					value = 0
				else:
					value = 10 - (x % 10)

				if set_check_digit == str(value):
					pass
				else:
					frappe.throw("Número RUC no válido")

			elif type_party == 'entidad_publica':
				if not len(raw_number) == 13 or raw_number[2] != '6' \
					or raw_number[-3:] != '001':
					frappe.throw("Número RUC no válido")
				number = raw_number[:8]
				set_check_digit = raw_number[8]
				for n in reversed(number):
					x += int(n) * factor
					factor += 1
					if factor == 8:
						factor = 2
				value = 11 - (x % 11)
				if value == 11:
					value = 0
				if set_check_digit == str(value):
					pass
				else:
					frappe.throw("Número RUC no válido")

			else:
				if len(raw_number) != 13 or \
					(type_party in ['persona_juridica'] \
					and int(raw_number[2]) != 9) or raw_number[-3:] != '001':
					frappe.throw("Número RUC no válido")
				number = raw_number[:9]
				set_check_digit = raw_number[9]
				for n in reversed(number):
					x += int(n) * factor
					factor += 1
					if factor == 8:
						factor = 2
				value = 11 - (x % 11)

				if value == 11:
					value = 0
				if set_check_digit == str(value):
					pass
				else:
					frappe.throw("Número RUC no válido")
		else:
			if len(raw_number) != 10:
				frappe.throw("Número C.I. no válido")
			number = raw_number[:9]
			set_check_digit = raw_number[9]
			for n in number:
				y = int(n) * factor
				if y >= 10:
					y = int(str(y)[0]) + int(str(y)[1])
				x += y
				if factor == 2:
					factor = 1
				else:
					factor = 2
			res = (x % 10)
			if res ==  0:
				value = 0
			else:
				value = 10 - (x % 10)
			if set_check_digit == str(value):
				pass
			else:
				frappe.throw("Número C.I. no válido")

	def validate_email(self, email):
		if re.match("[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,3})", email):
			pass
		else:
			frappe.throw("Correo electrónico no cumple con la estructura: ejemplo@mail.com")
