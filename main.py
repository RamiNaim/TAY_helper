import sys  # sys нужен для передачи argv в QApplication
import os  # Отсюда нам понадобятся методы для отображения содержимого директорий
from copy import deepcopy as dp
from numpy import poly1d as pol

from PyQt5 import QtWidgets

from GUI import design_new  # Это наш конвертированный файл дизайна

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
		self.rank_val = 0

	def det(self):

		if self.n == self.m:
			if self.m == 2:
				d = ( self.matrix[0][0]* self.matrix[1][1] - self.matrix[0][1]*self.matrix[1][0] )
				if d != 0:
					self.rank_val = 2
				return d
			elif self.n == 1:
				if self.matrix[0][0] != 0:
					self.rank_val = 1
				return self.matrix[0][0]
			else:
				d = pol([0])
				for j in range( self.m ):

					m = self.__minor(0, j)
					d += (-1)**j * self.matrix[0][j] * m

				if d != pol([0]):
					self.rank_val = self.n

				return d
		else:
			print("DetError: Matrix must be squared")
			return None


	def __minor(self, i, j, indexes=None):

		if not indexes:
			indexes = [[x for x in range(self.n)], [y for y in range(self.m)]]

		indexes[0].remove(i)
		indexes[1].remove(j)

		if ( len(indexes[0]) == len( indexes[1]) == 1 ):
			if self.matrix[indexes[0][0]][indexes[1][0]] != pol([0]) and self.rank_val < 1:
				self.rank_val = 1
			return self.matrix[indexes[0][0]][indexes[1][0]]

		elif ( len(indexes[0]) == len(indexes[1]) == 2 ):

			a1 = self.matrix[ indexes[0][0] ][ indexes[1][0] ] * self.matrix[ indexes[0][1] ][ indexes[1][1] ]
			a2 = self.matrix[ indexes[0][0] ][ indexes[1][1] ] * self.matrix[ indexes[0][1] ][ indexes[1][0] ]

			if (a1 - a2) != pol([0]) and self.rank_val < 2:
				self.rank_val = 2

			return a1 - a2
				
		res = 0
		count_l = 0
		for l in indexes[1]:
			minor = self.__minor( dp(indexes[0][0]), l, dp(indexes))

			if minor != pol([0]) and self.rank_val < len( indexes[0] ):
				self.rank_val = len( indexes[0] )

			res += (-1)**(count_l) * self.matrix[ indexes[0][0] ][l] * minor
			count_l+=1

		return res


	def rank(self):

		stop = False
		for row in self.matrix:
			for elem in row:
				if elem != pol([0]):
					self.rank_val = 1
					stop = True
					break
			if stop:
				break

		self.det()
		return self.rank_val


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
		if det == pol([0]):
			print("InverseError: Determinant is zero")
			return None
		
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

	# self.conj - объединение двух матриц
	# args: other - Matrix(), с которой сопрягаем, axis - способ сопряжения (0 - stack, 1 - extend)
	# return Возвращает новую склеянную матрицу
	def conj(self, other, axis):
		if axis == 0:
			self.matrix = self.matrix + other.matrix
			self.n = len(self.matrix)
			self.m = len(self.matrix[0])
			return None

		elif axis == 1:
			for i in range(self.n):
				self.matrix[i] = self.matrix[i] + other.matrix[i]
			self.n = len(self.matrix)
			self.m = len(self.matrix[0])
			return None

	def __pow__(self, other):
		res = self
		for _ in range( other - 1 ):
			res = res * self

		return res

	def __mul__(self, other):
		if self.m != other.n:
			print("MultError: Bad dimensions of matrixes!")
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
			print("SummError: Bad dimensions of matrixes!")
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
			print("SubError: Bad dimensions of matrixes!")
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



class Interface(QtWidgets.QMainWindow, design_new.Ui_MainWindow):
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

		self.controllabilityCheck()
		self.observabilityCheck()
		self.stabilityCheck()

		systemsQuality = ""

		if self.controllable:
			systemsQuality += "Да\n"
		else:
			systemsQuality += "Нет\n"

		if self.observable:
			systemsQuality += "Да\n"
		else:
			systemsQuality += "Нет\n"

		if self.stable:
			systemsQuality += "Да"
		else:
			systemsQuality += "Нет"

		self.SystemQualitiesField.setPlainText( systemsQuality )


	def VVtoVSV(self, tf_str):
		num_den = tf_str.split("\n")
		num_str = num_den[0].split(", ")
		den_str = num_den[1].split(", ")

		num = []
		for elem in num_str:
			if complex(elem).imag == 0:
				num.append( float(elem) )
			else:
				num.append( complex(elem) )

		den = []
		for elem in den_str:
			if complex(elem).imag == 0:
				den.append( float(elem) )
			else:
				den.append( complex(elem) )

		self.TransferFunction = ( pol( num ), pol( den ) )

	
		array_A = []
		array_B = []
		array_C = [[]]
		l_den = len(self.TransferFunction[1])
		l_num = len(self.TransferFunction[0])

		a0 = self.TransferFunction[1][l_den]

		for i in range( l_den ):
			### Рассчет матрицы C
			if (i <= l_num):
				array_C[0].append( self.TransferFunction[0][i] / a0 )
			else:
				array_C[0].append( pol([0]) )

			### Рассчет матрицы B
			if ( i == ( l_den - 1 )):
				array_B.append( [pol(1)] )
			else:
				array_B.append( [pol(0)] )

			### Рассчет матрицы A
			row_A = []
			for j in range( l_den ):
				if ( i == ( l_den - 1 )):
					row_A.append( -self.TransferFunction[1][j] / a0 )
				elif ( j == ( i + 1 )):
					row_A.append( pol([1]) )
				else:
					row_A.append( pol([0]) )


			array_A.append( row_A )

		self.matrix_A = Matrix(array_A)
		self.matrix_B = Matrix(array_B)
		self.matrix_C = Matrix(array_C)

		if self.ObserveRadioButton.isChecked():
			self.matrix_A = self.matrix_A.tr()
			b = dp(self.matrix_B)
			self.matrix_B = dp(self.matrix_C.tr())
			self.matrix_C = dp(b.tr())

		self.A_field.setPlainText( str(self.matrix_A) )
		self.B_field.setPlainText( str(self.matrix_B) )
		self.C_field.setPlainText( str(self.matrix_C) )


		self.controllabilityCheck()
		self.observabilityCheck()
		self.stabilityCheck()

		systemsQuality = ""

		if self.controllable:
			systemsQuality += "Да\n"
		else:
			systemsQuality += "Нет\n"

		if self.observable:
			systemsQuality += "Да\n"
		else:
			systemsQuality += "Нет\n"

		if self.stable:
			systemsQuality += "Да"
		else:
			systemsQuality += "Нет"

		self.SystemQualitiesField.setPlainText( systemsQuality )


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
		tf_str  = str(self.TransferFunction[0].c) + "\n"
		tf_str += str(self.TransferFunction[1].c)
		self.TF_field.setPlainText( tf_str )

	def controllabilityCheck(self):
		controllabilityMatrix = dp( self.matrix_B )

		for p in range( 1, self.matrix_A.n ):
			controllabilityMatrix.conj( (self.matrix_A ** p) * self.matrix_B , 1 )

		if controllabilityMatrix.rank() == self.matrix_A.n:
			self.controllable = True
		else:
			self.controllable = False

	def observabilityCheck(self):
		observabilityMatrix = dp(self.matrix_C)

		for p in range( 1, self.matrix_A.n ):
			observabilityMatrix.conj( self.matrix_C * (self.matrix_A ** p), 0 )

		if observabilityMatrix.rank() == self.matrix_A.n:
			self.observable = True
		else:
			self.observable = False

	def stabilityCheck(self):
		self.stable = True

		den = self.TransferFunction[1]
		den_roots = den.r
		for root in den_roots:
			r = complex(root)
			if r.real > 0:
				self.stable = False
				break


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
		self.SystemQualitiesField.clear()

def main():
	app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
	window = Interface()  # Создаём объект класса ExampleApp
	window.show()  # Показываем окно
	app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
	main()  # то запускаем функцию main()

