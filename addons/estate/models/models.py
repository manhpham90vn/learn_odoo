# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import models, fields, api


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'estate.estate'

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('expected_price', 'offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = record.expected_price
            for offer in record.offer_ids:
                if offer.price > record.best_price:
                    record.best_price = offer.price

    @api.onchange('garden', 'garden_orientation')
    def _onchange_garden(self):
        if self.garden:
            if not self.garden_area:
                self.garden_area = 10
            if not self.garden_orientation:
                self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

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
    property_type_id = fields.Many2one('estate.property.type', ondelete='set null', string='Property Type')
    buyer_id = fields.Many2one('res.partner', ondelete='set null', string='Buyer')
    seller_id = fields.Many2one('res.partner', ondelete='set null', string='Seller')
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer(compute='_compute_total_area', store=True)
    best_price = fields.Integer(compute='_compute_best_price', store=True)


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'estate.estate.type'

    name = fields.Char(required=True)


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'estate.estate.tag'

    name = fields.Char(required=True)


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'estate.estate.offer'

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for record in self:
            if record.create_date and record.validity:
                create_date = fields.Datetime.from_string(record.create_date)
                record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                create_date = fields.Datetime.from_string(record.create_date)
                record.validity = (record.date_deadline - create_date.date()).days

    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one('res.partner', ondelete='set null', string='Partner', require=True)
    property_id = fields.Many2one('estate.property', ondelete='cascade', string='Property', require=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline')
