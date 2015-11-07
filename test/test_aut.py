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
import pyparsing
import unittest

import aut

logger = logging.getLogger(__name__)

class AUTTest(unittest.TestCase):

	def test_parsing(self):

		logger.info('Starting \'{0}\''.format(inspect.stack()[0][3]))

		parser = aut._build_parser()

		pass_tests = [
			"foo",
			"foo-bar",
			"foo[1]",
			"foo[@prop='']",
			"foo[@prop='value']",
			"foo[@prop='dont-get-confused[1]']",
			"foo[@prop='aaa\\'bbb']",
			"foo[@prop='aaa\\bbb']",
			"foo[@prop='aaa\\\\bbb']",
			"foo[@special-prop='value']",
			"foo[@special-prop='long text']",
			"foo[@special-prop='long text' and @prop='text']",
			"foo[@special-prop='long text' and @prop='text' and @more='stuff']",

			".",
			"./foo",
			"./foo-bar",
			"./foo[1]",
			"./foo[@prop='value']",
			"./foo[@special-prop='value']",
			"./foo[@special-prop='long text']",
			"./foo[@special-prop='long text']/bar[1]/more",

			" foo [ 1 ] ",
			" foo [ @ prop = 'value' ] ",
			" foo [ @ special-prop = 'long text' and @ prop = 'text' ] ",

			" . ",
			" . / foo ",
			" . / foo [ 1 ] ",
			" . / foo [ @ special-prop = 'long text' ] / bar [ 1 ] / more ",
		]

		for t in pass_tests:
			try:
				results = parser.parseString(t, parseAll=True)
				# print t,"->", results
				self.assertIsNot(results, None)
			except pyparsing.ParseException, pe:
				self.fail(str(t) + " -> UNEXPECTED ERROR: " + str(pe))

		fail_tests = [
			"",
			"/foo-bar",
			"foo[a]",
			"foo[special_prop='value']",
			"foo[1 and special_prop='value']",
			"foo[special_prop='value' and 1]",
			"foo[special_prop='value' or @foo='bar']",
			"foo[@special_prop='aaa'bbb']",
		]

		for t in fail_tests:
			try:
				results = parser.parseString(t, parseAll=True)
				self.fail(str(t) + " -> UNEXPECTED PASS: " + str(results))
			except pyparsing.ParseException, pe:
				# print t,"-> EXPECTED ERROR:", pe
				pass

	def test_parsing_result_01(self):

		parser = aut._build_parser()

		pr = parser.parseString(".", parseAll=True)
		self.assertEquals(len(pr), 1)
		r = pr[0]
		self.assertItemsEqual(r.keys(), ['dot'])
		self.assertEquals(r.dot, '.')

	def test_parsing_result_02(self):

		parser = aut._build_parser()

		pr = parser.parseString("foo", parseAll=True)
		self.assertEquals(len(pr), 1)

		r = pr[0]
		self.assertItemsEqual(r.keys(), ['clazz'])
		self.assertEquals(r.clazz, 'foo')

	def test_parsing_result_03(self):

		parser = aut._build_parser()

		pr = parser.parseString("foo[1]", parseAll=True)
		self.assertEquals(len(pr), 1)

		r = pr[0]
		self.assertItemsEqual(r.keys(), ['clazz', 'condition'])
		self.assertEquals(r.clazz, 'foo')

		r = r.condition
		self.assertEquals(len(r), 1)
		self.assertEquals(r.keys(), ['index'])
		self.assertEquals(r.index, '1')

	def test_parsing_result_04(self):

		parser = aut._build_parser()

		pr = parser.parseString("foo[@p='v']", parseAll=True)
		self.assertEquals(len(pr), 1)

		r = pr[0]
		self.assertItemsEqual(r.keys(), ['clazz', 'condition'])
		self.assertEquals(r.clazz, 'foo')

		r = r.condition
		self.assertEquals(len(r), 1)
		self.assertEquals(r.keys(), ['subexp'])

		self.assertEquals(len(r[0]), 2)
		self.assertEquals(r[0].keys(), ['value', 'prop'])
		self.assertEquals(r[0].prop, 'p')
		self.assertEquals(r[0].value, 'v')

	def test_parsing_result_05(self):

		parser = aut._build_parser()

		pr = parser.parseString("foo[@p='v' and @x='y']", parseAll=True)
		self.assertEquals(len(pr), 1)

		r = pr[0]
		self.assertItemsEqual(r.keys(), ['clazz', 'condition'])
		self.assertEquals(r.clazz, 'foo')

		r = r.condition
		self.assertEquals(len(r), 2)
		self.assertEquals(r.keys(), ['subexp'])

		self.assertEquals(len(r[0]), 2)
		self.assertEquals(r[0].keys(), ['value', 'prop'])
		self.assertEquals(r[0].prop, 'p')
		self.assertEquals(r[0].value, 'v')

		self.assertEquals(len(r[1]), 2)
		self.assertEquals(r[1].keys(), ['value', 'prop'])
		self.assertEquals(r[1].prop, 'x')
		self.assertEquals(r[1].value, 'y')

	def test_parsing_result_06(self):

		parser = aut._build_parser()

		pr = parser.parseString("./foo[1]/bar", parseAll=True)
		self.assertEquals(len(pr), 3)
		r = pr[0]
		self.assertItemsEqual(r.keys(), ['dot'])
		self.assertEquals(r.dot, '.')

		r = pr[1]
		self.assertItemsEqual(r.keys(), ['clazz', 'condition'])
		self.assertEquals(r.clazz, 'foo')
		r = r.condition
		self.assertEquals(len(r), 1)
		self.assertEquals(r.keys(), ['index'])
		self.assertEquals(r.index, '1')

		r = pr[2]
		self.assertItemsEqual(r.keys(), ['clazz'])
		self.assertEquals(r.clazz, 'bar')

	def test_parsing_result_99(self):

		parser = aut._build_parser()

		pr = parser.parseString("foo[1]/./bar[@p='v' and @x='y']", parseAll=True)

		for part in pr:
			if 'dot' in part:
				print 'dot=.'
			elif 'clazz' in part:
				print 'clazz={0}'.format(part.clazz)
				if 'condition' in part:
					if 'index' in part.condition:
						print 'index={0}'.format(part.condition.index)
					elif 'subexp' in part.condition:
						for subexp in part.condition:
							print 'prop={0}, value={1}'.format(subexp.prop, subexp.value)
					else:
						raise Exception, 'Parse error: index or sub-expression expected'
			else:
				raise Exception, 'Parse error: dot or clazz expected'
