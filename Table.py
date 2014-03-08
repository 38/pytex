import TexObject
import Block
class Matrix(TexObject.TexObject):
	""" A matrix"""
	def __init__(self, row, column, table,**kwargs):
		TexObject.TexObject.__init__(self, **kwargs)
		self._content = [[TexObject.MakeTexObject(table.ValueAt(r,c)) for c in xrange(column)] for r in xrange(row)]
	def format(self, **kwargs):
		res = ['']
		for row in self._content:
			line = []
			for cell in row:
				line.append(cell.format(**kwargs))
			line = ' & '.join(line)
			res.append(line + '\n')
		res.append('')
		return '\\hline\n'.join(res)[:-1]
class Table(Block.Env):
	EnvName = 'tabular'
	Rows    = TexObject.ContentField()
	Columns = TexObject.ContentField()
	ValueAt = TexObject.ContentField(lambda R,C: 0)
	def __init__(self, **kwargs):
		Block.Env.__init__(self, **kwargs)
		self._kwargs['__rows__'] = TexObject.MakeTexObject(self.Rows, **kwargs)
		self._kwargs['__columns__'] = TexObject.MakeTexObject(self.Columns, **kwargs)
		self._content = Matrix(self.Rows, self.Columns, self, **self._kwargs) 
if __name__ == '__main__':
	print Table(Rows = 10, Columns = 10, ValueAt = lambda R,C: int(R==C))
	class testtable(Table):
		Rows = 5
		Columns = 2
		def ValueAt(self,R,C):
			if R == 1:
				return ['X', Block.InlineMath(Content = 'X^2')][C]
			else:
				return [R, R*R][C]
	print testtable()
