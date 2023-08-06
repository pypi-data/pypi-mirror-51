Checkstyle
==========

Checkstyle is another widely used xml based test format. The report can be
divided into a three parts or information sections. They are:

- **files:** which shows the list of files in which the violations have
  happened.
- **rules:** that shows overview of the rules that were used to check for
  violations.
- **details** that provide the details of the violations that have happened.
  This generally contains the line number, severity, error messages and other
  such information.

How to upload Checkstyle to Jenkins:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Checkstyle report is supported by the Warnings Next Generation Plugin. To use
the plugin, from your Jenkins dashboard go to Manage Jenkins -> Manage Plugins
and then you can easily install it by searching the plugin in the *available*
plugins tab.

The configuration of the plugin is the same for all Jenkins job types. It is
enabled in the UI by adding the post build action 'Record compiler warnings and
static analysis results' to your job. In pipelines the plugin will be activated
by adding the step ``recordIssues``.
The basic configuration of the plugin is shown in the image above:

.. image:: ../_static/images/checkstyle_config.png
   :align: center

You need to specify the pattern of the report files that should be parsed and
scanned for issues. If you do not specify a pattern, then the console log of
your build will be scanned.

For additional information on Warning Next Gen Plugin configuration settings
you can visit the `plugin documentation <https://github.com/jenkinsci/warnings-ng-plugin/blob/master/doc/Documentation.md>`_.
If everything works out a 'Checkstyle Warnings' field will appear on your
Jenkins build panel. The report might look something like this:

.. image:: ../_static/images/jenkins_checkstyle_report.png
   :align: center
