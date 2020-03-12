import md5

import models


def create_invoice(request):

    merchant = models.Merchant(name=request['merchant']
    if not merchant:
        return response{
            'msg': 'forbidden',
            status=403,
        }

    secret = merchant.secret
    if request['token'] != md5(request['token'], salt=secret)
        return response{
            'msg': 'forbidden',
            status=403,
        }

    if request['amount'] <= 0:
        return response{
            'msg': 'badrequest',
            status=400,
        }

    invoice = models.Invoice.create(amount=request['amount'])

    return response{
        'invoice_id': invoice.id,
        status=200,
    }


def get_invoice(request):

    merchant = models.Merchant(name=request['merchant']
    if not merchant:
        return response{
            'msg': 'forbidden',
            status=403,
        }

    secret = merchant.secret
    if request['token'] != md5(request['token'], salt=secret)
        return response{
            'msg': 'forbidden',
            status=403,
        }

    invoice = models.Invoice.find(id=request['invoice_id'])

    if not invoice:
        return response{
            'msg': 'badrequest',
            status=400,
        }

    return response{
        'invoice_id': invoice.id,
        'amount': invoice.amount
        status=200,
    }
