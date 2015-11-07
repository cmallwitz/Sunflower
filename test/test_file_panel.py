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

class FilePanelTest(base.BaseTest):

	def setUp(self):

		logger.info('Starting \'{0}\''.format(inspect.stack()[0][3]))

		self.main_frame = aut.create(constants.APP_NAME, constants.MAIN_FRAME, expected_clazz='frame')
		self.left_notebook = self.main_frame.find("./filler/filler[2]/split_pane/page_tab_list[0]")
		self.right_notebook = self.main_frame.find("./filler/filler[2]/split_pane/page_tab_list[1]")
		self.assertEqual(1, len(self.left_notebook.children))
		self.assertEqual(1, len(self.right_notebook.children))

		logger.info('Running as single test ' + str(self.is_single_test()))

		if not self.is_single_test():

			logger.info('Setting left table to \'/tmp/sunflower\'')
			context_push_button = self.left_notebook.find("./page_tab[0]/filler/panel[0]/filler/push_button[0]")
			context_push_button.click()
			aut.generatekeyevent('<down>')
			aut.generatekeyevent('<down>')
			aut.generatekeyevent('<down>')
			aut.generatekeyevent('<enter>')
			aut.waittillguiexist(constants.PATH_ENTRY_DIALOG)
			path_entry_dialog = aut.create(constants.PATH_ENTRY_DIALOG, constants.PATH_ENTRY_DIALOG, expected_clazz='dialog')

			path_text = path_entry_dialog.find("./filler[0]/filler[0]/filler/text")
			ok_button = path_entry_dialog.find("./filler[0]/filler[1]/push_button[@label='OK']")
			path_text.enterstring('/tmp/sunflower')
			ok_button.click()
			aut.waittillguinotexist(constants.PATH_ENTRY_DIALOG)

			logger.info('Setting right table to \'/tmp/sunflower\'')
			context_push_button = self.right_notebook.find("./page_tab[0]/filler/panel[0]/filler/push_button[0]")
			context_push_button.click()
			aut.generatekeyevent('<down>')
			aut.generatekeyevent('<down>')
			aut.generatekeyevent('<down>')
			aut.generatekeyevent('<enter>')
			aut.waittillguiexist(constants.PATH_ENTRY_DIALOG)
			path_entry_dialog = aut.create(constants.PATH_ENTRY_DIALOG, constants.PATH_ENTRY_DIALOG, expected_clazz='dialog')

			path_text = path_entry_dialog.find("./filler[0]/filler[0]/filler/text")
			ok_button = path_entry_dialog.find("./filler[0]/filler[1]/push_button[@label='OK']")
			path_text.enterstring('/tmp/sunflower')
			ok_button.click()
			aut.waittillguinotexist(constants.PATH_ENTRY_DIALOG)

		self.left_table = self.left_notebook.find("./page_tab[0]/filler/scroll_pane[1]/tree_table[0]")
		self.assertEqual(self.left_table.getrowcount(), len(self.generate_table_content('/tmp/sunflower')))

		self.right_table = self.right_notebook.find("./page_tab[0]/filler/scroll_pane[1]/tree_table[0]")
		self.assertEqual(self.right_table.getrowcount(), len(self.generate_table_content('/tmp/sunflower')))

	def test_02_panel_ctrl_left_right(self):

		logger.info('Starting \'{0}\''.format(inspect.stack()[0][3]))

		# self.left_notebook.print_details(indent=0, depth=6)

		# there is one tab for /tmp/sunflower
		self.assertEqual(1, len(self.left_notebook.find("./page_tab[@label='sunflower']").children))
		self.assertEqual(4, len(self.left_notebook.find("./page_tab[@label='sunflower']/filler").children))
		self.assertEqual(1, len(self.left_notebook.find("./page_tab[@label='sunflower']/filler/panel[0]").children))
		self.assertEqual(3, len(self.left_notebook.find("./page_tab[@label='sunflower']/filler/scroll_pane[1]").children))

		top_box_items = self.left_notebook.find("./page_tab[@label='sunflower']/filler/panel[0]/filler")
		self.assertEqual(6, len(top_box_items.children))

		self.assertIsNotNone(top_box_items.find("./push_button[@description='Context menu']"))
		self.assertIsNotNone(top_box_items.find("./filler[1]"))
		self.assertIsNotNone(top_box_items.find("./icon[@child_index='2' and @label='Spinner']"))
		self.assertIsNotNone(top_box_items.find("./push_button[@child_index='3' and @description='Terminal']"))
		self.assertIsNotNone(top_box_items.find("./push_button[@child_index='4' and @description='History']"))
		self.assertIsNotNone(top_box_items.find("./push_button[@child_index='5' and @description='Bookmarks']"))

		self.assertEqual(2, len(top_box_items.find("./filler[1]").children))
		self.assertIsNotNone(top_box_items.find("./filler[1]/filler[0]"))
		self.assertIsNotNone(top_box_items.find("./filler[1]/label[1]"))

		self.verify_table_content(self.left_table, self.generate_table_content('/tmp/sunflower'))
		self.verify_table_content(self.right_table, self.generate_table_content('/tmp/sunflower'))

		logger.info('Switch left to \'/tmp/sunflower/foo\'')
		self.left_table.selectrow('foo')
		aut.generatekeyevent('<enter>')
		self.verify_table_content(self.left_table, self.generate_table_content('/tmp/sunflower/foo'))

		logger.info('Switch right to \'/tmp/sunflower/foo\'') # TODO - this will change....
		self.left_table.selectrow('bar')
		aut.generatekeyevent('<ctrl><right>')
		self.verify_table_content(self.right_table, self.generate_table_content('/tmp/sunflower/foo'))

		logger.info('Switch left to \'/tmp/sunflower\'')
		self.left_table.selectrow('bar')
		aut.generatekeyevent('<backspace>')
		self.assertEqual(self.left_table.getrowcount(), len(self.generate_table_content('/tmp/sunflower')))

	def test_04_left_panel_ctrl_left(self):

		logger.info('Starting \'{0}\''.format(inspect.stack()[0][3]))

		self.assertEqual(self.left_table.getrowcount(), len(self.generate_table_content('/tmp/sunflower')))

		logger.info('Switch right side to \'/tmp/sunflower/foo\'')
		self.right_table.selectrow('foo')
		aut.generatekeyevent('<enter>')
		self.assertEqual(self.right_table.getrowcount(), len(self.generate_table_content('/tmp/sunflower/foo')))
		self.right_table.selectrow('bar')

		logger.info('Switch to \'/tmp/sunflower/foo\'')
		self.left_table.selectrow('foo')
		aut.generatekeyevent('<enter>')
		self.assertEqual(self.left_table.getrowcount(), len(self.generate_table_content('/tmp/sunflower/foo')))

		logger.info('Switch to \'/tmp/sunflower/foo/bar\'')
		self.left_table.selectrow('bar')
		aut.generatekeyevent('<enter>')
		self.assertEqual(self.left_table.getrowcount(), len(self.generate_table_content('/tmp/sunflower/foo/bar')))

		self.left_table.selectrow('..') # pulling /tmp/sunflower/foo from right
		aut.generatekeyevent('<ctrl><left>')
		self.assertEqual(self.left_table.getrowcount(), len(self.generate_table_content('/tmp/sunflower/foo')))

		logger.info('Switch right side to \'/tmp/sunflower\'')
		self.right_table.selectrow('..')
		aut.generatekeyevent('<enter>')
		self.assertEqual(self.right_table.getrowcount(), len(self.generate_table_content('/tmp/sunflower')))

		self.right_table.selectrow('test.zip')
		aut.generatekeyevent('<enter>')

		test_zip = [
			['..', '<DIR>'],
			['test', '<DIR>'],
		]
		self.verify_table_content(self.right_table, test_zip)

		self.left_table.selectrow('..') # pulling /tmp/sunflower/test.zip from right
		aut.generatekeyevent('<ctrl><left>')

		failed_zip = [
			['..', '<DIR>'],
		]

		self.verify_table_content(self.left_table, failed_zip) # TODO - switch failed - this will change....

	def test_04_right_panel_ctrl_right(self):

		logger.info('Starting \'{0}\''.format(inspect.stack()[0][3]))

		self.assertEqual(self.right_table.getrowcount(), len(self.generate_table_content('/tmp/sunflower')))

		logger.info('Switch left to \'/tmp/sunflower/foo\'')
		self.left_table.selectrow('foo')
		aut.generatekeyevent('<enter>')
		self.assertEqual(self.left_table.getrowcount(), len(self.generate_table_content('/tmp/sunflower/foo')))
		self.left_table.selectrow('bar')

		logger.info('Switch to \'/tmp/sunflower/foo\'')
		self.right_table.selectrow('foo')
		aut.generatekeyevent('<enter>')
		self.assertEqual(self.right_table.getrowcount(), len(self.generate_table_content('/tmp/sunflower/foo')))

		logger.info('Switch to \'/tmp/sunflower/foo/bar\'')
		self.right_table.selectrow('bar')
		aut.generatekeyevent('<enter>')
		self.assertEqual(self.right_table.getrowcount(), len(self.generate_table_content('/tmp/sunflower/foo/bar')))

		self.right_table.selectrow('..') # pulling /tmp/sunflower/foo from left
		aut.generatekeyevent('<ctrl><right>')
		self.assertEqual(self.right_table.getrowcount(), len(self.generate_table_content('/tmp/sunflower/foo')))

		logger.info('Switch right side to \'/tmp/sunflower\'')
		self.left_table.selectrow('..')
		aut.generatekeyevent('<enter>')
		self.assertEqual(self.left_table.getrowcount(), len(self.generate_table_content('/tmp/sunflower')))

		self.left_table.selectrow('test.zip')
		aut.generatekeyevent('<enter>')

		test_zip = [
			['..', '<DIR>'],
			['test', '<DIR>'],
		]
		self.verify_table_content(self.left_table, test_zip)

		self.right_table.selectrow('..') # pulling /tmp/sunflower/test.zip from left
		aut.generatekeyevent('<ctrl><right>')

		failed_zip = [
			['..', '<DIR>'],
		]

		self.verify_table_content(self.right_table, failed_zip) # TODO - switch failed - this will change....

	def test_06_source_zip_target_regular_directory(self):

		logger.info('Starting \'{0}\''.format(inspect.stack()[0][3]))

		self.assertEqual(self.left_table.getrowcount(), len(self.generate_table_content('/tmp/sunflower')))

		logger.info('Switch to \'/tmp/sunflower/test.zip\'')
		self.left_table.selectrow('test.zip')
		aut.generatekeyevent('<enter>')

		test_zip = [
			['..', '<DIR>'],
			['test', '<DIR>'],
		]
		self.verify_table_content(self.left_table, test_zip)

		failed_zip = [
			['..', '<DIR>'],
		]

		logger.info('Switch right to \'/tmp/sunflower/test.zip/test\'')
		self.left_table.selectrow('test')
		aut.generatekeyevent('<ctrl><right>')
		self.verify_table_content(self.right_table, failed_zip) # TODO - switch failed - this will change....

		logger.info('Switch to \'/tmp/sunflower/test.zip/test\'')
		self.left_table.selectrow('test')
		aut.generatekeyevent('<enter>')

		test_zip = [
			['..', '<DIR>'],
			['bar', '<DIR>'],
			['foo', '<DIR>'],
		]
		self.verify_table_content(self.left_table, test_zip)

		logger.info('Switch right to \'/tmp/sunflower/test.zip/test/foo\'')
		self.left_table.selectrow('foo')
		aut.generatekeyevent('<ctrl><right>')

		aut.waittillguiexist('dlgswitch_dir_failed') # TODO - switch failed - this will change....
		aut.generatekeyevent('<alt>n')
		self.verify_table_content(self.right_table, failed_zip)

		logger.info('Switch to \'/tmp/sunflower/\'')
		self.left_table.selectrow('..')
		aut.generatekeyevent('<backspace>')
		self.left_table.selectrow('..')
		aut.generatekeyevent('<backspace>')
		self.assertEqual(self.left_table.getrowcount(), len(self.generate_table_content('/tmp/sunflower')))

	def test_08_source_zip_target_zip(self):

		logger.info('Starting \'{0}\''.format(inspect.stack()[0][3]))

		self.assertEqual(self.left_table.getrowcount(), len(self.generate_table_content('/tmp/sunflower')))

		logger.info('Switch right to \'/tmp/sunflower/test.zip\'')
		self.right_table.selectrow('test.zip')
		aut.generatekeyevent('<enter>')

		logger.info('Switch right to \'/tmp/sunflower/test.zip/test\'')
		self.right_table.selectrow('test')
		aut.generatekeyevent('<enter>')

		logger.info('Switch right to \'/tmp/sunflower/test.zip/test/bar\'')
		self.right_table.selectrow('bar')
		aut.generatekeyevent('<enter>')

		logger.info('Switch to \'/tmp/sunflower/test.zip\'')
		self.left_table.selectrow('test.zip')
		aut.generatekeyevent('<enter>')

		test_zip = [
			['..', '<DIR>'],
			['test', '<DIR>'],
		]
		self.verify_table_content(self.left_table, test_zip)

		logger.info('Switch right to \'/tmp/sunflower/test.zip/test\'')
		self.left_table.selectrow('test')
		aut.generatekeyevent('<ctrl><right>')
		self.verify_table_content(self.right_table, test_zip) # TODO - switch failed - this will change....

		logger.info('Switch to \'/tmp/sunflower/test.zip/test\'')
		self.left_table.selectrow('test')
		aut.generatekeyevent('<enter>')

		test_zip = [
			['..', '<DIR>'],
			['bar', '<DIR>'],
			['foo', '<DIR>'],
		]
		self.verify_table_content(self.left_table, test_zip)

		logger.info('Switch right to \'/tmp/sunflower/test.zip/test/foo\'')
		self.left_table.selectrow('foo')
		aut.generatekeyevent('<ctrl><right>')
		self.verify_table_content(self.right_table, test_zip) # TODO - switch failed - this will change....

		logger.info('Switch to \'/tmp/sunflower/\'')
		self.left_table.selectrow('..')
		aut.generatekeyevent('<backspace>')
		self.left_table.selectrow('..')
		aut.generatekeyevent('<backspace>')
		self.assertEqual(self.left_table.getrowcount(), len(self.generate_table_content('/tmp/sunflower')))

	def test_20_command_text(self):

		logger.info('Starting \'{0}\''.format(inspect.stack()[0][3]))

		logger.info('Switch to \'/tmp/sunflower/empty.zip\'')
		self.left_table.selectrow('empty.zip')
		aut.generatekeyevent('<enter>')

		empty_zip = [
			['..', '<DIR>'],
			['empty.txt',],
		]
		self.verify_table_content(self.left_table, empty_zip)

		commmand_text_input_box = self.main_frame.find("./filler/filler[2]/filler/text[3]")

		commmand_text_input_box.enterstring('cd /tmp/sunflower<enter>')
		self.verify_table_content(self.left_table, empty_zip) # puts focus on table otherwise below fails

		# TODO - FIX - fails - this only works for same file item provider ? -> i.e. not from zip listing

		logger.info('Switch to \'/tmp/sunflower/\'')
		aut.generatekeyevent('<backspace>')
		self.assertEqual(self.left_table.getrowcount(), len(self.generate_table_content('/tmp/sunflower')))

		logger.info('Switch to \'/tmp/sunflower/foo\'')
		self.left_table.selectrow('foo')
		aut.generatekeyevent('<enter>')
		self.assertEqual(self.left_table.getrowcount(), len(self.generate_table_content('/tmp/sunflower/foo')))

		commmand_text_input_box.enterstring('cd /tmp/sunflower<enter>')
		self.assertEqual(self.left_table.getrowcount(), len(self.generate_table_content('/tmp/sunflower')))

	def test_30_user_home_directory(self):

		logger.info('Starting \'{0}\''.format(inspect.stack()[0][3]))

		dir = os.path.expanduser('~')

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
		ok_button = path_entry_dialog.find("./filler[0]/filler[1]/push_button[@label='OK']")
		path_text.enterstring(dir)
		ok_button.click()
		aut.waittillguinotexist(constants.PATH_ENTRY_DIALOG)

		self.verify_table_content(self.left_table, self.generate_table_content(dir))

	def test_40_encoding_directory(self):

		logger.info('Starting \'{0}\''.format(inspect.stack()[0][3]))

		logger.info('Switch to \'/tmp/sunflower/encoding\'')
		self.left_table.selectrow('encoding')
		aut.generatekeyevent('<enter>')

		self.verify_table_content(self.left_table, self.generate_table_content('/tmp/sunflower/encoding'))
