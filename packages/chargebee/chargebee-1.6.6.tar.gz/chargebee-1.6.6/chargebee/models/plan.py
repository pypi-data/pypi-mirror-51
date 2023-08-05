import json
from chargebee.model import Model
from chargebee import request
from chargebee import APIError

class Plan(Model):

    fields = ["id", "name", "invoice_name", "description", "price", "period", "period_unit", \
    "trial_period", "trial_period_unit", "charge_model", "free_quantity", "setup_cost", "downgrade_penalty", \
    "status", "archived_at", "billing_cycles", "redirect_url", "enabled_in_hosted_pages", "enabled_in_portal", \
    "invoice_notes", "taxable", "meta_data"]


    @staticmethod
    def create(params, env=None, headers=None):
        return request.send('post', request.uri_path("plans"), params, env, headers)

    @staticmethod
    def update(id, params=None, env=None, headers=None):
        return request.send('post', request.uri_path("plans",id), params, env, headers)

    @staticmethod
    def list(params=None, env=None, headers=None):
        return request.send('get', request.uri_path("plans"), params, env, headers)

    @staticmethod
    def retrieve(id, env=None, headers=None):
        return request.send('get', request.uri_path("plans",id), None, env, headers)

    @staticmethod
    def delete(id, env=None, headers=None):
        return request.send('post', request.uri_path("plans",id,"delete"), None, env, headers)
