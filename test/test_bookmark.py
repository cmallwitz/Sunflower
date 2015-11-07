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

import inspect
import logging

from aut import ldtp

import constants
import base

logger = logging.getLogger(__name__)

class BookmarkTest(base.BaseTest):

	def test_01_bookmark_menu(self):

		logger.info('Starting \'{0}\''.format(inspect.stack()[0][3]))

		left_notebook_tabs = ldtp.getobjectproperty(constants.APP_NAME, constants.NOTEBOOK_LEFT_PANEL, 'children')
		left_first_tab_filler = ldtp.getobjectproperty(constants.APP_NAME, left_notebook_tabs, 'children').split()[0]
		left_first_tab_top_panel = ldtp.getobjectproperty(constants.APP_NAME, left_first_tab_filler, 'children').split()[0]
		left_first_tab_top_panel_filler = ldtp.getobjectproperty(constants.APP_NAME, left_first_tab_top_panel, 'children').split()[0]
		left_first_tab_bookmark_button = ldtp.getobjectproperty(constants.APP_NAME, left_first_tab_top_panel_filler, 'children').split()[-1]

		ldtp.click(constants.APP_NAME, left_first_tab_bookmark_button) # pop up

		# print ldtp.objectexist(constants.APP_NAME, 'mnubookmarks')
		# print ldtp.waittillguiexist(constants.APP_NAME, 'mnubookmarks')

		# TODO can't find menu to select item in it ???

		ldtp.click(constants.APP_NAME, left_first_tab_bookmark_button) # close
