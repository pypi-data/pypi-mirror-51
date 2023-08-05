*** Settings ***

Library   OperatingSystem
Library   String

Resource   ./ipython.robot

Suite Setup   Run Keyword If   "" in sys.path
...   Evaluate   sys.path.remove("")   modules=sys


*** Test Cases ***

Run %dev w/o flags
   ${python} =   Evaluate   sys.executable   modules=sys
   Set Environment Variable   EDITOR
   ...   "${python}" -c "import sys; print('ARG: {}'.format(sys.argv[1]))"

   ${result}   ${output} =   Run IPython Process
   ...   import sys
   ...   sys.path.remove("")
   ...   %load_ext morepy
   ...   from morepy.magic import dev
   ...   %dev dev.__func__

   ${source file} =   Evaluate
   ...   path.Path(morepy.magic.__file__).realpath().normcase().rstrip('c')
   ...   modules=path, morepy
   ${source file regexp} =   Evaluate   re.escape("${source file}")
   ...   modules=re

   Should Match Regexp   ${output}
   ...   ^ARG: ${source file regexp}:17

Run %dev --editor
   ${result}   ${output} =   Run IPython Process
   ...   import sys
   ...   sys.path.remove("")
   ...   %load_ext morepy
   ...   from morepy.magic import dev
   ...   %dev --editor echo dev.__func__

   ${source file} =   Evaluate
   ...   path.Path(morepy.magic.__file__).realpath().normcase().rstrip('c')
   ...   modules=path, morepy
   ${source file regexp} =   Evaluate   re.escape("${source file}")
   ...   modules=re

   Should Match Regexp   ${output}
   ...   ^"?${source file regexp}:17"?

Run %dev --format
   ${python} =   Evaluate   sys.executable   modules=sys
   Set Environment Variable   EDITOR
   ...   "${python}" -c "import sys; print('ARG: {}'.format(sys.argv[1]))"

   ${result}   ${output} =   Run IPython Process
   ...   import sys
   ...   sys.path.remove("")
   ...   %load_ext morepy
   ...   from morepy.magic import dev
   ...   %dev --format FILE:{file}:LINE:{line} dev.__func__

   ${source file} =   Evaluate
   ...   path.Path(morepy.magic.__file__).realpath().normcase().rstrip('c')
   ...   modules=path, morepy
   ${source file regexp} =   Evaluate   re.escape("${source file}")
   ...   modules=re

   Should Match Regexp   ${output}
   ...   ^ARG: FILE:${source file regexp}:LINE:17

Run %dev --editor --format
   ${result}   ${output} =   Run IPython Process
   ...   import sys
   ...   sys.path.remove("")
   ...   %load_ext morepy
   ...   from morepy.magic import dev
   ...   %dev --editor echo --format FILE:{file}:LINE:{line} dev.__func__

   ${source file} =   Evaluate
   ...   path.Path(morepy.magic.__file__).realpath().normcase().rstrip('c')
   ...   modules=path, morepy
   ${source file regexp} =   Evaluate   re.escape("${source file}")
   ...   modules=re

   Should Match Regexp   ${output}
   ...   ^"?FILE:${source file regexp}:LINE:17"?
