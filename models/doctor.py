# -*- coding: utf-8 -*-

from odoo import models, fields, _,api


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _inherit = ['mail.thread','ir.needaction_mixin']
    _description = 'Hospital Doctor'
    _rec_name = 'doctor_name'

    doctor_name = fields.Char('Doctor Name')
    doctor_user = fields.Many2one('res.users', string='Related User')
    gender = fields.Selection(
        selection=[('male', 'Male'), ('female', 'Female')], default='male',
        index=True, required=True, copy=False)
    name = fields.Char('Doctor ID',default=_('NEW'),readonly=True)

    @api.model
    def create(self,vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('doctors.sequence')
        result = super(HospitalDoctor,self).create(vals)
        return result
