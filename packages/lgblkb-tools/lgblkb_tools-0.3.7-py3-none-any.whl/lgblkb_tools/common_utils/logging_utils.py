import logging.handlers as log_handlers
from timeit import default_timer as timer
import functools
from box import Box
from colorlog import ColoredFormatter
import logging
from python_log_indenter import IndentedLoggerAdapter

colored_log_format=f"%(log_color)s%(asctime)s %(processName)18.18s %(levelname)5.5s || %(message)s"
base_log_indent_settings=dict(indent_char='| ',spaces=1)
date_fmt="%m-%d %H:%M:%S"
wrapper_log_level=logging.INFO
default_log_level=logging.INFO
default_log_format=colored_log_format.replace(r'%(log_color)s','')
log_func_mapper=Box()
log_func_mapper[logging.DEBUG]=lambda logger:logger.debug
log_func_mapper[logging.INFO]=lambda logger:logger.info
log_func_mapper[logging.WARNING]=lambda logger:logger.warning
log_func_mapper[logging.CRITICAL]=lambda logger:logger.critical
log_func_mapper[logging.ERROR]=lambda logger:logger.error

log_sayer=lambda logger,log_level:log_func_mapper[log_level](logger)

class TheLogger(IndentedLoggerAdapter):
	
	def __init__(self,name,extra=None,auto_add=True,log_level=None,log_format='',**kwargs):
		logger=setup_logger(name,log_level,log_format)
		logger.propagate=False
		super(TheLogger,self).__init__(logger,extra,auto_add,**dict(base_log_indent_settings,**kwargs))
		self.current_handlers=[]
	
	def add_file_handler(self,log_filepath,log_level=logging.DEBUG):
		log_handler=logging.FileHandler(log_filepath)
		log_handler.setFormatter(logging.Formatter(default_log_format))
		log_handler.setLevel(log_level)
		self.logger.addHandler(log_handler)
		self.current_handlers.append(log_handler)
		return self
	
	def add_rotating_handler(self,log_filepath,log_level=None,maxBytes=1.99e6,backupCount=14,**other_opts):
		log_level=log_level or default_log_level
		log_handler=log_handlers.RotatingFileHandler(maxBytes=int(maxBytes),filename=log_filepath,backupCount=backupCount,**other_opts)
		log_handler=self.logger.addHandler(log_handler,level=log_level,log_format=default_log_format)
		self.current_handlers.append(log_handler)
		return self
	
	def wrap(self,log_level=None,skimpy=False):
		def second_wrapper(func):
			@functools.wraps(func)
			def wrapper(*args,**kwargs):
				log_say=log_sayer(self,log_level or wrapper_log_level)
				if skimpy: log_say('Performing "%s"...',func.__name__)
				else: log_say('Running "%s":',func.__name__)
				start=timer()
				self.add()
				result=func(*args,**kwargs)
				if not skimpy: log_say('Done "%s". Duration: %.3f sec.',func.__name__,timer()-start)
				self.sub()
				return result
			
			return wrapper
		
		return second_wrapper
	
	def remove_active_handler(self):
		target_handler=self.current_handlers.pop()
		self.logger.handlers.remove(target_handler)
		return self

def setup_logger(name,log_level=None,log_format=''):
	log_level=log_level or default_log_level
	new_logger=logging.getLogger(name)
	new_logger.setLevel(log_level)
	log_handler=logging.StreamHandler()
	log_format=log_format or colored_log_format
	log_handler.setFormatter(ColoredFormatter(log_format,date_fmt))
	new_logger.addHandler(log_handler)
	# new_logger.info(f'Root logger initialized with level {logging._levelToName[log_level]}.')
	return new_logger

# root_logger=setup_logger(log_level=logging.DEBUG)

simple_logger=TheLogger(__name__)
# log_wrapper=lambda log_level=logging.DEBUG,skimpy=False:simple_logger.wrap(log_level=log_level,skimpy=skimpy)
log_wrapper=simple_logger.wrap


# @simple_logger.wrap(log_level=logging.DEBUG)
@log_wrapper()
def main():
	x=[1,2,3]
	simple_logger.info('x: %s',x)
	
	
	pass

if __name__=='__main__':
	main()
