.. image:: https://travis-ci.org/NextThought/nti.plasTeX.svg?branch=master
    :target: https://travis-ci.org/NextThought/nti.plasTeX

.. note:: This README, while providing a basic introduction, is probably
		  outdated in many important ways in the context of this fork.

Installation of this package is done just like any other modern Python
package. See the INSTALL file for details.

Once you have plasTeX installed, you can use the command-line utility,
called "plastex" just like latex or pdflatex.  For example, if you
have a LaTeX file called mybook.tex, simply run::

    plastex mybook.tex

This will convert mybook.tex into XHTML (the default renderer).  Of course,
there are many options to control the execution of plastex.  Simply type
"plastex" on the command line without options or arguments to see the
full list of command-line options.

It is also possible to write your own command-line utilities that leverage
the power of the plasTeX framework.  In fact, the essence of the "plastex"
command can be written in just one line of code (not including the Python
import commands)::

    import sys
    from plasTeX.TeX import TeX
    from plasTeX.Renderers.XHTML import Renderer
    Renderer().render(TeX(file=sys.argv[1]).parse())

plasTeX is really much more than just a LaTeX-to-other-format converter
though.  See the documentation at http://plastex.sf.net/ for a complete
view of what it is capable of.
