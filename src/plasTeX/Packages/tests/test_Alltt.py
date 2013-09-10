#!/usr/bin/env python

import unittest
import os
import tempfile
import shutil
from plasTeX.TeX import TeX
from unittest import TestCase
from bs4 import BeautifulSoup as Soup

from hamcrest import assert_that
from hamcrest import has_property
from hamcrest import contains

class TestAlltt(TestCase):

	def runDocument(self, content):
		"""
		Compile a document with the given content

		Arguments:
		content - string containing the content of the document

		Returns: TeX document

		"""
		tex = TeX()
		tex.disableLogging()
		tex.input(r'''\document{article}\usepackage{alltt}\begin{document}%s\end{document}''' % content)
		return tex.parse()

	def runPreformat(self, content):
		"""
		This method compiles and renders a document fragment and
		returns the result

		Arguments:
		content - string containing the document fragment

		Returns: content of output file

		"""
		# Create document file
		document = r'\documentclass{article}\usepackage{alltt}\begin{document}%s\end{document}' % content
		tmpdir = tempfile.mkdtemp()
		filename = os.path.join(tmpdir, 'longtable.tex')
		open(filename, 'w').write(document)

		# Run plastex on the document
		log = os.popen('plastex -d %s %s 2>&1' % (tmpdir, filename)).read()


		# Get output file
		output = open(os.path.join(tmpdir, 'index.html')).read()

		# Clean up
		shutil.rmtree(tmpdir)
		os.remove('longtable.paux')

		return Soup(output).findAll('pre')[-1]

	def testSimple(self):
		text = '''\\begin{alltt}\n\t line 1\n\tline 2\n   line 3\n\\end{alltt}'''
		lines = ['', '\t line 1', '\tline 2', '   line 3', '']

		# Test text content of node
		out = self.runDocument(text).getElementsByTagName('alltt')[0]

		plines = out.textContent.split('\n')
		assert_that( plines, contains(*lines) )

		# Test text content of rendering
		out = self.runPreformat(text)

		plines = out.string.split('\n')
		assert lines == plines, 'Content doesn\'t match - %s - %s' % (lines, plines)


	def testCommands(self):
		text = '''\\begin{alltt}\n\t line 1\n\t \\textbf{line} 2\n\t \\textit{line 3}\n\\end{alltt}'''
		lines = ['', '\t line 1', '\t line 2', '\t line 3', '']

		# Test text content of node
		doc = self.runDocument(text)
		out = doc.getElementsByTagName('alltt')[0]

		plines = out.textContent.split('\n')
		__traceback_info__ = text, lines, out, plines
		assert_that( plines, contains(*lines) )

		bf = out.getElementsByTagName('textbf')[0]
		assert_that( bf, has_property( 'textContent', 'line' ), 'Bold text should be "line", but it is "%s"' % bf.textContent)

		it = out.getElementsByTagName('textit')[0]
		assert it.textContent == 'line 3', 'Italic text should be "line 3", but it is "%s"' % it.textContent

		# Test rendering
		out = self.runPreformat(text)

		assert out.b.string == 'line', 'Bold text should be "line", but it is "%s"' % out.b.string

		assert out.i.string == 'line 3', 'Italic text should be "line 3", but it is "%s"' % out.i.string


if __name__ == '__main__':
	unittest.main()
