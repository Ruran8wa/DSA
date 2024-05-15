import os

def process_file(input_file_path, output_file_path):
    seen = [False] * 2047

    with open(input_file_path, 'r') as input_file:
        for line in input_file:
            line = line.strip()
            if line:
                if len(line.split()) == 1:
                    try:
                        num = int(line)
                        if -1023 <= num <= 1023:
                            seen[num + 1023] = True
                    except ValueError:
                        pass

    with open(output_file_path, 'w') as output_file:
        for i in range(len(seen)):
            if seen[i]:
                output_file.write(str(i - 1023) + '\n')


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    input_file_path = os.path.join(current_dir, "..", "..", "sample_inputs", "sample_01.txt")
    output_file_path = os.path.join(current_dir, "..", "..", "sample_results", "sample_01.txt_result.txt")
    
    process_file(input_file_path, output_file_path)