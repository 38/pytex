import TexObject
import Block
import re
item_pattern = re.compile(r'_\d+')
class ContentList(TexObject.TexObject):
	"""Represents a run of contents"""
	def __init__(self, item_fmt ,**kwargs):
		"""item_fmt is the foramt string for each item, use __content__ as the content of item"""
		TexObject.TexObject.__init__(self, **kwargs)
		self._kwargs['__format__'] = item_fmt
		self._content = []
		self._next_id = 0
	def push(self, what, where = -1):
		if where == -1:
			where = self._next_id
			self._next_id += 1
		elif where > self._next_id:
			self._next_id = where + 1
		self._content.append((where, what))
	def format(self, **kwargs):
		kwargs = TexObject.MergeArgs(self._kwargs, kwargs)
		self._content.sort()
		res = []
		for _,item in self._content:
			res.append(kwargs['__format__'].format(__content__ = item.format(**kwargs)))
		return '\n'.join(res)
class ContentListEnv(Block.Env):
	def __init__(self, **kwargs):
		self.Content = ContentList(r'\item {__content__}', **kwargs)
		for name in dir(self):
			if name not in dir(Block.Env) and item_pattern.match(name):
				idx = int(name[1:])
				value = TexObject.MakeTexObject(getattr(self, name), **kwargs)
				self.Content.push(value, idx)
				setattr(self, name, value)   #set the attribute, so that we can modify it
		Block.Env.__init__(self, **kwargs)
	def push(self, what, where = -1):
		self._content.push(what, where)
class Itemize(ContentListEnv): 
	EnvName = 'itemize'
class Enumerate(ContentListEnv): 
	EnvName = 'enumerate'

if __name__ == '__main__':
	class test(Itemize):
		_1 = 'abc'
		_2 = 'def'
	print test()
	class test2(Itemize):
		class _1(Enumerate):
			_1 = 'this is {name}'
			_2 = 'this is the test for {name}'
		_2 = '{msg}'
	print test2(name = 'pytex', msg = 'hello world')
	obj = test2(name = 'pytex', msg = 'hello world')
	obj._1.push('new item')
	print obj 
