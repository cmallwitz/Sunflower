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

import ldtpd.core
ldtp = ldtpd.core.Ldtpd()

import logging
import ldtpd.utils
logger = logging.getLogger('')
logger.removeHandler(ldtpd.utils._custom_logger)

import time
import traceback
import pyparsing as pp

logger = logging.getLogger(__name__)

def create(window_name, component_name, parent_name=None, expected_clazz=None):

	_clazz_map = {
		'alert': 'Widget',
		'check_box': 'Widget',
		'check_menu_item': 'Menu',
		'combo_box': 'Widget',
		'dialog': 'Widget',
		'filler': 'Widget',
		'frame': 'Widget',
		'icon': 'Widget',
		'label': 'Widget',
		'menu': 'Menu',
		'menu_bar': 'Menu',
		'menu_item': 'Menu',
		'page_tab': 'Widget',
		'page_tab_list': 'Notebook',
		'panel': 'Widget',
		'push_button': 'Clickable',
		'scroll_bar': 'Widget',
		'scroll_pane': 'Widget',
		'separator': 'Widget',
		'split_pane': 'Widget',
		'table': 'Table',
		'table_column_header': 'Widget',
		'text': 'Text',
		'tool_bar': 'Widget',
		'tree_table': 'Table',
		'unknown': 'Widget',
	}

	try:
		clazz = ldtp.getobjectproperty(window_name, component_name, 'class')
		if expected_clazz is not None:
			if expected_clazz != clazz:
				logger.info("Clazz didn't match - window='%s', component='%s', clazz='%s', expected_clazz='%s'", window_name, component_name, clazz, expected_clazz)
				return None
			else:
				logger.info("Clazz matched - window='%s', component='%s', clazz='%s', expected_clazz='%s'", window_name, component_name, clazz, expected_clazz)
		type = _clazz_map[clazz]
		logger.debug('Creating \'%s\' [\'%s\'->\'%s\']', component_name, clazz, type)
		return globals()[type](window_name, component_name, parent_name=parent_name, clazz=clazz)
	except:
		traceback.print_exc()
		return None

def _build_parser():

	identifier     = pp.Word(pp.alphanums + '-' + '_')
	dot            = pp.Literal(".").setResultsName("dot")
	text           = pp.QuotedString(quoteChar="'", escChar='\\')
	and_token      = pp.Word("and").suppress()
	slash          = pp.Literal("/").suppress()
	left_bracket   = pp.Literal("[").suppress()
	right_bracket  = pp.Literal("]").suppress()
	equals         = pp.Literal("=").suppress()
	ampersand      = pp.Literal("@").suppress()

	sub_expression = pp.Group(ampersand + identifier.setResultsName("prop") + equals + text.setResultsName("value")).setResultsName("subexp")
	expression = sub_expression + pp.Optional(pp.OneOrMore(and_token + sub_expression))
	index = pp.Word(pp.nums).setResultsName("index")
	condition = left_bracket + pp.Group(index ^ expression ).setResultsName("condition") + right_bracket

	xpath_part = pp.Group(dot).setResultsName("dot") ^ pp.Group(identifier.setResultsName("clazz") + pp.Optional(condition))
	xpath = xpath_part + pp.Optional( pp.OneOrMore( slash + xpath_part))

	return xpath

class ChildrenProxy(object):

	def __init__(self, window_name, parent, children_names):
		self._window_name = window_name
		self._parent = parent
		self._children_names = children_names
		self._children = [None] * len(children_names)

	def __len__(self):
		return len(self._children_names)

	def __getitem__(self, key):
		if self._children[key] is None:
			self._children[key] = create(self._window_name, self._children_names[key], parent_name=self._parent)
		return self._children[key]

	def get_names(self):
		return list(self._children_names)

class Widget(object):

	parser = _build_parser()

	def __init__(self, window_name, component_name, parent_name=None, clazz=None):
		self.reset()
		self._window_name = window_name
		self._component_name = component_name
		self._parent_name = parent_name
		self._clazz = clazz

	def reset(self):
		self._property_names = None
		self._parent_name = None
		self._clazz = None
		self._label = None
		self._description = None
		self._children = None
		self._state = None
		self._obj_index = None
		self._child_index = None
		self._key_binding = None

	def __dir__(self):
		if self._property_names is None:
			self._property_names = ldtp.getobjectinfo(self._window_name, self._component_name)
			self._property_names = map(lambda p : 'clazz' if p == 'class' else p, self._property_names)
			self._property_names.append('state')
		return list(self._property_names)

	def __getitem__(self, item):

		if not isinstance(item, basestring):
			raise TypeError

		if item == 'window':
			return self.window
		elif item == 'key':
			return self.key
		elif item == 'parent':
			return self.parent
		elif item == 'clazz':
			return self.clazz
		elif item == 'label':
			return self.label
		elif item == 'description':
			return self.description
		elif item == 'children':
			return self.children
		elif item == 'child_index':
			return self.child_index
		elif item == 'obj_index':
			return self.obj_index
		elif item == 'key_binding':
			return self.key_binding
		elif item == 'state':
			return self.state
		else:
			raise KeyError, 'Unhandled key \'{0}\''.format(item)

	@property
	def window(self):
		return self._window_name

	@property
	def key(self):
		return self._component_name

	@property
	def parent(self):
		if self._parent_name is None:
			self._parent_name = ldtp.getobjectproperty(self._window_name, self._component_name, 'parent')
		return self._parent_name

	@property
	def clazz(self):
		if self._clazz is None:
			self._clazz = ldtp.getobjectproperty(self._window_name, self._component_name, 'class')
		return self._clazz

	@property
	def label(self):
		if self._label is None:
			self._label = ldtp.getobjectproperty(self._window_name, self._component_name, 'label')
		return self._label

	@property
	def description(self):
		if self._description is None:
			self._description = ldtp.getobjectproperty(self._window_name, self._component_name, 'description')
		return self._description

	@property
	def children(self):
		if self._children is None:
			self._children = ChildrenProxy(self._window_name, self._component_name,
				ldtp.getobjectproperty(self._window_name, self._component_name, 'children').split())
		return self._children

	@property
	def child_index(self):
		if self._child_index is None:
			self._child_index = ldtp.getobjectproperty(self._window_name, self._component_name, 'child_index')
		return self._child_index

	@property
	def obj_index(self):
		if self._obj_index is None:
			self._obj_index = ldtp.getobjectproperty(self._window_name, self._component_name, 'obj_index')
		return self._obj_index

	@property
	def key_binding(self):
		if self._key_binding is None:
			self._key_binding = ldtp.getobjectproperty(self._window_name, self._component_name, 'key_binding')
		return self._key_binding

	@property
	def state(self):
		if self._state is None:
			self._state = ldtp.getallstates(self._window_name, self._component_name)
		return self._state

	def __repr__(self):
		return self._component_name

	def __str__(self):
		return self._component_name

	def guiexist(self):
		return ldtp.guiexist(self._window_name, self._component_name)

	def find(self, path):

		logger.debug("Finding window='%s', component='%s', path=\"%s\"", self._window_name, self._component_name, path)

		pr = self.parser.parseString(path, parseAll=True)

		next_node = self
		for part_no, part in enumerate(pr):

			if 'dot' in part:
				pass # no op

			elif 'clazz' in part:

				#  TODO add backtracking ?

				for child_no, child in enumerate(next_node.children):
					next_node = None
					if part.clazz == child.clazz:
						if 'condition' in part:
							if 'index' in part.condition and int(part.condition.index) == child_no:
								next_node = child
								logger.info("Matched on index - part=%s", part)
							elif 'subexp' in part.condition:
								all_conditions_matched = True
								for subexp in part.condition:
									if str(child[subexp.prop]) != str(subexp.value):
										logger.debug("Unmatched prop - #=%i, clazz='%s', prop='%s', value='%s', found='%s'", child_no, part.clazz, subexp.prop, subexp.value, child[subexp.prop])
										all_conditions_matched = False
										break
								if all_conditions_matched:
									next_node = child
									logger.debug("Matched clazz and conditions - #=%i, clazz='%s', condition=%s", child_no, part.clazz, part.condition)
						else:
							next_node = child
							logger.debug("Matched clazz - #=%i, clazz='%s'", child_no, part.clazz)
					else:
						logger.debug("Unmatched clazz - #=%i, clazz='%s'", child_no, child.clazz)

					if next_node is not None:
						break

				if next_node is None:
					return None

		return next_node

	def print_details(self, indent=0, depth=6):

		def _print(widget, indent, depth, buffer=[]):

			props = dir(widget)

			children = []
			if 'children' in props:
				props.remove('children')
				children = widget['children']

			state = []
			if 'state' in props:
				props.remove('state')
				# state = widget['state']

			buffer.append((' ' * indent) + '\'' + widget.key + '\' : {')
			for i, prop in enumerate(props):
				if prop == 'key' or prop == 'parent':
					pass
				else:
					if i > 0:
						buffer.append(',')
					buffer.append('\'{0}\' : \'{1}\''.format(prop, widget[prop]))

			# if no further recursion - print children names only
			if children and indent >= depth:
				buffer.append(', \'children\' : {0}'.format(children.get_names()))

			buffer.append(' }')

			if state:
				buffer.append(str(state))

			buffer.append('\n')

			# recurse to handle children
			if indent < depth:
				for c in children:
					_print(c, indent+1, depth, buffer)

			return buffer

		for s in _print(self, indent, depth):
			print s,

class Table(Widget):

	def __init__(self, window_name, component_name, parent_name=None, clazz=None):
		super(Table, self).__init__(window_name, component_name, parent_name=parent_name, clazz=clazz)

	def selectrowindex(self, index):
		assert ldtp.selectrowindex(self._window_name, self._component_name, index) == 1

	def getrowcount(self):
		return ldtp.getrowcount(self._window_name, self._component_name)

	def getcellvalue(self, row_index, column = 0):
		return ldtp.getcellvalue(self._window_name, self._component_name, row_index, column)

	def selectrow(self, value_of_first_column):
		assert ldtp.selectrow(self._window_name, self._component_name, value_of_first_column) == 1

class Notebook(Widget):

	def __init__(self, window_name, component_name, parent_name=None, clazz=None):
		super(Notebook, self).__init__(window_name, component_name, parent_name=parent_name, clazz=clazz)

	def selecttabindex(self, tab_index):
		assert ldtp.selecttabindex(self._window_name, self._component_name, tab_index) == 1

class Clickable(Widget):

	def __init__(self, window_name, component_name, parent_name=None, clazz=None):
		super(Clickable, self).__init__(window_name, component_name, parent_name=parent_name, clazz=clazz)

	def click(self):
		assert ldtp.click(self._window_name, self._component_name) == 1

class Menu(Clickable):

	def __init__(self, window_name, component_name, parent_name=None, clazz=None):
		super(Menu, self).__init__(window_name, component_name, parent_name=parent_name, clazz=clazz)

	def enabled(self):
		return ldtp.menuitemenabled(self._window_name, self._component_name) == 1

class Text(Widget):

	def __init__(self, window_name, component_name, parent_name=None, clazz=None):
		super(Text, self).__init__(window_name, component_name, parent_name=parent_name, clazz=clazz)

	def enterstring(self, text):
		assert ldtp.enterstring(self._window_name, self._component_name, text) == 1

def generatekeyevent(event):
	assert ldtp.generatekeyevent(event) == 1

def click(window_name, object_name):
	assert ldtp.click(window_name, object_name) == 1

def waittillguiexist(window_name, object_name='', guiTimeOut=30, state=''):
	time.sleep(1)
	assert ldtp.waittillguiexist(window_name, object_name, guiTimeOut, state) == 1

def waittillguinotexist(window_name, object_name='', guiTimeOut=30):
	time.sleep(1)
	assert ldtp.waittillguinotexist(window_name, object_name, guiTimeOut) == 1

def onwindowcreate(window_name):
	assert ldtp.onwindowcreate(window_name) == 1

def poll_events():
	return ldtp.poll_events()

if __name__ == "__main__":

	import sys

	if len(sys.argv) != 2:
		print "Window name needs to be passsed as only argument"
		sys.exit()

	object_name = sys.argv[1]
	print "Processing window: '" + object_name + "'"
	widget = create(object_name, object_name)
	widget.print_details(indent=0, depth=8)
