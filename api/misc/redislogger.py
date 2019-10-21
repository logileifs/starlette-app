import redis
#import ujson
import logging
from datetime import datetime
from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def add_fields(self, log_record, record, message_dict):
		super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
		if not log_record.get('timestamp'):
			now = datetime.utcfromtimestamp(record.created).isoformat()
			log_record['timestamp'] = now
		if log_record.get('level'):
			log_record['level'] = log_record['level'].upper()
		else:
			log_record['level'] = record.levelname


class RedisHandler(logging.StreamHandler):
	def __init__(self, channel, host='localhost', port=6379, level=logging.NOTSET):
		self.level = level
		super().__init__()
		self.host = host
		self.port = port
		self.client = redis.Redis(host, port)
		self.channel = channel
		self.formatter = CustomJsonFormatter(
			'(timestamp) (level) (name) (message)',
		)

	def emit(self, record):
		record = self.format(record)
		#print('emitting record: %s' % record)
		try:
			return self.client.publish(self.channel, record)
		except redis.exceptions.ConnectionError:
			#print('failed to emit log to channel {channel} on {host}:{port}'.format(
			#	channel=self.channel,
			#	host=self.host,
			#	port=self.port
			#))
			pass
