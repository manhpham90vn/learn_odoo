# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import models, fields


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'estate.estate'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: fields.Date.today() + timedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean(default=True)
