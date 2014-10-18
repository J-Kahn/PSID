PSID
====

Code for downloading and interpreting Panel Study of Income Dynamics data in python. The PSID is a household survey conducted by the Institute for Social Research at the University of Michigan. It has been running since 1968 and covers 5,000 individuals. The survey has been very popular in the social sciences.

Users must first register at http://psidonline.isr.umich.edu/

Editing "download.py", the user can set the target directory. They must also set their user name and password from the registration. The program will download files, and convert them to .csv using a python interpreter for .sas import code. It will also create a subdirectory for code books.

TODO: create panels.
