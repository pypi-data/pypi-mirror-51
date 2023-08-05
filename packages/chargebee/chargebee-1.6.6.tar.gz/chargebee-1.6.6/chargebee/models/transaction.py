import json
from chargebee.model import Model
from chargebee import request
from chargebee import APIError

class Transaction(Model):
    class LinkedInvoice(Model):
      fields = ["invoice_id", "applied_amount", "applied_at", "invoice_date", "invoice_amount"]
      pass
    class LinkedRefund(Model):
      fields = ["txn_id", "txn_status", "txn_date", "txn_amount"]
      pass

    fields = ["id", "customer_id", "subscription_id", "payment_method", "reference_number", \
    "gateway", "description", "type", "date", "currency_code", "amount", "id_at_gateway", "status", \
    "initiator_type", "three_d_secure", "error_code", "error_text", "voided_at", "void_description", \
    "amount_unused", "masked_card_number", "reference_transaction_id", "refunded_txn_id", "reversal_transaction_id", \
    "linked_invoices", "linked_refunds"]


    @staticmethod
    def list(params=None, env=None, headers=None):
        return request.send('get', request.uri_path("transactions"), params, env, headers)

    @staticmethod
    def transactions_for_customer(id, params=None, env=None, headers=None):
        return request.send('get', request.uri_path("customers",id,"transactions"), params, env, headers)

    @staticmethod
    def transactions_for_subscription(id, params=None, env=None, headers=None):
        return request.send('get', request.uri_path("subscriptions",id,"transactions"), params, env, headers)

    @staticmethod
    def transactions_for_invoice(id, params=None, env=None, headers=None):
        return request.send('get', request.uri_path("invoices",id,"transactions"), params, env, headers)

    @staticmethod
    def retrieve(id, env=None, headers=None):
        return request.send('get', request.uri_path("transactions",id), None, env, headers)

    @staticmethod
    def record_payment(id, params, env=None, headers=None):
        return request.send('post', request.uri_path("invoices",id,"record_payment"), params, env, headers)
