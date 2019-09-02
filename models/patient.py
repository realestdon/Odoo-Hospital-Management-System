# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    patient_name = fields.Many2one('hospital.patient', 'Patient Name')


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _order = 'id desc'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Patient Record'
    _rec_name = 'patient_name'

    @api.model
    def _get_default_note(self):
        return "This is A DEFAULT NOTE"

    @api.multi
    def open_patient_appointments(self):
        return {
            'name': _('Appointments'),
            'domain':[('patient_name','=',self.id)],
            'res_model': 'hospital.appointment',
            'view_type':'form',
            'view_mode':'tree,form',
            'view_id': False,
            'type':'ir.actions.act_window'
        }

    patient_name = fields.Char('Name', required=True)
    patient_age = fields.Integer('Age')
    notes = fields.Text('Notes', default=_get_default_note)
    image = fields.Binary('Image')
    name = fields.Char('Test')
    gender = fields.Selection(string='Gender',selection=[('male', 'Male'),('fe_male', 'Female')],default='male')
    age_group = fields.Selection(string='Age Group', selection=[('major','Major'),('minor','Minor')],compute='_set_age_group')
    name_seq = fields.Char(string='Order Reference', required=True,
                           readonly=True, copy=False, index=True,
                           default=lambda self: _('NEW'))
    appointment_count = fields.Integer('# Appointments',compute='_number_of_appointments')
    appointment_ids = fields.One2many('hospital.appointment','patient_name')

    @api.multi
    def _number_of_appointments(self):
        data = self.env['hospital.appointment'].search([('patient_name','=',self.ids)]).ids
        self.appointment_count = len(data)

    @api.constrains('patient_age')
    def check_age(self):
        for rec in self:
            if rec.patient_age <= 5:
                raise ValidationError(_('Patient is too Young'))

    @api.model
    def create(self, vals):
        vals['name_seq'] = self.env['ir.sequence'].next_by_code(
            'hospital.patient.sequence')
        return super(HospitalPatient, self).create(vals)

    @api.depends('patient_age')
    def _set_age_group(self):
        for items in self:
            if items.patient_age:
                if items.patient_age > 18:
                    items.age_group = 'major'
                else:
                    items.age_group = 'minor'
