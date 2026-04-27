'''
Let's try to catch and handle exceptions.
What can go wrong? 
'''

num = int(input("Enter a number: "))
result = 100 / num

results_storage = {}

def complex_workflow(file_path):
    # Step 1: Open a file and read data
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Step 2: Process the file data
    data = []
    for line in lines:
        num = int(line.strip()) 
        data.append(num)

    result = sum(data) / len(data) 

    results_storage[file_path] = result
    print(f"Result for {file_path}: {result}")


# Call the function
complex_workflow('data1.txt')
# complex_workflow('data2.txt')
