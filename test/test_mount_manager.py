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

class MountManagerTest(base.BaseTest):
	
	def test_02_mount_public_ftp(self):

		ftp_server = 'ftp.mirrorservice.org'
		ftp_path = '/'
		ftp_user = 'anonymous'

		# ftp.mirrorservice.org /sites/sourceware.org/pub/cygwin
		# ftp://anonymous@ftp.mirrorservice.org/pub/gnu/emacs/windows

		logger.info('Starting \'{0}\''.format(inspect.stack()[0][3]))

		# open Mount Manger window through menu
		aut.create(constants.APP_NAME, 'mnuMountmanager', expected_clazz='menu_item').click()
		aut.waittillguiexist(constants.MOUNT_MGR_FRAME)

		# aut.create(constants.MOUNT_MGR_FRAME, constants.MOUNT_MGR_FRAME).print_details(indent=0, depth=7)

		mount_types = aut.create(constants.MOUNT_MGR_FRAME, 'tblmounttypes', expected_clazz='table')
		mount_tabs = aut.create(constants.MOUNT_MGR_FRAME, 'ptlmounttabs', expected_clazz='page_tab_list')

		# check mount types
		mount_type_list = [
			['Mounts',],
			['Volumes'],
			['Samba',],
			['FTP',],
			['SFTP',],
			['WebDav',],
		]
		self.verify_table_content(mount_types, mount_type_list)

		mount_types.selectrow('Mounts')

		mount_tab = mount_tabs.find("./page_tab[0]/filler[@key='flrmountsbox']")
		mount_table = mount_tab.find("./scroll_pane[0]/table[@key='tblmountstable']")
		mount_open_button = mount_tab.find("./filler[1]/push_button[@label='Open']")
		mount_openintab_button = mount_tab.find("./filler[1]/push_button[@label='Open in tab']")
		mount_unmount_button = mount_tab.find("./filler[1]/push_button[@label='Unmount']")

		logger.info('Unmounting everything')
		for i in range(0, mount_table.getrowcount()):
			_name = mount_table.getcellvalue(i, 0)
			mount_table.selectrowindex(i)
			mount_unmount_button.click()

		mount_types.selectrow('FTP')

		ftp_tab = mount_tabs.find("./page_tab[3]/filler[@key='flrftpbox']")
		ftp_table = ftp_tab.find("./scroll_pane[0]/table[@key='tblftptable']")
		ftp_add_button = ftp_tab.find("./filler[1]/push_button[@label='Add']")
		ftp_edit_button = ftp_tab.find("./filler[1]/push_button[@label='Edit']")
		ftp_del_button = ftp_tab.find("./filler[1]/push_button[@label='Delete']")
		ftp_mount_button = ftp_tab.find("./filler[1]/push_button[@label='Mount']")
		ftp_unmount_button = ftp_tab.find("./filler[1]/push_button[@label='Unmount']")

		for i in range(0, ftp_table.getrowcount()):
			_name = ftp_table.getcellvalue(i, 0)
			logger.info('Checking FTP config \'{0}\''.format(_name))
			if _name == ftp_server:
				ftp_table.selectrowindex(i)
				ftp_del_button.click()
				aut.waittillguiexist('dlgmount_confirmation_delete')
				dialog = aut.create('dlgmount_confirmation_delete', 'dlgmount_confirmation_delete', expected_clazz='alert')
				dialog.find("./filler/filler[1]/push_button[@label='Yes']").click()

		logger.info('Adding FTP config \'{0}\''.format(ftp_server))

		ftp_add_button.click()
		aut.waittillguiexist('dlgCreateFTPmount')
		dialog = aut.create('dlgCreateFTPmount', 'dlgCreateFTPmount', expected_clazz='dialog')
		dialog.find("./filler/filler[0]/filler[1]/filler[0]/text").enterstring(ftp_server)
		dialog.find("./filler/filler[0]/filler[1]/filler[2]/text").enterstring(ftp_server)
		dialog.find("./filler/filler[0]/filler[1]/filler[3]/text").enterstring(ftp_path)
		dialog.find("./filler/filler[0]/filler[1]/filler[5]/text").enterstring(ftp_user)
		dialog.find("./filler/filler[1]/push_button[@label='Save']").click()
		aut.waittillguinotexist('dlgCreateFTPmount')

		ftp_table.selectrow(ftp_server)
		ftp_mount_button.click()

		aut.create(constants.MOUNT_MGR_FRAME, 'btnClose').click()
		aut.waittillguinotexist(constants.MOUNT_MGR_FRAME)
