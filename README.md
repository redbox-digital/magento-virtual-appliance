

Let's start with a mission statement:

> I want for any developer, on any system, to have no technical
> impediment to starting work within one hour.

A few caveats:

+ Any system means Windows, OS X, or Linux.
+ There may be other impediments, but it will not be that project
  setup was impossible.

We will achieve this using Vagrant. Our priority right now is not
the benefits that come with dev-prod parity, although we should bear
all of that in mind. The focus is simply a development environment that
makes no assumptions of the developer.

There are many facets to consider, and many compromises that have be
made. These are things that are requirements.

+ A developer should be allowed to edit code on the host machine, with
  their preferred editor
+ A developer should at the very least have the ability to commit and
  push code from the host
+ The guest machine should have a working web server that shows the
  current state of the project.

These are things we should optimise for, in descending order of
importance.

+ Performance of shared filesystem (to a point)
+ Number of software requirements on host
+ Amount needed to learn

The exact technical details are not important. Currently, the biggest
foreseen problem is that Virtualbox shared folder support on Windows
might not be good enough.

If it turns out not to be good enough, we can try rsync, which has very
good reviews on the internet. This would be unfortunate, because it
would require running a separate command and installing an rsync
client. From cursory examination, it appears that cygwin is the best
one to use.


