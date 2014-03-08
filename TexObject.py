"""Some basic define of pytex system"""
from abc import abstractmethod
class UndefinedContentException(Exception): pass
class _ContentFieldRetBase(object): pass
def ContentField(default = None):
	"""A filed is used for indicate that this member is a field of this object,
	   see class definition for details
	   1. A content might be a constructor which can be called as Content(**kwargs)
	   2. A constant value like 'this is a test'
	   3. A TexObject like PlainText
	   4. A static method, which takes **kwargs as argument and return a TexObject
	"""
	class _ContentFieldRet(_ContentFieldRetBase):
		@staticmethod
		def __call__(**kwargs):
			if default != None: 
				return MakeTexObject(default, **kwargs)
			else:
				raise UndefinedContentException()
	return _ContentFieldRet()

class TexObject(object):
	_kwargs = {}
	"""In pytex, all class can be render by parameters, and the parameter was set in initializer"""
	def __init__(self, **kwargs):
		self._kwargs = kwargs
		for name in dir(self):
			val = getattr(self, name)
			if isinstance(val, _ContentFieldRetBase) and name in kwargs:
				setattr(self, name, kwargs[name])
	@abstractmethod
	def format(self, **kwargs): pass
	def __str__(self): 
		return self.format(**self._kwargs)
	def header(self):
		return []

class Empty(TexObject):
	"""This class defines an empty texobject, which produces nothing"""
	def __init__(self, **kwargs):
		TexObject.__init__(self,**kwargs)
	def format(self, **kwargs): 
		return ''

class PlainText(TexObject):
	"""Plain Text"""
	def __init__(self, text, **kwargs):
		TexObject.__init__(self, **kwargs)
		self._plain_text = text
	def format(self, **kwargs):
		return self._plain_text.format(**kwargs)

def MakeTexObject(value, **kwargs):
	"""Convert a non Tex Object to Tex object"""
	if callable(value): return value(**kwargs)
	if isinstance(value, TexObject): return value
	return PlainText(str(value), **kwargs)

def MergeArgs(first, second):
	"""merge initial arglist and formatting arglist"""
	ret = {key:value for key,value in first.items()}
	for key,value in second.items():
		if len(key) > 1 and key[:2] == "__": continue
		ret[key] = value
	return ret
