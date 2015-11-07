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

import os
os.environ['LDTP_DEBUG'] = '1'

import json
import logging
import re
import shutil
import subprocess
import stat
import sys
import time
import traceback
import unittest

from gi.repository import GLib
from gi.repository import Gio

logging.basicConfig(# filename='/tmp/sunflower-test.log', filemode='w',
                    format='[%(asctime)s] (%(threadName)s) %(levelname)s %(name)s:%(lineno)d %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

from aut import ldtp

import constants

# import logutil
# sys.stdout = logutil.StreamCapture('[stdout]')
# sys.stderr = logutil.StreamCapture('[stderr]')

def kill_sunflower():

    logger.info('Killing running Sunflower processes.')

    try:
        process_details = subprocess.check_output(["ps -aef | egrep '(python.*[a]pplication/main|[S]unflower.py)'"], shell=True).splitlines()
        for line in process_details:
            pid = line.split()[1]
            logger.info('Killing pid={0}'.format(pid))
            subprocess.call(['kill -9 ' + pid], shell=True)
        return True
    except:
        logger.info('No running Sunflower process found.')

    return False

def launch_sunflower():

    logger.info('Starting Sunflower process.')

    pid = ldtp.launchapp('python', ['Sunflower.py'], env=0)

    logger.info('Start pid={0}'.format(pid))

    cmd = "ps -aef | egrep '\\b{0}\\b.*(python.*[a]pplication/main|[S]unflower.py)'".format(pid)
    logger.info(cmd)

    process_details = subprocess.check_output([cmd], shell=True).splitlines()
    logger.info(process_details)

    assert len(process_details) > 0

    if ldtp.waittillguiexist(constants.APP_NAME) == 0:
        raise ldtp.LdtpExecutionError(constants.APP_NAME + ' window does not exist - is another ldtp enabled process still running?')

    ldtp.appundertest(constants.APP_NAME)

    return pid

def quit_sunflower():

    logger.info('Quit Sunflower process.')

    ldtp.selectmenuitem(constants.APP_NAME, 'mnuQuit')

    if ldtp.waittillguinotexist(constants.APP_NAME) == 0:
        if ldtp.guiexist(constants.APP_NAME) != 0:
            raise ldtp.LdtpExecutionError ('Sunflower window still exist')

def setup_panel_root_directory(panel_root_dir):

    logger.info('Setting up root test directory for panels')

    try:
        os.mkdir(panel_root_dir)
    except:
        pass # ignore if it exists

    try:
        if os.path.exists(panel_root_dir):
            shutil.rmtree(panel_root_dir)
    except:
        logger.error('Failed to delete panel root dir: ' + panel_root_dir)
        sys.exit()

    try:
        shutil.copytree('test/mime', panel_root_dir)
    except:
        logger.error('Failed to set up panel root dir: ' + panel_root_dir)
        traceback.print_exc()
        sys.exit()

    os.mkdir(panel_root_dir + '/foo')
    os.mkdir(panel_root_dir + '/foo/bar')

    open(panel_root_dir + '/foo/file_01.txt', 'a').close()
    open(panel_root_dir + '/foo/file_02.txt', 'a').close()
    open(panel_root_dir + '/foo/file_03.txt', 'a').close()
    open(panel_root_dir + '/foo/.ignore', 'a').close()
    open(panel_root_dir + '/foo/backup.txt~', 'a').close()

def get_config(config_dir):

    logger.info('Load Sunflower base config.')

    with open(config_dir + '/config.json', 'r') as fp:
        config = json.load(fp, encoding="utf-8")

    return config

def set_tab_config(config_dir, panel_root_dir):

    logger.info('Generate Sunflower test panel/tab config.')

    panel = {
        'active_tab': 0,
        'tabs': [{
            'class': "FileList",
            'lock': None,
            'path': panel_root_dir,
            'sort_ascending': True,
            'sort_column': 0
        }]
    }
    tabs = {
        'left': panel,
        'right': panel
    }

    with open(config_dir + '/tabs.json', 'w') as fp:
        json.dump(tabs, fp, indent=4, sort_keys=True, encoding="utf-8")

def unmount_all_volumes():

    main_loop = GLib.MainLoop()

    def unmount_cb(mount, async_result, user_data=None):
        try:
            mount.unmount_finish(async_result)
            main_loop.quit()
        except GLib.GError as e:
            raise AssertionError('GLib.GError: mount={0} domain={1} code={2} message={3}'.format(mount, e.domain, e.code, e.message))

    for m in Gio.VolumeMonitor().get().get_mounts():
        uri = m.get_root().get_uri()
        try:
            logger.info('unmounting {0}'.format(uri))
            mount = Gio.file_new_for_commandline_arg(uri).find_enclosing_mount(None)
            mount.unmount(Gio.MountUnmountFlags.FORCE, None, unmount_cb, None)
            main_loop.run()
        except GLib.GError as e:
            raise AssertionError('GLib.GError: uri={0} domain={1} code={2} message={3}'.format(uri, e.domain, e.code, e.message))

def mount_volume(uri, mount_op):

    main_loop = GLib.MainLoop()

    def mount_cb(mount, async_result, user_data=None):
        try:
            mount.mount_enclosing_volume_finish(async_result)
            main_loop.quit()
        except GLib.GError as e:
            raise AssertionError('GLib.GError: mount={0} domain={1} code={2} message={3}'.format(mount, e.domain, e.code, e.message))

    try:
        logger.info('mounting {0}'.format(uri))
        Gio.file_new_for_commandline_arg(uri).mount_enclosing_volume(Gio.MountMountFlags.NONE, mount_op, None, mount_cb, None)
        main_loop.run()
    except GLib.GError as e:
        raise AssertionError('GLib.GError: uri={0} domain={1} code={2} message={3}'.format(uri, e.domain, e.code, e.message))

# def unmount_all_volumes():
#
# 	main_loop = glib.MainLoop()
#
# 	def unmount_cb(mount, async_result, user_data=None):
# 		try:
# 			mount.unmount_finish(async_result)
# 			main_loop.quit()
# 		except glib.GError as e:
# 			raise AssertionError('GLib.GError: mount={0} domain={1} code={2} message={3}'.format(mount, e.domain, e.code, e.message))
#
# 	for m in gio.VolumeMonitor().get_mounts():
#
# 		uri = m.get_root().get_uri()
#
# 		try:
# 			logger.info('unmounting {0}'.format(uri))
# 			mount = gio.File(uri).find_enclosing_mount(None)
# 			mount.unmount(unmount_cb, gio.MOUNT_UNMOUNT_FORCE, None, None)
# 			main_loop.run()
# 		except glib.GError as e:
# 			raise AssertionError('GLib.GError: uri={0} domain={1} code={2} message={3}'.format(uri, e.domain, e.code, e.message))
#
# def mount_test_volume(uri, mount_op):
#
# 	main_loop = glib.MainLoop()
#
# 	def mount_cb(mount, async_result, user_data=None):
# 		try:
# 			mount.mount_enclosing_volume_finish(async_result)
# 			main_loop.quit()
# 		except glib.GError as e:
# 			raise AssertionError('GLib.GError: mount={0} domain={1} code={2} message={3}'.format(mount, e.domain, e.code, e.message))
#
# 	try:
# 		logger.info('mounting {0}'.format(uri))
# 		gio.File(uri).mount_enclosing_volume(mount_op, mount_cb)
# 		main_loop.run()
# 	except glib.GError as e:
# 		raise AssertionError('GLib.GError: uri={0} domain={1} code={2} message={3}'.format(uri, e.domain, e.code, e.message))

class BaseTest(unittest.TestCase):

    config = None

    @classmethod
    def setUpClass(clazz):

        logger.info('setUpClass() started')

        # enable toolkit accessibility for LDTP by running
        # gsettings set org.gnome.desktop.interface toolkit-accessibility true
        subprocess.call(['gsettings', 'set', 'org.gnome.desktop.interface', 'toolkit-accessibility', 'true'])
        # gsettings set org.gnome.desktop.a11y.applications screen-reader-enabled false
        # subprocess.call(['gsettings', 'set', 'org.gnome.desktop.a11y.applications', 'screen-reader-enabled', 'false'])

        home_dir = os.path.expanduser('~')
        config_dir = home_dir + '/.config/sunflower'
        panel_root_dir = '/tmp/sunflower'

        logger.info('user home directory: ' + home_dir)
        logger.info('config directory: ' + config_dir)
        logger.info('panel root directory: ' + panel_root_dir)

        kill_sunflower()
        setup_panel_root_directory(panel_root_dir)
        clazz.config = get_config(config_dir)
        set_tab_config(config_dir, panel_root_dir)

        unmount_all_volumes()

        def ask_password_cb(op, message, default_user, default_domain, flags):
            op.set_username("christian")
            op.set_password("catford")
            op.set_domain("")
            op.reply(Gio.MountMountFlags.NONE)

        op = Gio.MountOperation()
        op.connect('ask-password', ask_password_cb)
        mount_volume("smb://i7520/christian/", op)

        pid = launch_sunflower()

        logger.info('set up - finished')

    @classmethod
    def tearDownClass(clazz):

        logger.info('tearDownClass() started')
        quit_sunflower()
        logger.info('tear down - finished')

    def is_single_test(self):
        if len(sys.argv) == 3:
            return sys.argv[1].count('::') == 2
        return False

    def generate_table_content(self, path):

        config_item_list = self.config['item_list']
        config_show_hidden = config_item_list['show_hidden']
        config_number_sensitive_sort = config_item_list['number_sensitive_sort']
        config_case_sensitive_sort = config_item_list['case_sensitive_sort']
        config_mode_format = config_item_list['mode_format']
        config_time_format = config_item_list['time_format']

        file_list = []

        for f in os.listdir(unicode(path)):
            if (f.startswith('.') or f.endswith('~')) and not config_show_hidden:
                continue
            pathname = os.path.join(path, f)
            mode = os.stat(pathname).st_mode
            if stat.S_ISDIR(mode):
                file_list.append([f, '<DIR>'])
            elif stat.S_ISREG(mode):
                file_list.append([f])
            else:
                pass

        def sort_func(a, b):
            a_size = 1 if len(a) > 1 and a[1] == '<DIR>' else 2
            b_size = 1 if len(b) > 1 and b[1] == '<DIR>' else 2

            a_name = a[0]
            b_name = b[0]

            # GNOME conformant ordering - config_number_sensitive_sort irrelevant
            #if not config_case_sensitive_sort:
            #	a_name = GLib.utf8_casefold(a_name, -1)
            #	b_name = GLib.utf8_casefold(b_name, -1)
            #a_name = GLib.utf8_collate_key_for_filename(a_name, -1)
            #b_name = GLib.utf8_collate_key_for_filename(b_name, -1)

            # Sunflower ordering
            if not config_case_sensitive_sort:
                a_name = a_name.lower()
                b_name = b_name.lower()

            number_split = re.compile('([0-9]+)')
            if config_number_sensitive_sort:
                a_name = [int(part) if part.isdigit() else part for part in number_split.split(a_name)]
                b_name = [int(part) if part.isdigit() else part for part in number_split.split(b_name)]

            return cmp(a_size, b_size) or cmp(a_name, b_name)

        file_list.sort(sort_func)
        file_list.insert(0, ['..', '<DIR>'])

        return file_list

    def verify_table_content(self, table, content):
        self.assertEqual(len(content), table.getrowcount())
        for i, row in enumerate(content):
            for j, cell in enumerate(row):
                self.assertEqual(row[j], unicode(table.getcellvalue(i, j), encoding='utf-8'))
