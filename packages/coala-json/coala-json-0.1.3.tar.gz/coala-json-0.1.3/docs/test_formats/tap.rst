TAP
===

TAP or the Test Anything Protocol is a line based test result report format.
Many software and libraries of various language like C, Python, Java can
consume TAP and do something useful with it. Jenkins can also produce
insightful reports by using the TAP test files.

How to upload TAP to Jenkins:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use the TAP Plugin to generate reports from TAP files. To use the
plugin, from your Jenkins dashboard go to Manage Jenkins -> Manage Plugins and
then you can easily install it by searching the plugin in the *available*
plugins tab.

Configuration:

- Install the Jenkins TAP Plug-in using the Plug-in Manager
- Check the option to publish TAP in your post build actions option in job
  configuration, configure a pattern (and other settings)
- Execute your build and analyze the results

For more information visit: https://wiki.jenkins.io/display/JENKINS/TAP+Plugin

If everything works out a 'TAP Test Results' and a 'TAP Extended Test Results'
field will appear on your Jenkins build panel. The reports might look something
like this:

TAP Test Results:

.. image:: ../_static/images/jenkins_tap.png
   :align: center

TAP Extended Test Results:

.. image:: ../_static/images/jenkins_tap_extended.png
   :align: center
