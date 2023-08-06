# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from tuir.clipboard import copy
from tuir.exceptions import ProgramError


try:
    from unittest import mock
except ImportError:
    import mock


def test_copy():

    with mock.patch('subprocess.Popen') as Popen, \
            mock.patch('subprocess.call', return_value=0) as call:

        # Mock out the subprocess calls
        p = mock.Mock()
        p.communicate = mock.Mock()
        
        Popen.return_value = p

        copy('test', 'xsel -b -i')
        assert Popen.call_args[0][0] == ['xsel', '-b', '-i']
        p.communicate.assert_called_with(input='test'.encode('utf-8'))

        copy('test ❤', 'xclip')
        assert Popen.call_args[0][0] == ['xclip']
        p.communicate.assert_called_with(input='test ❤'.encode('utf-8'))

    with mock.patch('subprocess.Popen') as Popen, \
            mock.patch('subprocess.call', return_value=0) as call:

        # Simulate OSX
        mock.patch('sys.platform', return_value='darwin')
        
        p = mock.Mock()
        p.communicate = mock.Mock()
        Popen.return_value = p

        copy('test', 'pbcopy w')
        assert Popen.call_args[0][0] == ['pbcopy', 'w']
        p.communicate.assert_called_with(input='test'.encode('utf-8'))
