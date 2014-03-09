import TexObject
import Block
import ContentList
import re
item_pattern = re.compile(r'_\d+')
class Coordinates(Block.WrappedCode):
	Begin = '\\addplot {__plotargs__} coordinates {{\n'
	End   = '\n}};'
	PlotArgs = TexObject.ContentField('')
	def __init__(self, **kwargs):
		self.Content = ContentList.ContentList(r'({__content__})', **kwargs)
		Block.WrappedCode.__init__(self, **kwargs)
		self._kwargs['__plotargs__'] = TexObject.MakeTexObject(self.PlotArgs)
	def push(self, x, y):
		self._content.push('{x},{y}'.format(x = x, y = y))
class TikzAxis(Block.Env):
	EnvName = 'tikzpicture'
	AxisArgs = TexObject.ContentField('')
	PlotArgs = TexObject.ContentField('')
	class Content(Block.Env):
		EnvName = 'axis'
		class Content(TexObject.TexObject):
			def __init__(self, **kwargs):
				TexObject.TexObject.__init__(self, **kwargs)
				self._plots = []
			def addplot(self, points, args = None):
				if args == None: args = self._kwargs['__plotargs__']
				self._plots.append(Coordinates(PlotArgs = args))
				for x,y in points:
					self._plots[-1].push(x,y)
			def format(self, **kwargs):
				res = []
				for plot in self._plots:
					res.append(plot.format(**kwargs))
				return '\n'.join(res)
	def __init__(self, **kwargs):
		Block.Env.__init__(self, **kwargs)
		self._content._kwargs['__arglist__'] = TexObject.MakeTexObject(self.AxisArgs)
		self._content._content._kwargs['__plotargs__'] = TexObject.MakeTexObject(self.PlotArgs)
		for name in dir(self):
			if name not in dir(Block.Env) and item_pattern.match(name):
				self._content._content.addplot(getattr(self,name))
	def addplot(self, points, args = None):
		self._content._content.addplot(points, args)
if __name__ == '__main__':
	class graph(TikzAxis):
		_1 = [(x,x*x) for x in range(-10,10)]
		_2 = [(x,2*x) for x in range(-10,10)]
	print graph()
