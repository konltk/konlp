# How to make documentaion of konlp

First, Normally use like the command, "sphinx-build -b html sourcedir builddir"

But in our case, we have to run like this :

> sphinx-apidoc -f -o \_source ../konlp

Finally, run the following to get html files :

> make html

**But If you want to do two stages at runnig a command**

type in like this :

> make apidoc


# Reference 

 - [Sphinx-doc quickstart](http://www.sphinx-doc.org/en/master/usage/quickstart.html)
 - [How to use google doc style with sphinx extension](http://www.sphinx-doc.org/en/master/ext/napoleon.html)
