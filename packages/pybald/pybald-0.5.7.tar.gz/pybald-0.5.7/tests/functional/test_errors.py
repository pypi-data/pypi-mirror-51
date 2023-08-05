import unittest
from webob import Request
import pybald
from pybald import context
from pybald.core.router import Router
from pybald.core.controllers import Controller, action
from pybald.core.middleware.errors import ErrorMiddleware

import logging
log = logging.getLogger(__name__)

not_found_response = '404 Not Found\n\nThe resource could not be found.\n\n No URL match  '
stack_trace_head = '''<html>\n<head>\n    <title>Pybald Runtime Error</title>\n'''
general_fault_response = '500 Internal Server Error\n\nThe server has either erred or is incapable of performing the requested operation.\n\n General Fault  '


def map(urls):
    # errors
    urls.connect('throw_exception', r'/throw_exception', controller='sample',
                 action='throw_exception')


class SampleController(Controller):
    @action
    def index(self, req):
        self.sample_variable = "Testing"

    @action
    def throw_exception(self, req):
        raise Exception("This is a test exception")


test_conf = dict(database_engine_uri='sqlite:///:memory:',
                 env_name="SampleTestProjectEnvironment",
                 debug=True)


class TestErrors(unittest.TestCase):
    def setUp(self):
        context._reset()

    def tearDown(self):
        context._reset()

    def test_stack_trace(self):
        "When in debug mode, throw an Exception and generate a stack trace"
        pybald.configure(config_object=test_conf)
        app = Router(routes=map, controllers=[SampleController])
        app = ErrorMiddleware(app)

        try:
            resp = Request.blank('/throw_exception').get_response(app)
        except Exception as err:
            self.fail("Exception Generated or Fell Through Error Handler {0}".format(err))
        self.assertEqual(resp.status_code, 500)
        self.assertEqual(stack_trace_head, str(resp.text)[:len(stack_trace_head)])

    def test_non_stack_trace(self):
        "When *NOT* in debug mode, throw an Exception and return a generic error"
        test_w_debug_conf = test_conf.copy()
        test_w_debug_conf.update(dict(debug=False))
        pybald.configure(config_object=test_w_debug_conf)
        app = Router(routes=map, controllers=[SampleController])
        app = ErrorMiddleware(app)
        try:
            resp = Request.blank('/throw_exception').get_response(app)
        except Exception as err:
            self.fail("Exception Generated or Fell Through Error Handler {0}".format(err))
        self.assertEqual(resp.status_code, 500)
        self.assertEqual(str(resp.text), general_fault_response)

    def test_404(self):
        "Return a 404 response"
        pybald.configure(config_object=test_conf)
        app = Router(routes=map, controllers=[SampleController])
        app = ErrorMiddleware(app)
        try:
            resp = Request.blank('/not_there').get_response(app)
        except Exception as err:
            self.fail("Exception Generated or Fell Through Error Handler {0}".format(err))
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(str(resp.text), not_found_response)


if __name__ == "__main__":
    unittest.main()
