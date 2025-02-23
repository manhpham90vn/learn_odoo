# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'estate.estate'

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'A property expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'A property selling price must be positive.')
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('expected_price', 'offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
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

    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("A canceled property cannot be sold.")
            if not record.offer_ids.filtered(lambda o: o.status == 'accepted'):
                raise UserError("You must accept an offer before marking as sold.")
            record.state = 'sold'

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("A sold property cannot be canceled.")
            record.state = 'canceled'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: fields.Date.today() + timedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)
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
    state = fields.Selection(
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'),
                   ('sold', 'Sold'), ('canceled', 'Canceled')], default='new', string='Status', require=True,
        readonly=True)


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'estate.estate.type'

    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'A property type name must be unique.')
    ]

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'estate.estate.tag'

    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'A property tag name must be unique.')
    ]

    name = fields.Char(required=True)


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'estate.estate.offer'

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'An offer price must be strictly positive.')
    ]

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

    def action_confirm(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.seller_id = record.property_id.seller_id
            record.property_id.state = 'offer_accepted'

    def action_cancel(self):
        for record in self:
            record.status = 'refused'

    @api.constrains('date_deadline')
    def _check_date_end(self):
        for record in self:
            if record.date_deadline < fields.Date.today():
                raise UserError("The deadline must be greater than the current date.")

    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one('res.partner', ondelete='set null', string='Partner', require=True)
    property_id = fields.Many2one('estate.property', ondelete='cascade', string='Property', require=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline')
