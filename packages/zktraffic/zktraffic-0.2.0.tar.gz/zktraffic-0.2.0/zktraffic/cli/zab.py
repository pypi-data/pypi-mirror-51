# ==================================================================================================
# Copyright 2015 Twitter, Inc.
# --------------------------------------------------------------------------------------------------
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this work except in compliance with the License.
# You may obtain a copy of the License in the LICENSE file, or at:
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==================================================================================================

import sys

from .printer import Printer

from zktraffic import __version__
from zktraffic.network.sniffer import Sniffer
from zktraffic.zab.quorum_packet import (
  Ping,
  QuorumPacket
)

from twitter.common import app
from twitter.common.log.options import LogOptions


def setup():
  LogOptions.set_stderr_log_level('NONE')

  app.add_option('--iface', default='eth0', type=str,
                 help='The interface to sniff on')
  app.add_option('--port', default=2889, type=int,
                 help='The ZAB port used by the leader')
  app.add_option('-c', '--colors', default=False, action='store_true',
                 help='Color each learner/leader stream differently')
  app.add_option('--dump-bad-packet', default=False, action='store_true',
                 help='Dump packets that cannot be deserialized')
  app.add_option('--include-pings', default=False, action='store_true',
                 help='Whether to include pings send from learners to the leader')
  app.add_option('--version', default=False, action='store_true')


def main(_, options):
  if options.version:
    sys.stdout.write("%s\n" % __version__)
    sys.exit(0)

  skip = None if options.include_pings else lambda msg: isinstance(msg, Ping)
  printer = Printer(options.colors, output=sys.stdout, skip_print=skip)
  sniffer = Sniffer(options.iface, options.port, QuorumPacket, printer.add, options.dump_bad_packet)

  try:
    while printer.isAlive():
      sniffer.join(1)
  except (KeyboardInterrupt, SystemExit):
    pass


if __name__ == '__main__':
  setup()
  app.main()
