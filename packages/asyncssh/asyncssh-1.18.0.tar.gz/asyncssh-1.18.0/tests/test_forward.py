# Copyright (c) 2016-2018 by Ron Frederick <ronf@timeheart.net> and others.
#
# This program and the accompanying materials are made available under
# the terms of the Eclipse Public License v2.0 which accompanies this
# distribution and is available at:
#
#     http://www.eclipse.org/legal/epl-2.0/
#
# This program may also be made available under the following secondary
# licenses when the conditions for such availability set forth in the
# Eclipse Public License v2.0 are satisfied:
#
#    GNU General Public License, Version 2.0, or any later versions of
#    that license
#
# SPDX-License-Identifier: EPL-2.0 OR GPL-2.0-or-later
#
# Contributors:
#     Ron Frederick - initial implementation, API, and documentation

"""Unit tests for AsyncSSH forwarding API"""

import asyncio
import codecs
import os
import socket
import sys
import unittest

from unittest.mock import patch

import asyncssh
from asyncssh.packet import String, UInt32
from asyncssh.public_key import CERT_TYPE_USER
from asyncssh.socks import SOCKS5, SOCKS5_AUTH_NONE
from asyncssh.socks import SOCKS4_OK_RESPONSE, SOCKS5_OK_RESPONSE

from .server import Server, ServerTestCase
from .util import asynctest, echo, make_certificate


def _echo_non_async(stdin, stdout, stderr=None):
    """Non-async version of echo callback"""

    conn = stdin.get_extra_info('connection')
    conn.create_task(echo(stdin, stdout, stderr))


def _listener(orig_host, orig_port):
    """Handle a forwarded TCP/IP connection"""

    # pylint: disable=unused-argument

    return echo


def _listener_non_async(orig_host, orig_port):
    """Non-async version of handler for a forwarded TCP/IP connection"""

    # pylint: disable=unused-argument

    return _echo_non_async


def _unix_listener():
    """Handle a forwarded UNIX domain connection"""

    # pylint: disable=unused-argument

    return echo


def _unix_listener_non_async():
    """Non-async version of handler for a forwarded UNIX domain connection"""

    # pylint: disable=unused-argument

    return _echo_non_async


@asyncio.coroutine
def _pause(reader, writer):
    """Sleep to allow buffered data to build up and trigger a pause"""

    yield from asyncio.sleep(0.1)
    yield from reader.read()
    writer.close()


@asyncio.coroutine
def _async_runtime_error(reader, writer):
    """Raise a runtime error"""

    # pylint: disable=unused-argument

    raise RuntimeError('Async internal error')

class _ClientConn(asyncssh.SSHClientConnection):
    """Patched SSH client connection for unit testing"""

    @asyncio.coroutine
    def make_global_request(self, request, *args):
        """Send a global request and wait for the response"""

        return self._make_global_request(request, *args)


class _EchoPortListener(asyncssh.SSHListener):
    """A TCP listener which opens a connection that echoes data"""

    def __init__(self, conn):
        self._conn = conn

        conn.create_task(self._open_connection())

    @asyncio.coroutine
    def _open_connection(self):
        """Open a forwarded connection that echoes data"""

        yield from asyncio.sleep(0.1)
        reader, writer = yield from self._conn.open_connection('open', 65535)
        yield from echo(reader, writer)

    def close(self):
        """Stop listening for new connections"""

        pass

    @asyncio.coroutine
    def wait_closed(self):
        """Wait for the listener to close"""

        pass # pragma: no cover


class _EchoPathListener(asyncssh.SSHListener):
    """A UNIX domain listener which opens a connection that echoes data"""

    def __init__(self, conn):
        self._conn = conn

        conn.create_task(self._open_connection())

    @asyncio.coroutine
    def _open_connection(self):
        """Open a forwarded connection that echoes data"""

        yield from asyncio.sleep(0.1)
        reader, writer = yield from self._conn.open_unix_connection('open')
        yield from echo(reader, writer)

    def close(self):
        """Stop listening for new connections"""

        pass

    @asyncio.coroutine
    def wait_closed(self):
        """Wait for the listener to close"""

        pass # pragma: no cover


class _TCPConnectionServer(Server):
    """Server for testing direct and forwarded TCP connections"""

    def connection_requested(self, dest_host, dest_port, orig_host, orig_port):
        """Handle a request to create a new connection"""

        if dest_port == 1:
            return False
        elif dest_port == 7:
            return (self._conn.create_tcp_channel(), echo)
        elif dest_port == 8:
            return _pause
        elif dest_port == 9:
            self._conn.close()
            return (self._conn.create_tcp_channel(), echo)
        elif dest_port == 10:
            return _async_runtime_error
        else:
            return True

    def server_requested(self, listen_host, listen_port):
        """Handle a request to create a new socket listener"""

        if listen_host == 'open':
            return _EchoPortListener(self._conn)
        else:
            return listen_host != 'fail'


class _UNIXConnectionServer(Server):
    """Server for testing direct and forwarded UNIX domain connections"""

    def unix_connection_requested(self, dest_path):
        """Handle a request to create a new UNIX domain connection"""

        if dest_path == '':
            return True
        elif dest_path == '/echo':
            return (self._conn.create_unix_channel(), echo)
        else:
            return False

    def unix_server_requested(self, listen_path):
        """Handle a request to create a new UNIX domain listener"""

        if listen_path == 'open':
            return _EchoPathListener(self._conn)
        else:
            return listen_path != 'fail'


class _CheckForwarding(ServerTestCase):
    """Utility functions for AsyncSSH forwarding unit tests"""

    @asyncio.coroutine
    def _check_echo_line(self, reader, writer, delay=False, encoded=False):
        """Check if an input line is properly echoed back"""

        if delay:
            yield from asyncio.sleep(delay)

        line = str(id(self)) + '\n'

        if not encoded:
            line = line.encode('utf-8')

        writer.write(line)
        yield from writer.drain()

        result = yield from reader.readline()

        writer.close()

        self.assertEqual(line, result)

    @asyncio.coroutine
    def _check_echo_block(self, reader, writer):
        """Check if a block of data is properly echoed back"""

        data = 4 * [1025*1024*b'\0']

        writer.writelines(data)
        yield from writer.drain()
        writer.write_eof()

        result = yield from reader.read()

        yield from reader.channel.wait_closed()
        writer.close()

        self.assertEqual(b''.join(data), result)


class _TestTCPForwarding(_CheckForwarding):
    """Unit tests for AsyncSSH TCP connection forwarding"""

    @classmethod
    @asyncio.coroutine
    def start_server(cls):
        """Start an SSH server which supports TCP connection forwarding"""

        return (yield from cls.create_server(
            _TCPConnectionServer, authorized_client_keys='authorized_keys'))

    @asyncio.coroutine
    def _check_connection(self, conn, dest_host='', dest_port=7, **kwargs):
        """Open a connection and test if a block of data is echoed back"""

        reader, writer = yield from conn.open_connection(dest_host, dest_port,
                                                         *kwargs)

        yield from self._check_echo_block(reader, writer)

    @asyncio.coroutine
    def _check_local_connection(self, listen_port, delay=None):
        """Open a local connection and test if an input line is echoed back"""

        reader, writer = yield from asyncio.open_connection(None, listen_port)

        yield from self._check_echo_line(reader, writer, delay=delay)

    @asynctest
    def test_ssh_create_tunnel(self):
        """Test creating a tunneled SSH connection"""

        with (yield from self.connect()) as conn:
            conn2, _ = yield from conn.create_ssh_connection(
                None, self._server_addr, self._server_port)

            with conn2:
                yield from self._check_connection(conn2)

            yield from conn2.wait_closed()

        yield from conn.wait_closed()

    @asynctest
    def test_ssh_connect_tunnel(self):
        """Test connecting a tunneled SSH connection"""

        with (yield from self.connect()) as conn:
            with (yield from conn.connect_ssh(self._server_addr,
                                              self._server_port)) as conn2:
                yield from self._check_connection(conn2)

            yield from conn2.wait_closed()

        yield from conn.wait_closed()

    @asynctest
    def test_ssh_connect_reverse_tunnel(self):
        """Test creating a tunneled reverse direction SSH connection"""

        server2 = yield from self.listen_reverse()
        listen_port = server2.sockets[0].getsockname()[1]

        with (yield from self.connect()) as conn:
            with (yield from conn.connect_reverse_ssh('127.0.0.1', listen_port,
                                                      server_factory=Server,
                                                      server_host_keys=['skey'],
                                                      gss_host=None)) as conn2:
                pass

            yield from conn2.wait_closed()

        yield from conn.wait_closed()

        server2.close()
        yield from server2.wait_closed()

    @asynctest
    def test_ssh_listen_tunnel(self):
        """Test opening a tunneled SSH listener"""

        with (yield from self.connect()) as conn:
            server2 = yield from conn.listen_ssh(port=0, server_factory=Server,
                                                 server_host_keys=['skey'],
                                                 gss_host=None)
            listen_port = server2.get_port()

            with (yield from asyncssh.connect('127.0.0.1', listen_port,
                                              loop=self.loop, gss_host=None,
                                              known_hosts=(['skey.pub'],
                                                           [], []))) as conn2:
                pass

            yield from conn2.wait_closed()

            server2.close()
            yield from server2.wait_closed()

        yield from conn.wait_closed()

    @asynctest
    def test_ssh_listen_reverse_tunnel(self):
        """Test creating a tunneled reverse direction SSH connection"""

        with (yield from self.connect()) as conn:
            server2 = yield from conn.listen_reverse_ssh(
                port=0, loop=self.loop, gss_host=None,
                known_hosts=(['skey.pub'], [], []))
            listen_port = server2.get_port()

            with (yield from asyncssh.connect_reverse(
                '127.0.0.1', listen_port, server_factory=Server,
                loop=self.loop, gss_host=None,
                server_host_keys=['skey'])) as conn2:
                pass

            yield from conn2.wait_closed()

            server2.close()
            yield from server2.wait_closed()

        yield from conn.wait_closed()

    @asynctest
    def test_connection(self):
        """Test opening a remote connection"""

        with (yield from self.connect()) as conn:
            yield from self._check_connection(conn)

        yield from conn.wait_closed()

    @asynctest
    def test_connection_failure(self):
        """Test failure in opening a remote connection"""

        with (yield from self.connect()) as conn:
            with self.assertRaises(asyncssh.ChannelOpenError):
                yield from conn.open_connection('', 0)

        yield from conn.wait_closed()

    @asynctest
    def test_connection_rejected(self):
        """Test rejection in opening a remote connection"""

        with (yield from self.connect()) as conn:
            with self.assertRaises(asyncssh.ChannelOpenError):
                yield from conn.open_connection('fail', 0)

        yield from conn.wait_closed()

    @asynctest
    def test_connection_not_permitted(self):
        """Test permission denied in opening a remote connection"""

        ckey = asyncssh.read_private_key('ckey')
        cert = make_certificate('ssh-rsa-cert-v01@openssh.com',
                                CERT_TYPE_USER, ckey, ckey, ['ckey'],
                                extensions={'no-port-forwarding': ''})

        with (yield from self.connect(username='ckey',
                                      client_keys=[(ckey, cert)])) as conn:
            with self.assertRaises(asyncssh.ChannelOpenError):
                yield from conn.open_connection('', 7)

        yield from conn.wait_closed()

    @asynctest
    def test_connection_not_permitted_open(self):
        """Test open permission denied in opening a remote connection"""

        with (yield from self.connect(username='ckey',
                                      client_keys=['ckey'])) as conn:
            with self.assertRaises(asyncssh.ChannelOpenError):
                yield from conn.open_connection('fail', 7)

        yield from conn.wait_closed()

    @asynctest
    def test_connection_invalid_unicode(self):
        """Test opening a connection with invalid Unicode in host"""

        with (yield from self.connect()) as conn:
            with self.assertRaises(asyncssh.ChannelOpenError):
                yield from conn.open_connection(b'\xff', 0)

            yield from conn.wait_closed()

    @asynctest
    def test_server(self):
        """Test creating a remote listener"""

        with (yield from self.connect()) as conn:
            listener = yield from conn.start_server(_listener, '', 0)
            yield from self._check_local_connection(listener.get_port())
            listener.close()
            listener.close()
            yield from listener.wait_closed()
            listener.close()

        yield from conn.wait_closed()

    @asynctest
    def test_server_open(self):
        """Test creating a remote listener which uses open_connection"""

        def new_connection(reader, writer):
            """Handle a forwarded TCP/IP connection"""

            waiter.set_result((reader, writer))

        def handler_factory(orig_host, orig_port):
            """Handle all connections using new_connection"""

            # pylint: disable=unused-argument

            return new_connection

        with (yield from self.connect()) as conn:
            waiter = asyncio.Future(loop=self.loop)

            yield from conn.start_server(handler_factory, 'open', 0)

            reader, writer = yield from waiter
            yield from self._check_echo_line(reader, writer)

            # Clean up the listener during connection close

        yield from conn.wait_closed()

    @asynctest
    def test_server_non_async(self):
        """Test creating a remote listener using non-async handler"""

        with (yield from self.connect()) as conn:
            listener = yield from conn.start_server(_listener_non_async, '', 0)
            yield from self._check_local_connection(listener.get_port())
            listener.close()
            yield from listener.wait_closed()

        yield from conn.wait_closed()

    @asynctest
    def test_server_failure(self):
        """Test failure in creating a remote listener"""

        with (yield from self.connect()) as conn:
            listener = yield from conn.start_server(_listener, 'fail', 0)
            self.assertIsNone(listener)

        yield from conn.wait_closed()

    @asynctest
    def test_forward_local_port(self):
        """Test forwarding of a local port"""

        with (yield from self.connect()) as conn:
            listener = yield from conn.forward_local_port('', 0, '', 7)

            yield from self._check_local_connection(listener.get_port(),
                                                    delay=0.1)

            listener.close()
            yield from listener.wait_closed()

        yield from conn.wait_closed()

    @asynctest
    def test_forward_local_port_pause(self):
        """Test pause during forwarding of a local port"""

        with (yield from self.connect()) as conn:
            listener = yield from conn.forward_local_port('', 0, '', 8)
            listen_port = listener.get_port()

            reader, writer = yield from asyncio.open_connection(None,
                                                                listen_port)

            writer.write(4*1024*1024*b'\0')
            writer.write_eof()
            yield from reader.read()

            writer.close()
            listener.close()
            yield from listener.wait_closed()

        yield from conn.wait_closed()

    @asynctest
    def test_forward_local_port_failure(self):
        """Test failure in forwarding a local port"""

        with (yield from self.connect()) as conn:
            listener = yield from conn.forward_local_port('', 0, '', 65535)
            listen_port = listener.get_port()

            reader, writer = yield from asyncio.open_connection(None,
                                                                listen_port)

            self.assertEqual((yield from reader.read()), b'')

            writer.close()
            listener.close()
            yield from listener.wait_closed()

        yield from conn.wait_closed()

    @unittest.skipIf(sys.platform == 'win32',
                     'skip dual-stack tests on Windows')
    @asynctest
    def test_forward_bind_error_ipv4(self):
        """Test error binding a local forwarding port"""

        with (yield from self.connect()) as conn:
            listener = yield from conn.forward_local_port('0.0.0.0', 0,
                                                          '', 7)

            with self.assertRaises(OSError):
                yield from conn.forward_local_port(None, listener.get_port(),
                                                   '', 7)

            listener.close()
            yield from listener.wait_closed()

        yield from conn.wait_closed()

    @unittest.skipIf(sys.platform == 'win32',
                     'skip dual-stack tests on Windows')
    @asynctest
    def test_forward_bind_error_ipv6(self):
        """Test error binding a local forwarding port"""

        with (yield from self.connect()) as conn:
            listener = yield from conn.forward_local_port('::', 0, '', 7)

            with self.assertRaises(OSError):
                yield from conn.forward_local_port(None, listener.get_port(),
                                                   '', 7)

            listener.close()
            yield from listener.wait_closed()

        yield from conn.wait_closed()

    @asynctest
    def test_forward_connect_error(self):
        """Test error connecting a local forwarding port"""

        with (yield from self.connect()) as conn:
            listener = yield from conn.forward_local_port('', 0, '', 1)
            listen_port = listener.get_port()

            reader, writer = yield from asyncio.open_connection(None,
                                                                listen_port)

            self.assertEqual((yield from reader.read()), b'')

            writer.close()
            listener.close()
            yield from listener.wait_closed()

        yield from conn.wait_closed()

    @asynctest
    def test_forward_immediate_eof(self):
        """Test getting EOF before forwarded connection is fully open"""

        with (yield from self.connect()) as conn:
            listener = yield from conn.forward_local_port('', 0, '', 7)
            listen_port = listener.get_port()

            _, writer = yield from asyncio.open_connection(None,
                                                           listen_port)

            writer.close()
            yield from asyncio.sleep(0.1)

            listener.close()
            yield from listener.wait_closed()

        yield from conn.wait_closed()

    @asynctest
    def test_forward_remote_port(self):
        """Test forwarding of a remote port"""

        server = yield from asyncio.start_server(echo, None, 0,
                                                 family=socket.AF_INET)
        server_port = server.sockets[0].getsockname()[1]

        with (yield from self.connect()) as conn:
            listener = yield from conn.forward_remote_port('', 0, '',
                                                           server_port)

            yield from self._check_local_connection(listener.get_port())

            listener.close()
            yield from listener.wait_closed()

        yield from conn.wait_closed()

        server.close()
        yield from server.wait_closed()

    @asynctest
    def test_forward_remote_specific_port(self):
        """Test forwarding of a specific remote port"""

        server = yield from asyncio.start_server(echo, None, 0,
                                                 family=socket.AF_INET)
        server_port = server.sockets[0].getsockname()[1]

        sock = socket.socket()
        sock.bind(('', 0))
        remote_port = sock.getsockname()[1]
        sock.close()

        with (yield from self.connect()) as conn:
            listener = yield from conn.forward_remote_port('', remote_port,
                                                           '', server_port)

            yield from self._check_local_connection(listener.get_port())

            listener.close()
            yield from listener.wait_closed()

        yield from conn.wait_closed()

        server.close()
        yield from server.wait_closed()

    @asynctest
    def test_forward_remote_port_failure(self):
        """Test failure of forwarding a remote port"""

        with (yield from self.connect()) as conn:
            listener = yield from conn.forward_remote_port('', 65536, '', 0)

            self.assertIsNone(listener)

        yield from conn.wait_closed()

    @asynctest
    def test_forward_remote_port_not_permitted(self):
        """Test permission denied in forwarding of a remote port"""

        ckey = asyncssh.read_private_key('ckey')
        cert = make_certificate('ssh-rsa-cert-v01@openssh.com',
                                CERT_TYPE_USER, ckey, ckey, ['ckey'],
                                extensions={'no-port-forwarding': ''})

        with (yield from self.connect(username='ckey',
                                      client_keys=[(ckey, cert)])) as conn:
            listener = yield from conn.forward_remote_port('', 0, '', 0)

            self.assertIsNone(listener)

        yield from conn.wait_closed()

    @asynctest
    def test_forward_remote_port_invalid_unicode(self):
        """Test TCP/IP forwarding with invalid Unicode in host"""

        with (yield from self.connect()) as conn:
            listener = yield from conn.forward_remote_port(b'\xff', 0, '', 0)

            self.assertIsNone(listener)

        yield from conn.wait_closed()

    @asynctest
    def test_cancel_forward_remote_port_invalid_unicode(self):
        """Test canceling TCP/IP forwarding with invalid Unicode in host"""

        with patch('asyncssh.connection.SSHClientConnection', _ClientConn):
            with (yield from self.connect()) as conn:
                pkttype, _ = yield from conn.make_global_request(
                    b'cancel-tcpip-forward', String(b'\xff'), UInt32(0))

                self.assertEqual(pkttype, asyncssh.MSG_REQUEST_FAILURE)

            yield from conn.wait_closed()

    @asynctest
    def test_add_channel_after_close(self):
        """Test opening a connection after a close"""

        with (yield from self.connect()) as conn:
            with self.assertRaises(asyncssh.ChannelOpenError):
                yield from conn.open_connection('', 9)

        yield from conn.wait_closed()

    @asynctest
    def test_async_runtime_error(self):
        """Test runtime error in async listener"""

        with (yield from self.connect()) as conn:
            reader, _ = yield from conn.open_connection('', 10)
            with self.assertRaises(asyncssh.ConnectionLost):
                yield from reader.read()

        yield from conn.wait_closed()

    @asynctest
    def test_multiple_global_requests(self):
        """Test sending multiple global requests in parallel"""

        with (yield from self.connect()) as conn:
            listeners = yield from asyncio.gather(
                conn.forward_remote_port('', 0, '', 7),
                conn.forward_remote_port('', 0, '', 7))

            for listener in listeners:
                listener.close()
                yield from listener.wait_closed()

        yield from conn.wait_closed()


@unittest.skipIf(sys.platform == 'win32',
                 'skip UNIX domain socket tests on Windows')
class _TestUNIXForwarding(_CheckForwarding):
    """Unit tests for AsyncSSH UNIX connection forwarding"""

    @classmethod
    @asyncio.coroutine
    def start_server(cls):
        """Start an SSH server which supports UNIX connection forwarding"""

        return (yield from cls.create_server(
            _UNIXConnectionServer, authorized_client_keys='authorized_keys'))

    @asyncio.coroutine
    def _check_unix_connection(self, conn, dest_path='/echo', **kwargs):
        """Open a UNIX connection and test if an input line is echoed back"""

        reader, writer = yield from conn.open_unix_connection(dest_path,
                                                              encoding='utf-8',
                                                              *kwargs)

        yield from self._check_echo_line(reader, writer, encoded=True)

    @asyncio.coroutine
    def _check_local_unix_connection(self, listen_path):
        """Open a local connection and test if an input line is echoed back"""

        # pylint doesn't think open_unix_connection exists
        # pylint: disable=no-member
        reader, writer = yield from asyncio.open_unix_connection(listen_path)
        # pylint: enable=no-member

        yield from self._check_echo_line(reader, writer)

    @asynctest
    def test_unix_connection(self):
        """Test opening a remote UNIX connection"""

        with (yield from self.connect()) as conn:
            yield from self._check_unix_connection(conn)

        yield from conn.wait_closed()

    @asynctest
    def test_unix_connection_failure(self):
        """Test failure in opening a remote UNIX connection"""

        with (yield from self.connect()) as conn:
            with self.assertRaises(asyncssh.ChannelOpenError):
                yield from conn.open_unix_connection('')

        yield from conn.wait_closed()

    @asynctest
    def test_unix_connection_rejected(self):
        """Test rejection in opening a remote UNIX connection"""

        with (yield from self.connect()) as conn:
            with self.assertRaises(asyncssh.ChannelOpenError):
                yield from conn.open_unix_connection('/fail')

        yield from conn.wait_closed()

    @asynctest
    def test_unix_connection_not_permitted(self):
        """Test permission denied in opening a remote UNIX connection"""

        ckey = asyncssh.read_private_key('ckey')
        cert = make_certificate('ssh-rsa-cert-v01@openssh.com',
                                CERT_TYPE_USER, ckey, ckey, ['ckey'],
                                extensions={'no-port-forwarding': ''})

        with (yield from self.connect(username='ckey',
                                      client_keys=[(ckey, cert)])) as conn:
            with self.assertRaises(asyncssh.ChannelOpenError):
                yield from conn.open_unix_connection('/echo')

        yield from conn.wait_closed()

    @asynctest
    def test_unix_connection_invalid_unicode(self):
        """Test opening a UNIX connection with invalid Unicode in path"""

        with (yield from self.connect()) as conn:
            with self.assertRaises(asyncssh.ChannelOpenError):
                yield from conn.open_unix_connection(b'\xff')

            yield from conn.wait_closed()

    @asynctest
    def test_unix_server(self):
        """Test creating a remote UNIX listener"""

        path = os.path.abspath('echo')

        with (yield from self.connect()) as conn:
            listener = yield from conn.start_unix_server(_unix_listener, path)
            yield from self._check_local_unix_connection('echo')
            listener.close()
            listener.close()
            yield from listener.wait_closed()
            listener.close()

        yield from conn.wait_closed()

        os.remove('echo')

    @asynctest
    def test_unix_server_open(self):
        """Test creating a UNIX listener which uses open_unix_connection"""

        def new_connection(reader, writer):
            """Handle a forwarded UNIX domain connection"""

            waiter.set_result((reader, writer))

        def handler_factory():
            """Handle all connections using new_connection"""

            # pylint: disable=unused-argument

            return new_connection

        with (yield from self.connect()) as conn:
            waiter = asyncio.Future(loop=self.loop)

            listener = yield from conn.start_unix_server(handler_factory,
                                                         'open')

            reader, writer = yield from waiter
            yield from self._check_echo_line(reader, writer)

            listener.close()
            yield from listener.wait_closed()

        yield from conn.wait_closed()

    @asynctest
    def test_unix_server_non_async(self):
        """Test creating a remote UNIX listener using non-async handler"""

        path = os.path.abspath('echo')

        with (yield from self.connect()) as conn:
            listener = yield from conn.start_unix_server(
                _unix_listener_non_async, path)
            yield from self._check_local_unix_connection('echo')
            listener.close()
            yield from listener.wait_closed()

        yield from conn.wait_closed()

        os.remove('echo')

    @asynctest
    def test_unix_server_failure(self):
        """Test failure in creating a remote UNIX listener"""

        with (yield from self.connect()) as conn:
            listener = yield from conn.start_unix_server(_unix_listener,
                                                         'fail')
            self.assertIsNone(listener)

        yield from conn.wait_closed()

    @asynctest
    def test_forward_local_path(self):
        """Test forwarding of a local UNIX domain path"""

        with (yield from self.connect()) as conn:
            listener = yield from conn.forward_local_path('local', '/echo')

            yield from self._check_local_unix_connection('local')

            listener.close()
            yield from listener.wait_closed()

        yield from conn.wait_closed()

        os.remove('local')

    @asynctest
    def test_forward_remote_path(self):
        """Test forwarding of a remote UNIX domain path"""

        # pylint doesn't think start_unix_server exists
        # pylint: disable=no-member
        server = yield from asyncio.start_unix_server(echo, 'local')
        # pylint: enable=no-member

        path = os.path.abspath('echo')

        with (yield from self.connect()) as conn:
            listener = yield from conn.forward_remote_path(path, 'local')

            yield from self._check_local_unix_connection('echo')

            listener.close()
            yield from listener.wait_closed()

        yield from conn.wait_closed()

        server.close()
        yield from server.wait_closed()

        os.remove('echo')
        os.remove('local')

    @asynctest
    def test_forward_remote_path_failure(self):
        """Test failure of forwarding a remote UNIX domain path"""

        open('echo', 'w').close()

        path = os.path.abspath('echo')

        with (yield from self.connect()) as conn:
            listener = yield from conn.forward_remote_path(path, 'local')

            self.assertIsNone(listener)

        yield from conn.wait_closed()

        os.remove('echo')

    @asynctest
    def test_forward_remote_path_not_permitted(self):
        """Test permission denied in forwarding a remote UNIX domain path"""

        ckey = asyncssh.read_private_key('ckey')
        cert = make_certificate('ssh-rsa-cert-v01@openssh.com',
                                CERT_TYPE_USER, ckey, ckey, ['ckey'],
                                extensions={'no-port-forwarding': ''})

        with (yield from self.connect(username='ckey',
                                      client_keys=[(ckey, cert)])) as conn:
            listener = yield from conn.forward_remote_path('', 'local')

            self.assertIsNone(listener)

        yield from conn.wait_closed()

    @asynctest
    def test_forward_remote_path_invalid_unicode(self):
        """Test forwarding a UNIX domain path with invalid Unicode in it"""

        with (yield from self.connect()) as conn:
            listener = yield from conn.forward_remote_path(b'\xff', 'local')

            self.assertIsNone(listener)

        yield from conn.wait_closed()

    @asynctest
    def test_cancel_forward_remote_path_invalid_unicode(self):
        """Test canceling UNIX forwarding with invalid Unicode in path"""

        with patch('asyncssh.connection.SSHClientConnection', _ClientConn):
            with (yield from self.connect()) as conn:
                pkttype, _ = yield from conn.make_global_request(
                    b'cancel-streamlocal-forward@openssh.com', String(b'\xff'))

                self.assertEqual(pkttype, asyncssh.MSG_REQUEST_FAILURE)

            yield from conn.wait_closed()


class _TestSOCKSForwarding(_CheckForwarding):
    """Unit tests for AsyncSSH SOCKS dynamic port forwarding"""

    @classmethod
    @asyncio.coroutine
    def start_server(cls):
        """Start an SSH server which supports TCP connection forwarding"""

        return (yield from cls.create_server(
            _TCPConnectionServer, authorized_client_keys='authorized_keys'))

    @asyncio.coroutine
    def _check_early_error(self, reader, writer, data):
        """Check errors in the initial SOCKS message"""

        writer.write(data)

        self.assertEqual((yield from reader.read()), b'')

    @asyncio.coroutine
    def _check_socks5_error(self, reader, writer, data):
        """Check SOCKSv5 errors after auth"""

        writer.write(bytes((SOCKS5, 1, SOCKS5_AUTH_NONE)))
        self.assertEqual((yield from reader.readexactly(2)),
                         bytes((SOCKS5, SOCKS5_AUTH_NONE)))

        writer.write(data)

        self.assertEqual((yield from reader.read()), b'')

    @asyncio.coroutine
    def _check_socks4_connect(self, reader, writer, data, result):
        """Check SOCKSv4 connect requests"""

        writer.write(data)

        response = yield from reader.readexactly(len(SOCKS4_OK_RESPONSE))
        self.assertEqual(response, SOCKS4_OK_RESPONSE)

        if result:
            yield from self._check_echo_line(reader, writer)
        else:
            self.assertEqual((yield from reader.read()), b'')

    @asyncio.coroutine
    def _check_socks5_connect(self, reader, writer, data, result):
        """Check SOCKSv5 connect_requests"""

        writer.write(bytes((SOCKS5, 1, SOCKS5_AUTH_NONE)))
        self.assertEqual((yield from reader.readexactly(2)),
                         bytes((SOCKS5, SOCKS5_AUTH_NONE)))

        writer.write(data[:20])
        yield from asyncio.sleep(0.1)
        writer.write(data[20:])

        response = yield from reader.readexactly(len(SOCKS5_OK_RESPONSE))
        self.assertEqual(response, SOCKS5_OK_RESPONSE)

        if result:
            yield from self._check_echo_line(reader, writer)
        else:
            self.assertEqual((yield from reader.read()), b'')

    @asyncio.coroutine
    def _check_socks(self, handler, listen_port, msg, data, *args):
        """Unit test SOCKS dynamic port forwarding"""

        with self.subTest(msg=msg, data=data):
            data = codecs.decode(data, 'hex')

            reader, writer = \
                yield from asyncio.open_connection(None, listen_port)

            try:
                yield from handler(reader, writer, data, *args)
            finally:
                writer.close()

    @asynctest
    def test_forward_socks(self):
        """Test dynamic port forwarding via SOCKS"""

        # pylint: disable=bad-whitespace

        _socks_early_errors = [
            ('Bad version',               '0000'),
            ('Bad SOCKSv4 command',       '0400'),
            ('Bad SOCKSv4 Unicode data',  '040100010000000100ff00'),
            ('SOCKSv4 hostname too long', '040100010000000100' + 256 * 'ff'),
            ('Bad SOCKSv5 auth list',     '050101')
        ]

        _socks5_postauth_errors = [
            ('Bad command',      '05000001'),
            ('Bad address',      '05010000'),
            ('Bad Unicode data', '0501000301ff0007')
        ]

        _socks4_connects = [
            ('IPv4',          '040100077f00000100',                     True),
            ('Hostname',      '0401000700000001006c6f63616c686f737400', True),
            ('Rejected',      '04010001000000010000',                   False)
        ]

        _socks5_connects = [
            ('IPv4',        '050100017f0000010007',             True),
            ('Hostname',    '05010003096c6f63616c686f73740007', True),
            ('IPv6',        '05010004' + 15*'00' + '010007',    True),
            ('Rejected',    '05010003000001',                   False)
        ]

        # pylint: enable=bad-whitespace

        with (yield from self.connect()) as conn:
            listener = yield from conn.forward_socks('', 0)
            listen_port = listener.get_port()

            for msg, data in _socks_early_errors:
                yield from self._check_socks(self._check_early_error,
                                             listen_port, msg, data)

            for msg, data in _socks5_postauth_errors:
                yield from self._check_socks(self._check_socks5_error,
                                             listen_port, msg, data)

            for msg, data, result in _socks4_connects:
                yield from self._check_socks(self._check_socks4_connect,
                                             listen_port, msg, data, result)

            for msg, data, result in _socks5_connects:
                yield from self._check_socks(self._check_socks5_connect,
                                             listen_port, msg, data, result)

            listener.close()
            yield from listener.wait_closed()

        yield from conn.wait_closed()

    @unittest.skipIf(sys.platform == 'win32',
                     'Avoid issue with SO_REUSEADDR on Windows')
    @asynctest
    def test_forward_bind_error_socks(self):
        """Test error binding a local dynamic forwarding port"""

        with (yield from self.connect()) as conn:
            listener = yield from conn.forward_socks(None, 0)

            with self.assertRaises(OSError):
                yield from conn.forward_socks(None, listener.get_port())

            listener.close()
            yield from listener.wait_closed()

        yield from conn.wait_closed()
