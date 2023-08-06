USAGE
===============

Basic
---------

log = CLogging("log_name", "temp_dir/xxx.log")

log.info('info msg')
log.info('info msg')
	
Advanced
----------

my_define_format = logging.Formatter(u'%(asctime)s|%(levelname)s|%(name)s|%(message)s')

log = CLogging("log_name", "C:dir/xxx.log", logging.INFO, 'w', my_define_format, stream_handler_on=True, stream_level=logging.ERROR)
     

	