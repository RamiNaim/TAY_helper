import sys  # sys нужен для передачи argv в QApplication
from copy import deepcopy as dp # используется для полного копирования объектов
from numpy import poly1d as pol # основной тип данных, используемый в матрицах

from PyQt5 import QtWidgets # Необходимый модуль для создания интерфейса

from GUI import design_new  # Файл с дизайном


### Класс Матрица ###
### В основном контейнере для элементов self.matrix используется тип данных numpy.poly1d 
### для корректного рассчета передаточной функции
class Matrix:
	### Конструктор класса
	### Args: массив, содержащий числа. Если массив пустой, создается нулевая матрица размера 1х1
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
		self.rank_val = 0

	### Метод self.det()
	### Args: -
	### Return: определитель матрицы (тип данных numpy.poly1d), None если матрица не квадратная
	### Функция рассчитывает детерминант для матрицы 2х2 и 1х1 'на месте', иначе вызывает метод self.__minor(i, j)
	### Также во время рассчета определителя определяется ранг матрицы: изначально ранг r = 0, если найден минор большего порядка - ранг увеличивается
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
			### При размерности>(2х2) разложение производится по первой строке матрицы
			else:
				d = pol([0])
				for j in range( self.m ):
					d += (-1)**j * self.matrix[0][j] * self.__minor(0, j)

				### Если дискриминант!=0, ранг матрицы равен размерности матрицы
				if d != pol([0]):
					self.rank_val = self.n

				return d
		else:
			print("DetError: Matrix must be squared")
			return None


	### Метод self.__minor()
	### Args: i, j - индексы элемента, для которых ищется минор
	### 	  indexes - массив индексов, которые не 'вычеркнуты' при рассчете минора, передается при рекурсивном вызове функции
	### Return: значение i-ого j-ого минора (тип данных numpy.poly1d)
	### Функция рассчитывает минор 2х2 и 1х1 'на месте', иначе рекурсивно вызывает метод self.__minor(i, j, indexes).
	### Также во время рассчета определителя определяется ранг матрицы: изначально ранг r = 0, если найден минор большего порядка - ранг увеличивается
	def __minor(self, i, j, indexes=None):

		if not indexes:
			# Создаем массив, который содержит все индексы нашей матрицы
			indexes = [[x for x in range(self.n)], [y for y in range(self.m)]]

		# Удаляем из списков с индексами номера минора, который необходимо рассчитать
		indexes[0].remove(i)
		indexes[1].remove(j)

		# Если остался один элемент - возвращаем этот элемент
		if ( len(indexes[0]) == len( indexes[1]) == 1 ):

			if self.matrix[indexes[0][0]][indexes[1][0]] != pol([0]) and self.rank_val < 1:
				self.rank_val = 1

			return self.matrix[indexes[0][0]][indexes[1][0]]

		# Если минор размера 2х2 возвращаем определитель
		elif ( len(indexes[0]) == len(indexes[1]) == 2 ):

			a1 = self.matrix[ indexes[0][0] ][ indexes[1][0] ] * self.matrix[ indexes[0][1] ][ indexes[1][1] ]
			a2 = self.matrix[ indexes[0][0] ][ indexes[1][1] ] * self.matrix[ indexes[0][1] ][ indexes[1][0] ]

			if (a1 - a2) != pol([0]) and self.rank_val < 2:
				self.rank_val = 2

			return a1 - a2
		
		# Если порядок минора >2 - рекурсивно вызываем метод self.__minor(i, j, indexes), 
		# передавая в качестве индексов строк и столбцов только те, которые не были "вычеркнуты" предыдущими рассчетами
		res = 0
		count_l = 0
		for l in indexes[1]:
			minor = self.__minor( dp(indexes[0][0]), l, dp(indexes) )

			if minor != pol([0]) and self.rank_val < len( indexes[0] ):
				self.rank_val = len( indexes[0] )

			res += (-1)**(count_l) * self.matrix[ indexes[0][0] ][l] * minor
			count_l+=1

		return res

	### Метод self.rank()
	### Args: -
	### Return: ранг матрицы (тип данных int)
	def rank(self):
		# Обнулим значение ранга
		self.rank_val = 0

		stop = False
		# Если хотя бы один элемент матрицы отличен от нуля - ранг равен 1
		for row in self.matrix:
			for elem in row:
				if elem != pol([0]):
					self.rank_val = 1
					stop = True
					break
			if stop:
				break

		# Запускаем функцию self.det(), в процессе выполнения которой рассчитывается ранг
		self.det()
		return self.rank_val


	### Статический метод класса Matrix.rank()
	### Args: dim - размер желаемой диагональной матрицы, val - значение элементов главной диагонали
	### Return: Диагональную матрицу
	@staticmethod
	def diag(dim, val=1):

		array = []
		for i in range(dim):
			row = [0 for x in range(dim)]
			row[i] = val
			array.append(row)

		return Matrix(array)

	### Метод self.tf()
	### Args: -
	### Return: транспонированную матрицу
	### NOTE: функция возвращает новую матрицу, а не изменяет саму себя
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

	### Метод self.inv()
	### Args: -
	### Return: лист, который содержит определитель и обратную матрицу, умноженную на детерминант
	### NOTE: функция возвращает массив, а не изменяет саму себя
	def inv(self):
		if self.n != self.m:
			print("InverseError: Matrix must be squared")
			return None
		det = self.det()
		if det == pol([0]):
			print("InverseError: Determinant is zero")
			return None
		
		# i, j элемент сопряженной матрицы - это i, j минор с учетом знака
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

		# Транспонируем сопряженную матрицу и получаем обратную
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


	### Перегрузка операторов степени, умножения, сложения, вычитания, str()
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


### Класс Интерфейс ###
### Отвечает за рассчет передаточной функции, системы вход-состояние-выход в управляемом/наблюдаемом базисе,
### определение управляемости, наблюдаемости, устойчивости
class Interface(QtWidgets.QMainWindow, design_new.Ui_MainWindow):
	def __init__(self):
		# Наследование необходимо для доступа к объектам, методам из design_new
		super().__init__()

		# Инициализация интерфейса
		self.setupUi(self)

		# Привязка функций, которые будут выполняться при нажатии на кнопки
		self.startButton.clicked.connect(self.parse_fields)
		self.clearButton.clicked.connect(self.clear_fields)
															
	### Метод self.parse_field()
	### Args: -
	### Return: -
	### Метод выгружает введенные пользователем данные и обрабатывает их
	def parse_fields(self):

		# Выгрузка данных из полей
		matrix_A_str = self.A_field.toPlainText()
		matrix_B_str = self.B_field.toPlainText()
		matrix_C_str = self.C_field.toPlainText()
		tf_str = self.TF_field.toPlainText()

		# Если пользователь ввел передаточную функцию, запускаем функцию перевода из ВВ в ВСВ
		if tf_str:
			self.VVtoVSV(tf_str)
		# Если введены три матрицы, запускаем функцию перевода из ВСВ в ВВ
		elif matrix_A_str and matrix_B_str and matrix_C_str:
			self.VSVtoVV(matrix_A_str, matrix_B_str, matrix_C_str)

		# Проверяем систему на управляемость, наблюдаемость и устойчивость
		self.controllabilityCheck()
		self.observabilityCheck()
		self.stabilityCheck()

		# Вывод сообщения об управляемости, наблюдаемости, устойчивости в специальное поле
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


	### Метод self.VVtoVSV()
	### Args: tf_str - передаточная функция в виде строки
	### Return: -
	### Метод обрабатывает передаточную функцию и находит матрицы A, B, C в выбранном пользователем базисе
	def VVtoVSV(self, tf_str):
		# Парсим строку и представляем передаточную функцию в виде списков num(числитель) и den(знаменатель)
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

		# Составляем матрицы A, B, C в управляемом базисе
		array_A = []
		array_B = []
		array_C = [[]]
		l_den = len(self.TransferFunction[1].c)
		l_num = len(self.TransferFunction[0].c)

		a0 = self.TransferFunction[1][l_den - 1]

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

		# Если пользователь выбрал наблюдаемый базис, транспнируем A, меняем транспонированные B и С местами
		if self.ObserveRadioButton.isChecked():
			self.matrix_A = self.matrix_A.tr()
			b = dp(self.matrix_B)
			self.matrix_B = dp(self.matrix_C.tr())
			self.matrix_C = dp(b.tr())

		# Вывод матриц в поля
		self.A_field.setPlainText( str(self.matrix_A) )
		self.B_field.setPlainText( str(self.matrix_B) )
		self.C_field.setPlainText( str(self.matrix_C) )

	### Метод self.VSVtoVV()
	### Args: matrix_A_str, matrix_B_str, matrix_C_str - матрицы А, В, С в виде строки
	### Return: -
	### Метод обрабатывает матрицы А, B, C и находит передаточную функцию
	def VSVtoVV(self, matrix_A_str, matrix_B_str, matrix_C_str):
		# Выгружаем введенные пользователем данные
		matrix_A_str = self.A_field.toPlainText()
		matrix_B_str = self.B_field.toPlainText()
		matrix_C_str = self.C_field.toPlainText()

		# Создаем объекты Matrix для введенных пользователем матриц
		self.matrix_A = Matrix( self.parse_string_matrix(matrix_A_str) )
		self.matrix_B = Matrix( self.parse_string_matrix(matrix_B_str) )
		self.matrix_C = Matrix( self.parse_string_matrix(matrix_C_str) )

		# Расчитываем передаточную функцию
		sI = Matrix.diag(self.matrix_A.n, [1, 0])
		sIA = sI-self.matrix_A
		inv_sIA = sIA.inv()
		den = inv_sIA[0]
		num = self.matrix_C*inv_sIA[1]*self.matrix_B
		num = num.matrix[0][0]

		# Проверка на сократимость полинома знаменателя и числителя
		# Если есть общие корни, то делим числитель на знаменатель
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

		# Формируем строку для вывода передаточной функции
		tf_str = ""
		for koef in self.TransferFunction[0].c:
			tf_str += str(koef) + ", "
		tf_str = tf_str[:-2]
		tf_str += "\n"

		for koef in self.TransferFunction[1].c:
			tf_str += str(koef) + ", "
		tf_str = tf_str[:-2]

		# Записываем передаточную функцию в соответствующее поле
		self.TF_field.setPlainText( tf_str )

	### Метод self.controllabilityCheck()
	### Args: -
	### Return: -
	### Метод проверяет систему на управляемость
	def controllabilityCheck(self):
		controllabilityMatrix = dp( self.matrix_B )

		for p in range( 1, self.matrix_A.n ):
			controllabilityMatrix.conj( (self.matrix_A ** p) * self.matrix_B , 1 )

		if controllabilityMatrix.rank() == self.matrix_A.n:
			self.controllable = True
		else:
			self.controllable = False

	### Метод self.observabilityCheck()
	### Args: -
	### Return: -
	### Метод проверяет систему на наблюдаемость
	def observabilityCheck(self):
		observabilityMatrix = dp(self.matrix_C)

		for p in range( 1, self.matrix_A.n ):
			observabilityMatrix.conj( self.matrix_C * (self.matrix_A ** p), 0 )

		if observabilityMatrix.rank() == self.matrix_A.n:
			self.observable = True
		else:
			self.observable = False

	### Метод self.stabilityCheck()
	### Args: -
	### Return: -
	### Метод проверяет систему на устойчивость	
	def stabilityCheck(self):
		self.stable = True

		den = self.TransferFunction[1]
		den_roots = den.r
		for root in den_roots:
			r = complex(root)
			# Если реальная часть корня положительна, что система неустойчива
			if r.real > 0:
				self.stable = False
				break

	### Метод self.parse_string()
	### Args: str_matrix - матрица в виде строки, выгруженной из поля ввода
	### Return: res - объект Matrix() 
	### Метод переводит матрицу в виде строки в объект Matrix()
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

	### Метод self.clear_fields()
	### Args: -
	### Return: -
	### Метод очищает поля для ввода
	def clear_fields(self):
		self.A_field.clear()
		self.B_field.clear()
		self.C_field.clear()
		self.TF_field.clear()
		self.SystemQualitiesField.clear()

def main():
	# Новый экземпляр QApplication
	app = QtWidgets.QApplication(sys.argv)
	# Создаём объект класса ExampleApp
	window = Interface()
	# Показываем окно
	window.show()
	# Запускаем приложение
	app.exec_()

if __name__ == '__main__':
	main()

