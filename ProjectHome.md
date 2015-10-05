This is the "Make-and-Run" plugin for Gedit.

# Update #

Now a gtk3 port exists in the svn.


# Background #

I've been learning Python and GTK in the last weeks and made this plugin to have a better programming environment for it in GEdit. I also use C/C++, so the plugin supports these languages too.

# What the plugin can do #

Make-and-Run can run "make" on your source code file (if it doesn't find a Makefile on your source code's directory, it popups a window to create one for you), it can also directly compile the current file (either thru "gcc -c <your currentfile>" or g++ etc). It can, also, run the file thru a special make target (for example, "make exec") and throw the process in a separate gnome-terminal window. If your file is a python source code, it can also run it inside a special python-specific "running" window, displaying the stdout/stderr from your python-program.

I do not want a very complex "for-every-type-of-big-project" environment. I just want to open my favorite text editor, write some simple C or Python code (specially for my homeworks which often use OpenGL) and click a "Run" or "Compile" button that does the thing for me.

# Portuguese #

The plugin currently has all messages in portuguese, but I do want to release it in other languages too. This is one point that I might need some help! ;)

# Screenshots #

Here are several screenshots to present the plugin. Note that they are all in portuguese.

![http://gedit-plugin-make-and-run.googlecode.com/svn/trunk/Screenshots/screenshot_001.png](http://gedit-plugin-make-and-run.googlecode.com/svn/trunk/Screenshots/screenshot_001.png)

![http://gedit-plugin-make-and-run.googlecode.com/svn/trunk/Screenshots/screenshot_002.png](http://gedit-plugin-make-and-run.googlecode.com/svn/trunk/Screenshots/screenshot_002.png)

![http://gedit-plugin-make-and-run.googlecode.com/svn/trunk/Screenshots/screenshot_003.png](http://gedit-plugin-make-and-run.googlecode.com/svn/trunk/Screenshots/screenshot_003.png)

![http://gedit-plugin-make-and-run.googlecode.com/svn/trunk/Screenshots/screenshot_004.png](http://gedit-plugin-make-and-run.googlecode.com/svn/trunk/Screenshots/screenshot_004.png)

![http://gedit-plugin-make-and-run.googlecode.com/svn/trunk/Screenshots/screenshot_005.png](http://gedit-plugin-make-and-run.googlecode.com/svn/trunk/Screenshots/screenshot_005.png)

![http://gedit-plugin-make-and-run.googlecode.com/svn/trunk/Screenshots/screenshot_006.png](http://gedit-plugin-make-and-run.googlecode.com/svn/trunk/Screenshots/screenshot_006.png)

![http://gedit-plugin-make-and-run.googlecode.com/svn/trunk/Screenshots/screenshot_007.png](http://gedit-plugin-make-and-run.googlecode.com/svn/trunk/Screenshots/screenshot_007.png)

![http://gedit-plugin-make-and-run.googlecode.com/svn/trunk/Screenshots/screenshot_008.png](http://gedit-plugin-make-and-run.googlecode.com/svn/trunk/Screenshots/screenshot_008.png)

![http://gedit-plugin-make-and-run.googlecode.com/svn/trunk/Screenshots/screenshot_009.png](http://gedit-plugin-make-and-run.googlecode.com/svn/trunk/Screenshots/screenshot_009.png)

# Credits #

I've used Glade, Gedit and Devhelp very much. I also have been using several Gedit plugins, which are the true source for this "home-made-for-personal-use" plugin. I would like to thank very much all the gedit plugin makers out there.