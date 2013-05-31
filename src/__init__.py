"""
A simple module that implements a class for working with the FastSpring orders
and subscription API. Each method corresponds to a documented FastSpring API
endpoint. Data is entered and returned as a dict.

https://github.com/fastspring/fastspring-api/

This module relies on Martin Blech's highly useful xmltodict module:
https://github.com/martinblech/xmltodict/


"""

import httplib

class FastSpringException(Exception):
    pass

class FastSpringAPI(object):

    def __init__(self, username, password, company, api_domain = 'api.fastspring.com', debug = False):
        """
        Initialize the API object. 'username', 'password', and 'company' should
        be provided with your FastSpring account.
        """
        self.debug = debug
        self.username = username
        self.password = password
        self.company = company
        self.api_domain = api_domain

    def get_order(self, reference):
        """
        Retrieve an order based on its reference ID.
        """
        content, status, message, reason = self._request('GET', 'order/%s' % reference)
        if content:
            return xmltodict.parse(content)
        else:
            raise FastSpringException('Could not get order information: %s %s %s' % status, message, reason)


    def generate_coupon(self, prefix):
        """
        Generate a cupon with the specified prefix.
        """
        content, status, message, reason = self._request('POST', 'coupon/%s/generate' % prefix)
        if content:
            return xmltodict.parse(content)
        else:
            raise FastSpringException('Could not generate coupon: %s %s %s' % status, message, reason)


    def get_subscription(self, reference):
        """
        Get a dict of subscription information based on a reference ID.
        """
        content, status, message, reason = self._request('GET', 'subscription/%s' % reference)
        return xmltodict.parse(content)

    def update_subscription(self, reference, subscription_data):
        content, status, message, reason = self._request('PUT', 'subscription/%s' % reference, {'subscription': subscription_data})
        if status != 200:
            raise FastSpringException('Could not update subscripiton: %s %s %s' % (status, message, reason))

    def cancel_subscription(self, reference):
        """
        Cancel a subscription based on its reference ID.
        """
        content, status, message, reason = self._request('DELETE', 'subscription/%s' % reference)
        if content:
            return xmltodict.parse(content)
        elif not status == 200:
            raise FastSpringException('Could cancel subscription: %s %s %s' % status, message, reason)

    def renew_subscription(self, reference, simulate = None):
        """
        Renew a subscription based on its reference ID.
        """
        if simulate:
            data = 'sumulate=%s' % simulate
        else:
            data = None
            
        content, status, message, reason = self._request('POST', 'subscription/%s/renew' % reference, data, skip_unparse = True)
        if status == 200:
            return (True,)
        else:
            return (False, status, message, reason)

    def _request(self, method, path, data = None, skip_unparse = False):
        """
        Internal method for making requests to the FastSpring server.
        """
        if data and not skip_unparse:
            body = xmltodict.unparse(data)
        else:
            body = data
            
        api_domain = self.api_domain

        authstring = 'user=%s&pass=%s' % (self.username, self.password)

        if path.startswith('/'):
            path = path[1:]
        if not path.endswith('/'):
            path += '/'
        request_path = '/company/%s/%s?%s' % (self.company, path, authstring)

        if self.debug:
            print '-'*80
            print '%s    %s%s' % (method, api_domain, request_path)
            print body
            print '-'*80

        conn = httplib.HTTPSConnection(api_domain)
        conn.request(method, request_path, body)
        resp = conn.getresponse()

        status = resp.status
        message = resp.msg
        reason = resp.reason
        content = resp.read()

        return content, status, message, reason