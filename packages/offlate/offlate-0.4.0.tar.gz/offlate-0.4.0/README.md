Offlate
=======

Offlate is a translation interface for offline translation of projects using
online platforms. Its features include:

* Finding your project and configuring it
* Offline translation
* Submission to your upstream's favorite platform

How to Use?
-----------

Some projects are already available. All you need to do is to open the `new`
menu and select your project from there. If your project is not available, you
can still create a new project with name, a language and a translation system.

The translation system is one of the following methods of sending your work to
upstream:

Currently Supported Platforms
-----------------------------

Offlate currently supports getting translations from and sending them to the
[Translation Project](https://translationproject.org),
[Transifex](https://transifex.org) and any [Gitlab](https://gitlab.com)
instance.

Transifex only allows us to translate files in their original formats, so
we only support transifex projects for which we support the format. See the
following section for more info on supported formats.

Gitlab is a free source code forge designed for developpers, not translators.
It is used by developpers to keep their sources together, and this is where
translations ultimately go (unless developpers use a different forge). Using
gitlab or any other forge is a last resort when the developpers do not use
a platform already. Make sure you visite their repository and project page
to learn about their prefered translation workflow.

As with Transifex, the Gitlab system can only get translation files in their
original format, so the system is limited to formats supported by the
application. When sending your work upstream with this system, offlate will
use your account on the instance used by the project to create a new project
in your user space, clone the upstream project, create a new branch on your
namespace and send a merge request to the upstream project, so they can
review your changes before accepting them.

Currently Supported Formats
---------------------------

Currently, offlate supports gettext files (.po), qt translation format (.ts)
and Yaml files.
