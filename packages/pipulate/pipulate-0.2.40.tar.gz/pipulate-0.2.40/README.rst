:Author: `Mike Levin SEO in NYC, Commodore & 360i alum, HitTail creator, J2 Global employee. <http://mikelev.in>`_

Pipulate Free & Open Source SEO Software (Automate GSheets for Dashboards)
##########################################################################

.. image:: https://raw.githubusercontent.com/miklevin/Pipulate/master/pipulate-logo.svg?sanitize=true

- Do you make Spreadsheet Reports using Google Analytics, GSC and other Data?
- Are you using expensive plug-ins or products to keep these Reports Updated?
- Do you feel all this stuff should be FREE if only you could wire it all up?

Then It's Time To Learn a Little Python!
========================================

Pipulate is designed to make playing with data in Jupyter Notebook easy. The
easiest way to install Pipulate from Jupyter is to execute these commands from
within a Notebook::

    import sys
    !{sys.executable} -m pip install --upgrade --no-cache-dir pipulate

If you're not using Anaconda, then you will have to install Pandas first. But
you should really be using Anaconda.

The first time you import Pipulate, you will receive a Google OAuth prompt to
allow access to the Google Spreadsheet you want to edit.  Click the big link
and paste the resulting token back into the field shown in Jupyter Notebook or
your command-line. Once this is done, the basic use is::

    import pipulate as gs
    cl, df = gs.pipulate(tab, rows, cols)
    # Do stuff to df
    gs.populate(tab, cl, df)

This loads the rectangular region you defined with the rows and columns into
memory in a way where you can treat it a lot like a tab in Microsoft Excel or
table in SQL. You can manipulate the pandas "DataFrame" (abbreviated as df),
and then push the changes back out to the Google Sheet. For example::

    import pipulate as gs
    sheet = gs.key('119mnC8Day78KexU_yv7J_wfA3p7iZeXa0YEtmg1Igu4')  # your key
    tab = sheet.worksheet('Sheet1')
    cl, df = gs.pipulate(tab, rows=(1, 5), cols=('A', 'C'))
    df['A'] = 'foo'
    df['B'] = 'bar'
    df['C'] = df['A'] + df['B']
    gs.populate(tab, cl, df)  # Watch the sheet update :)

And that's it. All Pipulate does is pull down the rectangular cell-range you
define and plop it into df. What you do with the Pandas DataFrame (df) is up to
you. I'll load the examples directory with ideas, but this is very open-ended,
designed to make automation of traditional tedious tasks in SEO much simpler.
Once you're happy with your script, you can copy/paste it into a .py file and
schedule it with a standard Linux scheduler, which is another part of this
project I'll be expanding considerably (generic task-scheduling under Linux).

Parametrizing Your Arguments for Scheduling
===========================================

The time has come the Walrus said to talk about automation. After you get your
script working in Jupyter Notebook what are you going to do? Unless you want to
sit there and press a button every day like in Lost, then you're going to have
to put the code in some sort of scheduling system. When you do this, it is best
to do it in a parameterized fashion, meaning you can feed the one script
different sites, Google Analytics IDs, keywords, filters and whatnot; allowing
the same code to drive different dashboards. 

Generic Linux script scheduling is too much to cover here, but I may as well
show you how to develop with parameterized arguments in Jupyter Notebook then
have those same arguments able to be used on the command-line when invoked from
scheduling. So if you have filename.ipynb (A Jupyter Notebook) and you
copy/paste its content into filename.py, then you can change its internal
variable values by the way you run it form the Unix shell, thereby using it to
drive many different Google Sheet dashboards. You're welcome::

    (py36) MikeL@LunderVand:$ filename.py --kung "foo"
    kung: foo

You can alternatively use::

    (py36) MikeL@LunderVand:$ filename.py -k "foo"
    kung: foo

To support more arguments, just make more of the parser.add_argument() function
calls and access them through the args dictionary. Here's the code in
filename.py in the above commands. When this is run from Jupyter Notebook, the
"foo" value is set in the "if jn:" if-block. It's fairly likely you'll have
code like this at the top of any Pipulate script that starts out in Jupyter
Notebook and is destined for scheduling. Clear? Enjoy!::

    name = 'kung'
    jn = True
    try:
        get_ipython()
    except NameError:
        jn = False
    if jn:
        val = 'foo'
    else:
        import argparse
        parser = argparse.ArgumentParser(description='Parses args when run from console.')
        parser.add_argument('-k','--kung', default='foo', help='', required=False)
        args = vars(parser.parse_args())
        val = args[name]
    print('%s: %s' % (name, val))

Fear Is The Mind Killer
=======================

Why do I call Google Sheets automation components "SEO software"? It's because
this is the main missing ingredient in building all those custom reports
necessary to surface new actionable data every day. It's also your easy route
into data manipulation with Python/Pandas and the repurposing of your aging SEO
career into something simultaneously more timely and timeless. SEO is dead.
Long live SEO! Sound familiar? Well, the other shoe is finally dropping with
all the Machine Learning tricks ol' Uncle Google is learning, and if you're a
dinosaur then y'all better learn to fly. If you can do Excel macros, then you
can survive, evolve and thrive.

Learning Linux, Python, vim and git (LPvg) will set you on a good course for at
least the next 10-years. If you're still scared of the Unix shell, that old
text-based command-line interface which is both the past and future of tech,
then stick your hand into the Gom Jabbar pain-box of Linux and cut your teeth
on my other repo here on Github `Levinux <https://github.com/miklevin/levinux>`_.
Now repeat after me: I must not fear. Fear is the mind-killer. Fear is the
little-death that brings total obliteration. I will face my fear. I will permit
it to pass over me and through me.

.. image:: https://raw.githubusercontent.com/miklevin/Pipulate/master/mike-levin-seo-nyc.png
