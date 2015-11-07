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

import aut
import constants
import base

logger = logging.getLogger(__name__)

class FilePropertiesTest(base.BaseTest):

	def setUp(self):

		logger.info('Starting \'{0}\''.format(inspect.stack()[0][3]))

		self.main_frame = aut.create(constants.APP_NAME, constants.MAIN_FRAME, expected_clazz='frame')
		self.left_notebook = self.main_frame.find("./filler/filler[2]/split_pane/page_tab_list[0]")
		self.assertEqual(1, len(self.left_notebook.children))

		self.left_table = self.left_notebook.find("./page_tab[0]/filler/scroll_pane[1]/tree_table[0]")
		self.assertEqual(self.left_table.getrowcount(), len(self.generate_table_content('/tmp/sunflower')))

	def test_02_file_properties(self):

		logger.info('Starting \'{0}\''.format(inspect.stack()[0][3]))

		self.left_table.selectrow('test.zip')
		aut.generatekeyevent('<alt><enter>')

		window_name = 'frmtest.zipProperties'
		aut.waittillguiexist(window_name)
		properties = aut.create(window_name, window_name, expected_clazz='frame')

		tabs = properties.find("./filler/page_tab_list")
		basic_tab =       tabs.find("./page_tab[@key='ptabBasic']")
		permissions_tab = tabs.find("./page_tab[@key='ptabPermissions']")
		openwith_tab =    tabs.find("./page_tab[@key='ptabOpenWith']")
		emblems_tab =     tabs.find("./page_tab[@key='ptabEmblems']")

		basic_panel = basic_tab.find("./filler/panel")
		self.assertEqual(15, len(basic_panel.children))

		self.assertEqual('unknown', basic_panel.children[2].label)
		self.assertEqual('/tmp/sunflower', basic_panel.children[3].label)

		close_button = properties.find("./filler/filler[1]/push_button[@key='btnClose']")

		close_button.click()

		self.left_table.selectrow('foo')
		aut.generatekeyevent('<enter>')

		self.left_table.selectrow('file_01.txt')
		aut.generatekeyevent('<alt><enter>')

		window_name = 'frmfile_01.txtProperties'
		aut.waittillguiexist(window_name)
		properties = aut.create(window_name, window_name, expected_clazz='frame')

		tabs = properties.find("./filler/page_tab_list")
		basic_tab =       tabs.find("./page_tab[@key='ptabBasic']")
		permissions_tab = tabs.find("./page_tab[@key='ptabPermissions']")
		openwith_tab =    tabs.find("./page_tab[@key='ptabOpenWith']")
		emblems_tab =     tabs.find("./page_tab[@key='ptabEmblems']")

		basic_panel = basic_tab.find("./filler/panel")
		self.assertEqual(15, len(basic_panel.children))

		self.assertEqual('unknown', basic_panel.children[2].label)
		self.assertEqual('/tmp/sunflower/foo', basic_panel.children[3].label)

		close_button = properties.find("./filler/filler[1]/push_button[@key='btnClose']")

		close_button.click()

		self.left_table.selectrow('..')
		aut.generatekeyevent('<backspace>')
