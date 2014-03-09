import TexObject
import Block
import ContentList
import re
item_pattern = re.compile(r'_\d+')
class Coordinates(Block.WrappedCode):
	Begin = '\\addplot coordinates {{\n'
	End   = '\n}};'
	def __init__(self, **kwargs):
		self.Content = ContentList.ContentList(r'({__content__})', **kwargs)
		Block.WrappedCode.__init__(self, **kwargs)
	def push(self, x, y):
		self._content.push('{x},{y}'.format(x = x, y = y))
class TikzAxis(Block.Env):
	EnvName = 'tikzpicture'
	class Content(Block.Env):
		EnvName = 'axis'
		class Content(TexObject.TexObject):
			def __init__(self, **kwargs):
				TexObject.TexObject.__init__(self, **kwargs)
				self._plots = []
			def addplot(self, points):
				self._plots.append(Coordinates())
				for x,y in points:
					self._plots[-1].push(x,y)
			def format(self, **kwargs):
				res = []
				for plot in self._plots:
					res.append(plot.format(**kwargs))
				return '\n'.join(res)
	def __init__(self, **kwargs):
		Block.Env.__init__(self, **kwargs)
		for name in dir(self):
			if name not in dir(Block.Env) and item_pattern.match(name):
				self._content._content.addplot(getattr(self,name))
if __name__ == '__main__':
	class graph(TikzAxis):
		_1 = [(x,x*x) for x in range(-10,10)]
		_2 = [(x,2*x) for x in range(-10,10)]
	print graph()
