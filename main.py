import sys  # sys нужен для передачи argv в QApplication
import os  # Отсюда нам понадобятся методы для отображения содержимого директорий
from copy import deepcopy as dp
from numpy import poly1d as pol

from PyQt5 import QtWidgets

from GUI import design  # Это наш конвертированный файл дизайна

### TODO: перегрузить вывод, сложение, умножение
class Matrix:
	def __init__(self, array=None):
		if not array:
			self.matrix = [[pol([0])]]
			self.n = 1
			self.m = 1
		else:
			self.matrix = []
			for row in array:
				r = []
				for elem in row:
					r.append( pol(elem) )
				self.matrix.append( r )

			self.n = len(self.matrix)
			self.m = len(self.matrix[0])
		self.dim = (self.n, self.m)


	def det(self):

		if self.n == self.m:
			if self.m == 2:
				return ( self.matrix[0][0]* self.matrix[1][1] - self.matrix[0][1]*self.matrix[1][0] )
			else:
				d = 0
				for j in range( self.m ):
					if self.matrix[0][j] == pol([0]):
						continue

					m = self.__minor(0, j)
					d += (-1)**j * self.matrix[0][j] * m
				return d
		else:
			return None

	def __minor(self, i, j, indexes=None):

		if not indexes:
			indexes = [[x for x in range(self.n)], [y for y in range(self.m)]]

		indexes[0].remove(i)
		indexes[1].remove(j)

		if ( len(indexes[0]) == len( indexes[1]) == 1 ):
			return self.matrix[indexes[0][0]][indexes[1][0]]

		elif ( len(indexes[0]) == len(indexes[1]) == 2 ):

			a1 = self.matrix[ indexes[0][0] ][ indexes[1][0] ] * self.matrix[ indexes[0][1] ][ indexes[1][1] ]
			a2 = self.matrix[ indexes[0][0] ][ indexes[1][1] ] * self.matrix[ indexes[0][1] ][ indexes[1][0] ]

			return a1 - a2
				
		res = 0
		count_l = 0
		for l in indexes[1]:
			if self.matrix[ indexes[0][0] ][l] == pol([0]):
				continue
			res += (-1)**(count_l) * self.matrix[ indexes[0][0] ][l] * self.__minor( dp(indexes[0][0]), l, dp(indexes))
			count_l+=1

		return res

	@staticmethod
	def diag(dim, val=1):

		array = []
		for i in range(dim):
			row = [0 for x in range(dim)]
			row[i] = val
			array.append(row)

		return Matrix(array)


	def tr(self):
		res = Matrix()

		array = []
		for j in range(self.m):
			col = []
			for i in range(self.n):
				col.append( self.matrix[i][j] )

			array.append(col)

		res.matrix = array
		res.n = self.m
		res.m = self.n

		return res


	def inv(self):
		if self.n != self.m:
			print("InverseError: Matrix must be squared")
			return None
		det = self.det()
		
		array = []
		for i in range(self.n):
			row = []
			for j in range(self.m):
				row.append( (-1)**(i+j)*self.__minor(i, j) )
			array.append(row)

		invert = Matrix()
		invert.matrix = array
		invert.n = self.n
		invert.m = self.m

		res = invert.tr()
		return [det, res]



	def __mul__(self, other):
		if self.m != other.n:
			print("Bad dimensions of matrixes!")
			return None
		else:
			res = []
			for i in range(self.n):
				row = []
				for j in range(other.m):
					elem = 0
					for k in range(other.n):
						elem += self.matrix[i][k] * other.matrix[k][j]
					row.append( elem )
				res.append( row )

			product = Matrix([])
			product.matrix = res
			product.n = len(product.matrix)
			product.m = len(product.matrix[0])

			return product


	def __add__(self, other):
		if self.n != other.n or self.m != other.m:
			print("Bad dimensions of matrixes!")
			return None
		else:
			res = Matrix()
			res.n = self.n
			res.m = self.m
			array = []
			for i in  range(self.n):
				row = []
				for j in range(self.m):
					sum_res = self.matrix[i][j] + other.matrix[i][j]
					row.append( sum_res )
				array.append( row )

			res.matrix = array
			return res


	def __sub__(self, other):
		if self.n != other.n or self.m != other.m:
			print("Bad dimensions of matrixes!")
			return None
		else:
			res = Matrix()
			res.n = self.n
			res.m = self.m
			array = []
			for i in  range(self.n):
				row = []
				for j in range(self.m):
					sum_res = self.matrix[i][j] - other.matrix[i][j]
					row.append( sum_res )
				array.append( row )

			res.matrix = array
			return res

		
	def __str__(self):
		out = ""
		for row in self.matrix:
			for elem in row:
				string = str(elem)
				out += string.split('\n')[1].replace('x', 's') + "  "
			out += "\n"
		out = out[:-1]
		return out



class Interface(QtWidgets.QMainWindow, design.Ui_MainWindow):
	def __init__(self):
		# Это здесь нужно для доступа к переменным, методам
		# и т.д. в файле design.py
		super().__init__()
		self.setupUi(self)  # Это нужно для инициализации нашего дизайна
		self.startButton.clicked.connect(self.parse_fields)
		self.clearButton.clicked.connect(self.clear_fields)
															

	def parse_fields(self):
		matrix_A_str = self.A_field.toPlainText()
		matrix_B_str = self.B_field.toPlainText()
		matrix_C_str = self.C_field.toPlainText()
		tf_str = self.TF_field.toPlainText()
		
		if tf_str:
			self.VVtoVSV(tf_str)
		elif matrix_A_str and matrix_B_str and matrix_C_str:
			self.VSVtoVV(matrix_A_str, matrix_B_str, matrix_C_str)


	def VVtoVSV(self, tf_str):
		pass


	def VSVtoVV(self, matrix_A_str, matrix_B_str, matrix_C_str):
		matrix_A_str = self.A_field.toPlainText()
		matrix_B_str = self.B_field.toPlainText()
		matrix_C_str = self.C_field.toPlainText()
		self.matrix_A = Matrix( self.parse_string(matrix_A_str) )
		self.matrix_B = Matrix( self.parse_string(matrix_B_str) )
		self.matrix_C = Matrix( self.parse_string(matrix_C_str) )


		sI = Matrix.diag(self.matrix_A.n, [1, 0])
		sIA = sI-self.matrix_A
		inv_sIA = sIA.inv()
		den = inv_sIA[0]
		num = self.matrix_C*inv_sIA[1]*self.matrix_B
		num = num.matrix[0][0]


		num_roots = num.r.tolist()
		den_roots = den.r.tolist()

		for n_root in num_roots:
			for d_root in den_roots:
				if n_root == d_root:
					num = (num / pol( [ 1, -n_root ] ) )[0]
					num_roots.remove(n_root)

					den = (den / pol( [ 1, -d_root ] ) )[0]
					den_roots.remove(d_root)

		self.TransferFunction = ( num, den )
		tf_str  = str(self.TransferFunction[0]).split("\n")[1].replace('x','s') + "\n"
		tf_str += str(self.TransferFunction[1]).split("\n")[1].replace('x','s')
		self.TF_field.setPlainText( tf_str )
		"""print("numerator  : ", str(self.TransferFunction[0]).split("\n")[1].replace('x','s'))
		print("---------------------")
		print("denumerator: ", str(self.TransferFunction[1]).split("\n")[1].replace('x','s'))
		print()"""


	def parse_string(self, str_matrix):
		str_matrix = str_matrix.split('\n')
		res = []

		for str_row in str_matrix:
			splitted_row = str_row.split(' ')
			row = []
			for symbol in splitted_row:
				if symbol:
					num = complex(symbol)
					if num.imag == 0:
						num = float(num.real)
					row.append([num])
			if row:
				res.append(row)

		return res

	def clear_fields(self):
		self.A_field.clear()
		self.B_field.clear()
		self.C_field.clear()
		self.TF_field.clear()

def main():
	app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
	window = Interface()  # Создаём объект класса ExampleApp
	window.show()  # Показываем окно
	app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
	main()  # то запускаем функцию main()

