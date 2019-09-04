# -*- coding: utf-8 -*-

from odoo import models, fields


class CreateAppointment(models.TransientModel):
    _name = 'create.appointment'

    patient_id = fields.Many2one('hospital.patient', string='Patient Name',
                                 required=True)
    appointment_date = fields.Date('Date', required=True)
    gender = fields.Selection(string='Doctor Gender',selection=[('male', 'Male'),('female', 'Female')])

    def action_submit(self):
        vals = {
            'patient_name': self.patient_id.id,
            'appointment_date': self.appointment_date
        }
        self.env['hospital.appointment'].create(vals)

