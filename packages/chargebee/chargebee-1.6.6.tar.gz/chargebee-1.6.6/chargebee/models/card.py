import json
from chargebee.model import Model
from chargebee import request
from chargebee import APIError

class Card(Model):

    fields = ["status", "gateway", "reference_id", "first_name", "last_name", "iin", "last4", \
    "card_type", "expiry_month", "expiry_year", "billing_addr1", "billing_addr2", "billing_city", \
    "billing_state_code", "billing_state", "billing_country", "billing_zip", "ip_address", "customer_id", \
    "masked_number"]


    @staticmethod
    def retrieve(id, env=None, headers=None):
        return request.send('get', request.uri_path("cards",id), None, env, headers)

    @staticmethod
    def update_card_for_customer(id, params, env=None, headers=None):
        return request.send('post', request.uri_path("customers",id,"credit_card"), params, env, headers)

    @staticmethod
    def update_card_for_customer_using_payment_intent(id, params=None, env=None, headers=None):
        return request.send('post', request.uri_path("customers",id,"credit_card_using_payment_intent"), params, env, headers)

    @staticmethod
    def switch_gateway_for_customer(id, params, env=None, headers=None):
        return request.send('post', request.uri_path("customers",id,"switch_gateway"), params, env, headers)

    @staticmethod
    def delete_card_for_customer(id, env=None, headers=None):
        return request.send('post', request.uri_path("customers",id,"delete_card"), None, env, headers)
