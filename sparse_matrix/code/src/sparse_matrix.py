import os

class SparseMatrix:
    def __init__(self, matrixFilePath=None, numRows=0, numCols=0):
        self.numRows = numRows
        self.numCols = numCols
        self.elements = {}
        if matrixFilePath:
            self.loadFromFile(matrixFilePath)
    
    def loadFromFile(self, matrixFilePath):
        print(f"Loading matrix from file: {matrixFilePath}") 
        with open(matrixFilePath, 'r') as file:
            lines = file.readlines()
            try:
                self.numRows = int(lines[0].split('=')[1].strip())
                self.numCols = int(lines[1].split('=')[1].strip())
            except (IndexError, ValueError) as e:
                raise ValueError("Input file has wrong format: invalid rows/cols definition")

            for line in lines[2:]:
                if line.strip():
                    if not line.startswith('(') or not line.endswith(')'):
                        raise ValueError(f"Input file has wrong format: {line.strip()}")
                    parts = line[1:-1].split(',')
                    if len(parts) != 3:
                        raise ValueError(f"Input file has wrong format: {line.strip()}")
                    try:
                        row = int(parts[0].strip())
                        col = int(parts[1].strip())
                        value = int(parts[2].strip())
                        self.setElement(row, col, value)
                    except ValueError:
                        raise ValueError(f"Input file has wrong format: {line.strip()}")

    def getElement(self, currRow, currCol):
        return self.elements.get((currRow, currCol), 0)

    def setElement(self, currRow, currCol, value):
        if value != 0:
            self.elements[(currRow, currCol)] = value
        elif (currRow, currCol) in self.elements:
            del self.elements[(currRow, currCol)]

    def add(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrix dimensions must agree for addition")
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)
        result.elements = self.elements.copy()
        for (row, col), value in other.elements.items():
            result.setElement(row, col, result.getElement(row, col) + value)
        return result

    def subtract(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrix dimensions must agree for subtraction")
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)
        result.elements = self.elements.copy()
        for (row, col), value in other.elements.items():
            result.setElement(row, col, result.getElement(row, col) - value)
        return result

    def multiply(self, other):
        if self.numCols != other.numRows:
            raise ValueError("Matrix dimensions must agree for multiplication")
        result = SparseMatrix(numRows=self.numRows, numCols=other.numCols)
        for (row1, col1), value1 in self.elements.items():
            for col2 in range(other.numCols):
                if (col1, col2) in other.elements:
                    result.setElement(row1, col2, result.getElement(row1, col2) + value1 * other.getElement(col1, col2))
        return result

    def __str__(self):
        result = f"rows={self.numRows}\ncols={self.numCols}\n"
        for (row, col), value in sorted(self.elements.items()):
            result += f"({row}, {col}, {value})\n"
        return result.strip()

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_input_path = os.getenv('DSA_BASE_INPUT_PATH', os.path.join(script_dir, '../../sample_inputs/'))
    base_output_path = os.getenv('DSA_BASE_OUTPUT_PATH', script_dir)
    
    matrix1_path = os.path.join(base_input_path, "easy_sample_01_1.txt")
    matrix2_path = os.path.join(base_input_path, "easy_sample_01_2.txt")
    
    print(f"Matrix 1 path: {matrix1_path}") 
    print(f"Matrix 2 path: {matrix2_path}") 
    
    if not os.path.isfile(matrix1_path):
        print(f"File not found: {matrix1_path}")
        return
    if not os.path.isfile(matrix2_path):
        print(f"File not found: {matrix2_path}")
        return

    try:
        matrix1 = SparseMatrix(matrix1_path)
        matrix2 = SparseMatrix(matrix2_path)
    except ValueError as e:
        print(e)
        return
    
    operation = input("Enter the operation to perform (add, subtract, multiply): ").strip().lower()
    
    if operation == 'add':
        result = matrix1.add(matrix2)
        result_file = "addition_result.txt"
    elif operation == 'subtract':
        result = matrix1.subtract(matrix2)
        result_file = "subtraction_result.txt"
    elif operation == 'multiply':
        result = matrix1.multiply(matrix2)
        result_file = "multiplication_result.txt"
    else:
        print("Invalid operation")
        return
    
    output_path = os.path.join(base_output_path, result_file)
    with open(output_path, 'w') as file:
        file.write(str(result))
    print(f"Result saved to {output_path}")

if __name__ == "__main__":
    main()
