### 0.1.0

* Provide `morepy` extension for IPython, which:

  * Installs a magic `%dev` function that opens the source locations of given
    objects in an editor of the user's choice with customizable argument
    format for the editor command
  * Is loadable via either calling `%load_ext morepy` in the IPython shell or
    calling `morepy.load(shell)` from another extension's
    `load_ipython_extension(shell)` entry function
