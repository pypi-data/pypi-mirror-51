import unittest

from ..framework import cli_test_suite
from .util import DEFAULT_MANAGEMENT_KEY


@cli_test_suite
def additional_tests(ykman_cli):
    class Misc(unittest.TestCase):

        def setUp(self):
            ykman_cli('piv', 'reset', '-f')

        def test_info(self):
            output = ykman_cli('piv', 'info')
            self.assertIn('PIV version:', output)

        def test_reset(self):
            output = ykman_cli('piv', 'reset', '-f')
            self.assertIn('Success!', output)

        def test_write_read_object(self):
            ykman_cli(
                'piv', 'write-object',
                '-m', DEFAULT_MANAGEMENT_KEY, '0x5f0001',
                '-', input='test data')
            output = ykman_cli('piv', 'read-object', '0x5f0001')
            self.assertEquals('test data\n', output)

    return [Misc]
