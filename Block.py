"""Define Base Class of block object, and some simple class like math"""
import TexObject


class WrappedCode(TexObject.TexObject):
	"""Wrapped Code is some tex code that is wrapped by other code
	   like $x = 3$
	   Expect define new fields, the class also accept content from 
	   the constructor.
	   For exmple
	   class m(Math):
	   		Content = '123'
	   obj = m()
	   is equavailent to

	   obj = Math(Content = '123')
	"""
	Content = TexObject.ContentField()
	Begin = TexObject.ContentField()
	End = TexObject.ContentField 
	def __init__(self, **kwargs): 
		TexObject.TexObject.__init__(self, **kwargs)
		self._content = TexObject.MakeTexObject(self.Content,**self._kwargs)
		self._begin = TexObject.MakeTexObject(self.Begin,**self._kwargs)
		self._end = TexObject.MakeTexObject(self.End,**self._kwargs)
	def format(self, **kwargs):
		_content_args = TexObject.MergeArgs(self._content._kwargs, kwargs)
		_wrapper_args = TexObject.MergeArgs(self._kwargs, kwargs)
		return "{begin}{content}{end}"\
				.format(begin = self._begin.format(**_wrapper_args), \
				 		end   = self._end.format(**_wrapper_args), \
						content = self._content.format(**_content_args))

class Env(WrappedCode):
	"""A environment block. In the content, there are 3 additoinal parameters:
	   __envname__: the environment name
	   __arglist__: the envirionment argument list
	   __envobj__ : the object of this environment
	"""
	Content = TexObject.Empty
	Begin = '\\begin{{{__envname__}}}{__arglist__}\n'
	End   = '\n\\end{{{__envname__}}}{__arglist__}'
	EnvArgs = TexObject.ContentField('')
	EvnName = TexObject.ContentField()
	def __init__(self, **kwargs):
		WrappedCode.__init__(self, **kwargs)
		self._kwargs['__envname__'] =  TexObject.MakeTexObject(self.EnvName, **self._kwargs)
		self._kwargs['__arglist__'] =  TexObject.MakeTexObject(self.EnvArgs, **self._kwargs)
		self._kwargs['__envobj__'] = self

class InlineMath(WrappedCode):
	Begin = '$'
	End = '$'

class Math(WrappedCode):
	Begin = '$$'
	End = '$$'
class Block(WrappedCode):
	Begin = '{'
	End = '}'

if __name__ == '__main__':
	class testEnv(Env):
		EnvName = 'test1'
		class Content(Env):
			EnvName = 'test2'
			class Content(Env):
				EnvName = 'test3'
	print testEnv()
	print TexObject.PlainText("this is a test {name}", name = 3)
	class testMath(Math):
		Content = 'x+3'
	print testMath()
	print Math(Content = '1+{variable}', variable = 3)
