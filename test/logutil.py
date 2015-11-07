# -*- Mode: Python; py-indent-offset: 4 -*-
# vim: tabstop=4 shiftwidth=4 expandtab
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

import sys

import logging

logger = logging.getLogger(__name__)

class StreamCapture(object):

    def __init__(self, prefix=''):
        self.prefix = prefix
        self.data = ''

    def write(self, data):
        
        self.data += str(data).strip('\r')
        
        if not '\n' in self.data:
            return
        
        for s in self.data.splitlines(True):
            if s[-1] == '\n':
                logger.info('%s %s' % (self.prefix, s.rstrip('\n')))
                self.data = '' # maybe done more than once
            else:
                self.data = s # this assume the last iteration without \n

if __name__ == "__main__":
    
    logging.basicConfig(format='[%(asctime)s] (%(threadName)s) %(levelname)s %(name)s:%(lineno)d %(funcName)s %(message)s', 
                        level=logging.DEBUG)

    sys.stderr = StreamCapture('[stderr]')
 
    sys.stderr.write('foo\n')
    sys.stderr.write('bar\n')

    sys.stderr = StreamCapture('[stderr]')
 
    sys.stderr.write('foo')
    sys.stderr.write('\nbar\nhello')
    sys.stderr.write(' world\n')
    sys.stderr.write('')
    sys.stderr.write('\n')