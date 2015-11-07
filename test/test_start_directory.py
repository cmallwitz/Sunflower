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
import os

import aut
import constants
import base

logger = logging.getLogger(__name__)

class StartDirectoryTest(base.BaseTest):

	def test_02_regular_sub_directory(self):

		logger.info('Starting \'{0}\''.format(inspect.stack()[0][3]))

		self.main_frame = aut.create(constants.APP_NAME, constants.MAIN_FRAME, expected_clazz='frame')
		self.left_notebook = self.main_frame.find("./filler/filler[2]/split_pane/page_tab_list[0]")
		self.assertEqual(1, len(self.left_notebook.children))

		self.left_table = self.left_notebook.find("./page_tab[0]/filler/scroll_pane[1]/tree_table[0]")

		dir = '/tmp/sunflower/foo'

		logger.info('Setting left table to \'{0}\''.format(dir))
		context_push_button = self.left_notebook.find("./page_tab[0]/filler/panel[0]/filler/push_button[0]")
		context_push_button.click()
		aut.generatekeyevent('<down>')
		aut.generatekeyevent('<down>')
		aut.generatekeyevent('<down>')
		aut.generatekeyevent('<enter>')
		aut.waittillguiexist(constants.PATH_ENTRY_DIALOG)

		path_entry_dialog = aut.create(constants.PATH_ENTRY_DIALOG, constants.PATH_ENTRY_DIALOG, expected_clazz='dialog')
		path_text = path_entry_dialog.find("./filler[0]/filler[0]/filler/text")
		path_text.enterstring(dir)
		aut.generatekeyevent('<enter>')
		aut.waittillguinotexist(constants.PATH_ENTRY_DIALOG)

		self.verify_table_content(self.left_table, self.generate_table_content(dir))

		base.quit_sunflower()
		base.launch_sunflower()

		self.verify_table_content(self.left_table, self.generate_table_content(dir))

	def test_04_zip_root_directory(self):

		logger.info('Starting \'{0}\''.format(inspect.stack()[0][3]))

		self.main_frame = aut.create(constants.APP_NAME, constants.MAIN_FRAME, expected_clazz='frame')
		self.left_notebook = self.main_frame.find("./filler/filler[2]/split_pane/page_tab_list[0]")
		self.assertEqual(1, len(self.left_notebook.children))

		self.left_table = self.left_notebook.find("./page_tab[0]/filler/scroll_pane[1]/tree_table[0]")

		dir = '/tmp/sunflower'

		logger.info('Setting left table to \'{0}\''.format(dir))
		context_push_button = self.left_notebook.find("./page_tab[0]/filler/panel[0]/filler/push_button[0]")
		context_push_button.click()
		aut.generatekeyevent('<down>')
		aut.generatekeyevent('<down>')
		aut.generatekeyevent('<down>')
		aut.generatekeyevent('<enter>')
		aut.waittillguiexist(constants.PATH_ENTRY_DIALOG)

		path_entry_dialog = aut.create(constants.PATH_ENTRY_DIALOG, constants.PATH_ENTRY_DIALOG, expected_clazz='dialog')
		path_text = path_entry_dialog.find("./filler[0]/filler[0]/filler/text")
		path_text.enterstring(dir)
		aut.generatekeyevent('<enter>')
		aut.waittillguinotexist(constants.PATH_ENTRY_DIALOG)

		self.verify_table_content(self.left_table, self.generate_table_content(dir))

		logger.info('Switch to \'/tmp/sunflower/test.zip\'')
		self.left_table.selectrow('test.zip')
		aut.generatekeyevent('<enter>')

		test_zip = [
			['..', '<DIR>'],
			['test', '<DIR>'],
		]
		self.verify_table_content(self.left_table, test_zip)

		base.quit_sunflower()
		base.launch_sunflower()

		failed_zip = [
			['..', '<DIR>'],
		]

		self.verify_table_content(self.left_table, failed_zip) # TODO - wrong directory - this will change....

	def test_06_zip_sub_directory(self):

		logger.info('Starting \'{0}\''.format(inspect.stack()[0][3]))

		self.main_frame = aut.create(constants.APP_NAME, constants.MAIN_FRAME, expected_clazz='frame')
		self.left_notebook = self.main_frame.find("./filler/filler[2]/split_pane/page_tab_list[0]")
		self.assertEqual(1, len(self.left_notebook.children))

		self.left_table = self.left_notebook.find("./page_tab[0]/filler/scroll_pane[1]/tree_table[0]")

		dir = '/tmp/sunflower'

		logger.info('Setting left table to \'{0}\''.format(dir))
		context_push_button = self.left_notebook.find("./page_tab[0]/filler/panel[0]/filler/push_button[0]")
		context_push_button.click()
		aut.generatekeyevent('<down>')
		aut.generatekeyevent('<down>')
		aut.generatekeyevent('<down>')
		aut.generatekeyevent('<enter>')
		aut.waittillguiexist(constants.PATH_ENTRY_DIALOG)

		path_entry_dialog = aut.create(constants.PATH_ENTRY_DIALOG, constants.PATH_ENTRY_DIALOG, expected_clazz='dialog')
		path_text = path_entry_dialog.find("./filler[0]/filler[0]/filler/text")
		path_text.enterstring(dir)
		aut.generatekeyevent('<enter>')
		aut.waittillguinotexist(constants.PATH_ENTRY_DIALOG)

		self.verify_table_content(self.left_table, self.generate_table_content(dir))

		logger.info('Switch to \'/tmp/sunflower/test.zip/test\'')
		self.left_table.selectrow('test.zip')
		aut.generatekeyevent('<enter>')
		self.left_table.selectrow('test')
		aut.generatekeyevent('<enter>')

		test_zip = [
			['..', '<DIR>'],
			['bar', '<DIR>'],
			['foo', '<DIR>'],
		]
		self.verify_table_content(self.left_table, test_zip)

		base.quit_sunflower()
		base.launch_sunflower()

		aut.waittillguiexist('dlgswitch_dir_failed')  # TODO - switch failed - this will change....
		aut.generatekeyevent('<alt>n')
		self.verify_table_content(self.left_table, self.generate_table_content(os.path.expanduser('~')))
