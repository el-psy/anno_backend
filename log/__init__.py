import os
import json
import logging
import logging.config



def get_logger(config_path):
	with open(config_path, 'r', encoding='utf-8') as f:
		config = json.load(f)
		logging.config.dictConfig(config)
	logger = logging.getLogger('root')
	return logger



def logger_test():
	config_path = './log/log_config.json'
	logger = get_logger(config_path)
	for i in range(2):
		logger.info('adsiodhoaid')
		logger.warn('ashohdaodiah')
		logger.error('hdohaihfo')

logger = get_logger('./log/log_config.json')

if __name__ == "__main__":
    # configure_logging("log_config.json")
    # set_log_info()
	logger_test()