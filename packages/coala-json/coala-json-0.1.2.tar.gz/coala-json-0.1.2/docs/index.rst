.. meta::
   :description: coala-json provides utilities to convert json format into
    various test result formats like Junit, CheckStyle, TAP etc.  
   :keywords:    coala-json, static code analysis, linter

=============================
The coala-json documentation!
=============================

.. toctree::
   :caption: Home
   :hidden:

   Welcome <self>

.. toctree::
   :caption: Test Formats
   :hidden:

   JUnit <test_formats/junit>
   Checkstyle <test_formats/checkstyle>
   TAP <test_formats/tap>

.. toctree::
   :caption: Help
   :hidden:

   How To Get In Touch With Us <Help/Getting_In_Touch>

You might also want to look at `coala's website <http://coala.io/>`_.

coala-json: tools for test reports integration
==============================================

**coala-json holds a collection of useful utilities that are used
to read JSON output and convert it to other formats.**

Result format inconsistencies have been a problem for a long time. Converting
the static analysis results into a test results format has been done a few 
times, such as early PEP8 plugins to Jenkins. The mapping isn’t exact, but the 
benefits of using the test result format are tight integration with various
CI/CD systems. This module will thus help you to convert your results in json 
format to many useful test results format easily.

.. image:: _static/images/no_tests.png
   :align: center

Usually when your tests fail you have to look through the builds in search of
the failures but with our reporter tool your can see your test summary
automatically in front of you. After using the coala reporter tool your CI will
show test results
automatically in their respective *Tests* tab.

CircleCI:

.. image:: _static/images/circleci_tests.png
   :align: center

AppVeyor:

.. image:: _static/images/appveyor_tests.png
   :align: center

Jenkins:

.. image:: _static/images/jenkins_tests.png
   :align: center
