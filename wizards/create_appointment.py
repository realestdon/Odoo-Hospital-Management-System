# -*- coding: utf-8 -*-

from odoo import models,fields


class CreateAppointment(models.TransientModel):
    _name = 'create.appointment'

    patient_id = fields.Many2one('hospital.patient', string='Patient Name',
                                   required=True)
    appointment_date = fields.Date('Date', required=True)