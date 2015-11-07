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

class MenuTest(base.BaseTest):

	def test_01_menues(self):

		logger.info('Starting \'{0}\''.format(inspect.stack()[0][3]))

		self.assertIsNone(aut.create(constants.APP_NAME, 'mnuFoo'))

		main_frame = aut.create(constants.APP_NAME, constants.MAIN_FRAME, expected_clazz='frame')
		menu_bar = main_frame.find("./filler/menu_bar")

		file_menu = menu_bar.find("./menu[@key='mnuFile' and @label='File']")
		self.assertTrue(file_menu.enabled())
		self.assertTrue(file_menu.find("./menu[@key='mnuNewtab' and @label='New tab']").enabled())
		self.assertTrue(file_menu.find("./menu[@key='mnuNewtab' and @label='New tab']/menu_item[@key='mnuSystemterminal' and @label='System terminal']").enabled())
		self.assertTrue(file_menu.find("./menu[@key='mnuNewtab' and @label='New tab']/menu_item[@key='mnuLocalfilelist' and @label='Local file list']").enabled())
		self.assertTrue(file_menu.find("./menu[@key='mnuNewtab' and @label='New tab']/menu_item[@key='mnuTrashcan' and @label='Trash can']").enabled())
		self.assertTrue(file_menu.find("./menu_item[@key='mnuCreatefile' and @label='Create file']").enabled())
		self.assertTrue(file_menu.find("./menu_item[@key='mnuCreatedirectory' and @label='Create directory']").enabled())
		self.assertTrue(file_menu.find("./menu_item[@key='mnuOpen' and @label='Open']").enabled())
		self.assertTrue(file_menu.find("./menu_item[@key='mnuOpeninnewtab' and @label='Open in new tab']").enabled())
		self.assertTrue(file_menu.find("./menu_item[@key='mnuProperties' and @label='Properties']").enabled())
		self.assertTrue(file_menu.find("./menu_item[@key='mnuQuit' and @label='Quit']").enabled())

		edit_menu = menu_bar.find("./menu[@key='mnuEdit' and @label='Edit']")
		self.assertTrue(edit_menu.enabled())

		mark_menu = menu_bar.find("./menu[@key='mnuMark' and @label='Mark']")
		self.assertTrue(mark_menu.enabled())

		tools_menu = menu_bar.find("./menu[@key='mnuTools' and @label='Tools']")
		self.assertTrue (tools_menu.enabled())
		self.assertTrue (tools_menu.find("./menu_item[@key='mnuFindfiles' and @label='Find files']").enabled())
		self.assertFalse(tools_menu.find("./menu_item[@key='mnuFindduplicatefiles' and @label='Find duplicate files']").enabled())
		self.assertFalse(tools_menu.find("./menu_item[@key='mnuSynchronizedirectories' and @label='Synchronize directories']").enabled())
		self.assertTrue (tools_menu.find("./menu_item[@key='mnuAdvancedrename' and @label='Advanced rename']").enabled())
		self.assertTrue (tools_menu.find("./menu_item[@key='mnuMountmanager' and @label='Mount manager']").enabled())
		self.assertTrue (tools_menu.find("./menu_item[@key='mnuKeyringmanager' and @label='Keyring manager']").enabled())

		view_menu = menu_bar.find("./menu[@key='mnuView' and @label='View']")
		self.assertTrue (view_menu.enabled())

		cmd_menu = menu_bar.find("./menu[@key='mnuCommands' and @label='Commands']")
		self.assertTrue (cmd_menu.enabled())

		op_menu = menu_bar.find("./menu[@key='mnuOperations' and @label='Operations']")
		self.assertTrue (op_menu.enabled())

		help_menu = menu_bar.find("./menu[@key='mnuHelp' and @label='Help']")
		self.assertTrue (help_menu.enabled())
