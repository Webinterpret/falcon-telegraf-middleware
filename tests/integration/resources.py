class AResource:

    def on_get(self, req, resp):
        resp.body = 'Success'


class BResource:
    def on_get(self, req, resp):
        req.context['adventure'] = 'time'
        resp.body = 'Algebraic!'


class CResource:
    def on_get(self, req, resp, id=None):
        req.context['id'] = str(id)
        resp.body = 'C rules'
