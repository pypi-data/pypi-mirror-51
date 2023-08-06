Metric-Farmer
=============

**Cares about your project metrics**

**Documentation**: https://metricfarmer.readthedocs.io

Metric-Farmer is a Python based command line application to collect and store metrics from different sources
to different targets.

It is designed to easily create and maintain complex metric measurements and to painless integrate its functions into
continuous integration systems (CI/CD) or local task executions (cron jobs).

The configuration is completely done by JSON-based ``farm``-files in a project folder called ``.farmer``.
And no development skills are needed to use Metric-Farmer.

Developers can easily create own Metric-Farmer extensions to provide custom solutions for sources and targets.
For instance to measure a company-internal service.

Features
---------
Metric-Farmer is capable to collect metrics from following sources:

* static values
* random values
* file count
* REST requests (E.g. to measure JIRA or GitHub)


And sends the results to the following targets:

* print output (text or json)
* file output (text or json)
* database output (sqlite)
