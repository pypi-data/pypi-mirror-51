# TextConfig

TextConfig is a Class for managing simple text configuration files with
python. By simple, it means that they are simple text files, there are
no sections and all options in the configuration files use a strict

```
OPTION=value
```

format, with no spaces between `OPTION`, `=` and `value`.
The same `OPTION` can be used more than once, so you can have multiple
values, for example:

```
EXAMPLE=one
EXAMPLE=two
```

Here's a real-world example of such a file, taken from the `slapt-get` package
manager repository configuration file in Salix:

```
# Working directory for local storage/cache.
WORKINGDIR=/var/slapt-get

# Exclude package names and expressions.
# To exclude pre and beta packages, add this to the exclude:
#   [0-9\_\.\-]{1}pre[0-9\-\.\-]{1}
EXCLUDE=^aaa_elflibs,^aaa_base,^devs,^glibc.*,^kernel-.*,^rootuser-settings,^zzz-settings.*,-i?86-

# The Slackware repositories, including dependency information
SOURCE=http://www.mirrorservice.org/sites/download.salixos.org/x86_64/slackware-14.2/:OFFICIAL
SOURCE=http://www.mirrorservice.org/sites/download.salixos.org/x86_64/slackware-14.2/extra/:OFFICIAL

# The Salix repository
SOURCE=http://www.mirrorservice.org/sites/download.salixos.org/x86_64/14.2/:PREFERRED
# And the Salix extra repository
SOURCE=http://www.mirrorservice.org/sites/download.salixos.org/x86_64/extra-14.2/:OFFICIAL
```

You may call it like this:

```
from textconfig import TextConfig
c = TextConfig('/path/to/configfile')
```

