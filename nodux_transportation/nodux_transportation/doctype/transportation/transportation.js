// Copyright (c) 2016, NODUX and contributors
// For license information, please see license.txt

frappe.ui.form.on('Transportation', {
	refresh: function(frm) {

	},
	type_document: function(frm) {
		if (frm.doc.type_document == "Consumidor Final"){
			frm.set_value("tax_id", "9999999999999");
		}

		frm.refresh_fields();
	}

});
