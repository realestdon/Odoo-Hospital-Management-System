# -*-coding: utf-8 -*-

from odoo import fields, models, api, _


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointment'
    _order = 'id desc'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    patient_name = fields.Many2one('hospital.patient', string='Patient Name',
                                   required=True)
    patient_id = fields.Integer(related='patient_name.patient_age',
                                string='Age', readonly=1)
    notes = fields.Text('Registration Note')
    appointment_date = fields.Date('Date', required=True)
    name = fields.Char(string='Appointment ID', copy=False, index=True,
                       default=(_('NEW')))
    state = fields.Selection(
        selection=[('draft', 'Draft'), ('confirm', 'Confirm'), ('done', 'Done'),
                   ('cancel', 'Cancelled')], string='Status', index=True,
        required=True, default='draft', track_visibility='onchange')
    doctors_note = fields.Text('Doctors Note')
    pharmacy_note = fields.Text('Pharmacy Note')
    appointment_ids = fields.One2many('hospital.appointment.lines','appointment_id', string='Appointment')

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code(
            'hospital.appointment.sequence')
        result = super(HospitalAppointment, self).create(vals)
        return result


class HospitalAppointmentLines(models.Model):
    _name = 'hospital.appointment.lines'
    _description = 'Appointment Lines'

    product_id = fields.Many2one('product.product' 'Product')
    appointment_id = fields.Many2one('hospital.appointment', string ='Appointment ID')
    product_qty = fields.Integer('Quantity')