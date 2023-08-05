*** Settings ***

Library   OperatingSystem
Library   String

Resource   ./ipython.robot


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
   ...   re.escape(path.Path(morepy.magic.__file__).realpath().rstrip('c'))
   ...   modules=re, path, morepy

   Should Match Regexp   ${output}
   ...   ^ARG: ${source file}:17

Run %dev --editor
   ${result}   ${output} =   Run IPython Process
   ...   import sys
   ...   sys.path.remove("")
   ...   %load_ext morepy
   ...   from morepy.magic import dev
   ...   %dev --editor echo dev.__func__

   ${source file} =   Evaluate
   ...   re.escape(path.Path(morepy.magic.__file__).realpath().rstrip('c'))
   ...   modules=re, path, morepy

   Should Match Regexp   ${output}
   ...   ^"?${source file}:17"?

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
   ...   re.escape(path.Path(morepy.magic.__file__).realpath().rstrip('c'))
   ...   modules=re, path, morepy

   Should Match Regexp   ${output}
   ...   ^ARG: FILE:${source file}:LINE:17

Run %dev --editor --format
   ${result}   ${output} =   Run IPython Process
   ...   import sys
   ...   sys.path.remove("")
   ...   %load_ext morepy
   ...   from morepy.magic import dev
   ...   %dev --editor echo --format FILE:{file}:LINE:{line} dev.__func__

   ${source file} =   Evaluate
   ...   re.escape(path.Path(morepy.magic.__file__).realpath().rstrip('c'))
   ...   modules=re, path, morepy

   Should Match Regexp   ${output}
   ...   ^"?FILE:${source file}:LINE:17"?
