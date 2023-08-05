from chargebee.compat import json
from chargebee.models import *


class Result(object):

    def __init__(self, response):
        self._response = response
        self._response_obj = {}

    @property
    def subscription(self):
        return self._get('subscription', Subscription,
        {'addons' : Subscription.Addon, 'coupons' : Subscription.Coupon, 'shipping_address' : Subscription.ShippingAddress});

    @property
    def customer(self):
        return self._get('customer', Customer,
        {'billing_address' : Customer.BillingAddress, 'contacts' : Customer.Contact, 'payment_method' : Customer.PaymentMethod});

    @property
    def card(self):
        return self._get('card', Card);

    @property
    def invoice(self):
        return self._get('invoice', Invoice,
        {'line_items' : Invoice.LineItem, 'discounts' : Invoice.Discount, 'taxes' : Invoice.Tax, 'linked_transactions' : Invoice.LinkedTransaction, 'linked_orders' : Invoice.LinkedOrder, 'notes' : Invoice.Note, 'shipping_address' : Invoice.ShippingAddress, 'billing_address' : Invoice.BillingAddress});

    @property
    def order(self):
        return self._get('order', Order);

    @property
    def transaction(self):
        return self._get('transaction', Transaction,
        {'linked_invoices' : Transaction.LinkedInvoice, 'linked_refunds' : Transaction.LinkedRefund});

    @property
    def hosted_page(self):
        return self._get('hosted_page', HostedPage);

    @property
    def estimate(self):
        return self._get('estimate', Estimate,
        {'line_items' : Estimate.LineItem, 'discounts' : Estimate.Discount, 'taxes' : Estimate.Tax});

    @property
    def plan(self):
        return self._get('plan', Plan);

    @property
    def addon(self):
        return self._get('addon', Addon);

    @property
    def coupon(self):
        return self._get('coupon', Coupon);

    @property
    def coupon_code(self):
        return self._get('coupon_code', CouponCode);

    @property
    def address(self):
        return self._get('address', Address);

    @property
    def event(self):
        return self._get('event', Event,
        {'webhooks' : Event.Webhook});

    @property
    def comment(self):
        return self._get('comment', Comment);

    @property
    def download(self):
        return self._get('download', Download);

    @property
    def portal_session(self):
        return self._get('portal_session', PortalSession,
        {'linked_customers' : PortalSession.LinkedCustomer});

    @property
    def payment_intent(self):
        return self._get('payment_intent', PaymentIntent,
        {'payment_attempt' : PaymentIntent.PaymentAttempt});



    def _get(self, type, cls, sub_types=None):
        if not type in self._response:
            return None

        if not type in self._response_obj:
            self._response_obj[type] = cls.construct(self._response[type], sub_types)

        return self._response_obj[type]

    def __str__(self):
        return json.dumps(self._response, indent=4)


class Content(Result):
    pass
