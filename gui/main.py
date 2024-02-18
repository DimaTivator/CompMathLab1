import math

from compmath import SimpleIterationSolver, SoleData

from parse import get_matrix_vector

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic


sole = SoleData()


class SimpleIterationApp(QMainWindow):
    def __init__(self):
        super(SimpleIterationApp, self).__init__()
        uic.loadUi("gui/simple_iteration_main.ui", self)
        self.show()
        self.initUI()

        self.history = []
        self.eps = 0.001
        self.power = 3
        self.criterion = 'abs_deviation'

    def initUI(self):
        self.setWindowTitle("Simple Iteration Method")

        # add a user guide hyperlink
        self.guide_link_label.setText("<a href='https://github.com/DimaTivator/CompMathLab1/blob/main/README.md'>"
                                      + self.guide_link_label.text() + "</a>")
        self.guide_link_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.guide_link_label.setOpenExternalLinks(True)

        # matrix and vector input buttons
        self.A_input_button.clicked.connect(lambda: MatrixInputWindow().exec_())
        self.b_input_button.clicked.connect(lambda: VectorInputWindow().exec_())

        # pig image
        pixmap = QPixmap("gui/img/pig.png")
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

        # solve button
        self.solve_button.clicked.connect(self.solve)

        # accuracy input
        validator = QRegExpValidator(QRegExp("[+-]?\\d*\\.?\\d+"))
        self.accuracy_input.setValidator(validator)
        self.accuracy_input.setText('0.001')
        self.accuracy_input.textChanged.connect(self.parse_accuracy)

        # criterion input
        self.criterion_input.setText('abs_deviation')
        self.criterion_input.textChanged.connect(self.parse_criterion)

        # browse files
        self.browse_button.clicked.connect(self.browse_files)

        # load file button
        self.load_button.clicked.connect(self.load_file)

    def solve(self):
        solver = SimpleIterationSolver(eps=self.eps, criterion=self.criterion)

        try:
            self.history = solver.solve(A=sole.A, b=sole.b)
        except ValueError as e:
            QMessageBox.warning(self, 'Error', str(e))
            return

        self.fill_history_table()

    """
    Files
    """

    def browse_files(self):
        file_filter = "Text files *.txt"
        fname = QFileDialog.getOpenFileName(self, 'Open file', '', file_filter)
        self.filename_input.setText(fname[0])

    def load_file(self):
        fname = self.filename_input.text()

        try:
            with open(fname, 'r') as f:
                lines = f.readlines()

            n, A, b = get_matrix_vector(lines)

            sole.n = n
            sole.m = n

            for i in range(n):
                for j in range(n):
                    sole.set_A(i, j, A[i][j])

            for i in range(n):
                sole.set_b(i, b[i][0])

        except FileNotFoundError:
            QMessageBox.warning(self, 'Error', 'File not found')
            return

        except Exception as e:
            QMessageBox.warning(self, 'Error',
                                f'{str(e)}\nInvalid file format. Read the documentation for more information')

    """
    Fill the table 
    """

    def fill_history_table(self):
        num_rows = len(self.history)
        num_cols = len(self.history[0][0]) + 1

        self.history_table.setRowCount(num_rows)
        self.history_table.setColumnCount(num_cols)

        for i, (x, inaccuracy) in enumerate(self.history):
            for j, value in enumerate(x):
                val = str(value).replace('[', '').replace(']', '')
                val = str(round(float(val), self.power))

                item = QTableWidgetItem(val)
                self.history_table.setItem(i, j, item)

            try:
                item = QTableWidgetItem(str(round(float(inaccuracy), self.power)))
            except ValueError:
                item = QTableWidgetItem(str(inaccuracy))

            self.history_table.setItem(i, num_cols - 1, item)

        self.history_table.setHorizontalHeaderLabels(
            ["x" + str(i + 1) for i in range(len(self.history[0][0]))] + ["Inaccuracy"])

    """
    Parse the arguments
    """

    def parse_accuracy(self, text):
        try:
            self.eps = float(text)
        except ValueError:
            pass

        m, e = math.frexp(self.eps)
        self.power = abs(int(e * math.log10(2))) + 1

    def parse_criterion(self, text):
        self.criterion = text.lower().strip()


class NumericInputWindow(QDialog):
    def __init__(self):
        super(NumericInputWindow, self).__init__()

    def on_key_press(self, event, item):
        key = event.key()
        text = item.text()
        print(key, text)
        if not (ord('0') <= key <= ord('9')) and key != ord('.') and key != ord('-'):
            event.ignore()
        else:
            # allow only one point
            if key == ord('.'):
                if "." in text:
                    event.ignore()
            # allow minus sign only if it is the first character
            elif key == ord('-'):
                if len(text) > 0:
                    event.ignore()
            else:
                super().keyPressEvent(event)


class MatrixInputWindow(NumericInputWindow):
    def __init__(self):
        super(MatrixInputWindow, self).__init__()
        uic.loadUi("gui/matrix_input.ui", self)
        self.show()

        self.default_cell_size = 44

        self.initUI()
        self.create_matrix()

    def initUI(self):
        self.matrix_size_spinbox.valueChanged.connect(self.create_matrix)

        self.table_widget.setStyleSheet("QTableWidget::item:selected { background-color: lightgray; }")

        self.table_widget.setColumnWidth(0, self.default_cell_size)
        self.table_widget.setRowHeight(0, self.default_cell_size)

        self.load_data()

    def load_data(self):
        if sole.n is None:
            return

        self.matrix_size_spinbox.setValue(sole.n)

    def create_matrix(self):
        size = self.matrix_size_spinbox.value()

        sole.n = size
        sole.m = size

        self.table_widget.clear()
        self.table_widget.setRowCount(size)
        self.table_widget.setColumnCount(size)

        column_width = self.default_cell_size - size
        row_height = self.default_cell_size - size

        for i in range(size):
            self.table_widget.setColumnWidth(i, column_width)
            self.table_widget.setRowHeight(i, row_height)
            for j in range(size):
                cell_item = QTableWidgetItem()
                cell_item.setData(Qt.DisplayRole, str(sole.A[i][j]))

                self.table_widget.setItem(i, j, cell_item)

                # Connect keyPressEvent for each cell to restrict input to numbers
                # cell_item.keyPressEvent = lambda event, item=cell_item: self.on_key_press(event, item)

        self.table_widget.cellChanged.connect(self.update_matrix)

    def update_matrix(self, i, j):
        item = self.table_widget.item(i, j)
        if item is not None:
            try:
                value = float(item.text())
                sole.set_A(i, j, value)
            except ValueError:
                item.setText(str(sole.A[i][j]))


class VectorInputWindow(NumericInputWindow):
    def __init__(self):
        super(VectorInputWindow, self).__init__()
        uic.loadUi("gui/vector_input.ui", self)
        self.show()

        self.default_cell_height = 30
        self.default_cell_width = 44

        self.initUI()
        self.create_vector()

    def initUI(self):
        self.vector_size_spinbox.valueChanged.connect(self.create_vector)

        self.table_widget.setStyleSheet("QTableWidget::item:selected { background-color: lightgray; }")

        self.table_widget.setColumnWidth(0, self.default_cell_width)
        self.table_widget.setRowHeight(0, self.default_cell_height)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.horizontalHeader().setVisible(False)

        self.load_data()

    def load_data(self):
        if sole.n is None:
            return

        self.vector_size_spinbox.setValue(sole.n)

    def create_vector(self):
        size = self.vector_size_spinbox.value()

        sole.n = size
        sole.m = size

        self.table_widget.clear()
        self.table_widget.setRowCount(size)

        row_height = self.default_cell_height - size

        for i in range(size):
            cell_item = QTableWidgetItem()
            cell_item.setData(Qt.DisplayRole, str(sole.b[i][0]))

            self.table_widget.setRowHeight(i, row_height)
            self.table_widget.setItem(i, 0, cell_item)

            # Connect keyPressEvent for each cell to restrict input to numbers
            # cell_item.keyPressEvent = lambda event, item=cell_item: self.on_key_press(event, item)

        self.table_widget.cellChanged.connect(self.update_vector)

    def update_vector(self, i, j):
        item = self.table_widget.item(i, j)
        if item is not None:
            try:
                value = float(item.text())
                sole.set_b(i, value)
            except ValueError:
                item.setText(str(sole.b[i][j]))


def main():
    app = QApplication([])
    window = SimpleIterationApp()

    app.exec_()


if __name__ == '__main__':
    main()

