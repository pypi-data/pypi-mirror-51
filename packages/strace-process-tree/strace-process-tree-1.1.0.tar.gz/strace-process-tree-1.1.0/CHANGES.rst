Changes
=======


1.1.0 (2019-08-22)
------------------

* Show process running times when the strace log has timestamps
  (i.e. -t/-tt/ -ttt was passed to strace).
* Fix tree construction to avoid duplicating processes when execve()
  shows up in the log before the parent's clone() resumes.


1.0.0 (2019-08-21)
------------------

* Moved to its own repository on GitHub, added a README and this changelog.
* First release to PyPI.


0.9.0 (2019-08-01)
------------------

* Use Python 3 by default.


0.8.0 (2019-06-05)
------------------

* Parse more strace log variations: pids shown as "[pid NNN]", timestamps
  formatted as "HH:MM:SS.ssss" (strace -t/-tt versus -ttt that we already
  handled).


0.7.0 (2019-04-10)
------------------

* Do not lose information on repeated execve() calls.


0.6.2 (2019-04-10)
------------------

* PEP-8 and slight readability refactoring.


0.6.1 (2018-05-19)
------------------

* New strace in Ubuntu 18.04 LTS formats its log files differently.
* Recognize fork().


0.6.0 (2018-01-19)
------------------

* Use argparse, add help message.
* Better error reporting.
* Print just the command lines instead of execve() system call arguments
  (pass -v/--verbose if you want to see full execve() calls like before).
* execve() is more important than clone().
* Distinguish threads from forks.
* This was the last version released as a Gist.  Newer versions were available
  from `my scripts repository
  <https://github.com/mgedmin/scripts/blob/master/strace-process-tree>`__.


0.5.1 (2016-12-07)
------------------

* Strip trailing whitespace in output.


0.5.0 (2015-12-01)
------------------

* Handle strace -T output.
* Simplify clone() args in output.


0.4.0 (2015-11-18)
------------------

* Support vfork() and fork().


0.3.0 (2015-11-13)
------------------

* Support optional timestamps (strace -ttt).


0.2.3 (2014-11-14)
------------------

* Recommend strace options in --help message.
* Add a file containing example output.


0.2.2 (2013-05-29)
------------------

* Fix strace files that have two spaces between pid and event.


0.2.1 (2013-02-27)
------------------

* Add output example.
* Fix incorrect assumption that strace files always had two spaces between the
  pid and the event.


0.2 (2013-02-15)
----------------

* Add Unicode line art.


0.1 (2013-02-14)
----------------

* First public release as a GitHub Gist at
  https://gist.github.com/mgedmin/4953427
