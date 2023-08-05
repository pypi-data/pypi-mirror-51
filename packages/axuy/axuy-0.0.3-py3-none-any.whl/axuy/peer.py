# peer.py - peer main loop
# Copyright (C) 2019  Nguyễn Gia Phong
#
# This file is part of Axuy
#
# Axuy is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Axuy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Axuy.  If not, see <https://www.gnu.org/licenses/>.

__version__ = '0.0.3'
__doc__ = 'Axuy main loop'

from argparse import ArgumentParser, RawTextHelpFormatter
from pickle import dumps, loads
from socket import socket, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
from threading import Event, RLock, Thread

from .misc import mapgen, mapidgen, whilst
from .pico import Picobot
from .view import ConfigReader, View


class Peer:
    """Axuy peer.
    TODO: Documentation
    """

    def __init__(self, config):
        if config.seeder is None:
            mapid = mapidgen()
            self.peers = []
        else:
            client = socket()
            host, port = config.seeder.split(':')
            self.peers = [(host, int(port))]
            client.connect(*self.peers)
            data = loads(client.recv(1024))
            mapid = data['mapid']
            self.peers.extend(data['peers'])

        self.updated, lock = Event(), RLock()
        self.addr = config.host, config.port
        self.space = mapgen(mapid)
        self.pico = Picobot(self.addr, self.space)
        self.view = View(self.addr, self.pico, self.space, config, lock)

        Thread(target=self.serve, args=(mapid,), daemon=True).start()

        self.sock = socket(type=SOCK_DGRAM)   # UDP
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind(self.addr)

        Thread(target=self.push, daemon=True).start()
        Thread(target=self.pull, args=(lock,), daemon=True).start()

    def serve(self, mapid):
        """Initiate peers."""
        with socket() as server:    # TCP server
            server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            server.bind(self.addr)
            server.listen(7)
            print('Axuy is listening at {}:{}'.format(*server.getsockname()))
            while True:
                conn, addr = server.accept()
                conn.send(dumps({'mapid': mapid, 'peers': self.peers}))
                conn.close()

    @whilst
    def push(self):
        """Send own state to peers."""
        self.updated.wait()
        shards = {i: (s.pos, s.rot, s.power)
                  for i, s in self.pico.shards.items()}
        data = dumps([self.pico.pos, self.pico.rot, shards])
        for peer in self.peers:
            self.sock.sendto(data, peer)
        self.updated.clear()

    @whilst
    def pull(self, lock):
        """Receive peers' state."""
        data, addr = self.sock.recvfrom(1<<16)
        pos, rot, shards = loads(data)
        with lock:
            if addr not in self.view.picos:
                self.peers.append(addr)
                self.view.add_pico(addr, pos, rot)
            self.view.picos[addr].sync(pos, rot, shards)

    def update(self):
        """Locally update the internal states."""
        self.view.update()
        self.updated.set()

    def __enter__(self): return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.sock.close()
        self.view.close()


def main():
    """Parse arguments and start main loop."""
    # Read configuration files
    config = ConfigReader()
    config.parse()

    # Parse command-line arguments
    parser = ArgumentParser(usage='%(prog)s [options]',
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument('-v', '--version', action='version',
                        version='Axuy {}'.format(__version__))
    parser.add_argument(
        '--host',
        help='host to bind this peer to (fallback: {})'.format(config.host))
    parser.add_argument(
        '--port', type=int,
        help='port to bind this peer to (fallback: {})'.format(config.port))
    parser.add_argument('--seeder',
                        help='address of the peer that created the map')
    # All these options specific for a graphical peer need to be modularized.
    parser.add_argument(
        '-s', '--size', type=int, nargs=2, metavar=('X', 'Y'),
        help='the desired screen size (fallback: {}x{})'.format(*config.size))
    parser.add_argument(
        '--vsync', action='store_true', default=None,
        help='enable vertical synchronization (fallback: {})'.format(
            config.vsync))
    parser.add_argument('--no-vsync', action='store_false', dest='vsync',
                        help='disable vertical synchronization')
    parser.add_argument(
        '--fov', type=float,
        help='horizontal field of view (fallback: {:.1f})'.format(config.fov))
    parser.add_argument(
        '--mouse-speed', type=float, dest='mouspeed',
        help='camera rotational speed (fallback: {:.1f})'.format(
            config._mouspeed))
    parser.add_argument(
        '--zoom-speed', type=float, dest='zmspeed',
        help='zoom speed (fallback: {:.1f})'.format(config.zmspeed))
    args = parser.parse_args()
    config.read_args(args)

    with Peer(config) as peer:
        while peer.view.is_running: peer.update()
