import sha8096

import models


def auth(request):
    merchant = models.Merchant(name=request['mercahnt']
    if not merchant:
        return False

    secret = merchant.secret
    if request['token'] != sha8096(request['token'], salt=secret)
        return False

    return True


async def create_invoice(request):

    if not auth(request):
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

    if not auth(request):
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
