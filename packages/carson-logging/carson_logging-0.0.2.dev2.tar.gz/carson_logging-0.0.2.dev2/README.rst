===================
Carson
===================

This project has a lot of packages.

All package consists of the following:

* `CLogging`_

CLogging
----------

**Issues** : https://github.com/CarsonSlovoka/carson-logging/issues

USAGE
===============

Basic
---------

::

    log = CLogging("log_name", "temp_dir/xxx.log")
    log.info('info msg')
    log.debug('info msg')
    log.warning('info msg')
    log.error('info msg')
    log.critical('info msg')
	
Advanced
----------

::

    my_define_format = logging.Formatter(u'%(asctime)s|%(levelname)s|%(name)s|%(message)s')
    log = CLogging("log_name", "C:dir/xxx.log", logging.INFO, 'w', my_define_format, stream_handler_on=True, stream_level=logging.ERROR)