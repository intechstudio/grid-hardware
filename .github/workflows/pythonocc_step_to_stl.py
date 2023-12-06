import os
from OCC.Extend.DataExchange import *

directory_path = './temp'  # Replace with the path to your directory

# List all files in the directory
file_list = [f for f in os.listdir(directory_path) if f.endswith('.step')]

# Process each .step file
for step_file in file_list:
    step_file_path = os.path.join(directory_path, step_file)
    print(f"Converting {step_file} to STL...")
    
    # Read STEP file
    shape = read_step_file(step_file_path)

    # Generate STL file name (replace .step with .stl)
    stl_file = os.path.splitext(step_file)[0] + '.stl'
    stl_file_path = os.path.join(directory_path, stl_file)

    # Write STL file
    write_stl_file(shape, stl_file_path, mode='binary', linear_deflection=0.1, angular_deflection=0.5)

    print(f"Conversion of {step_file} to {stl_file} complete\n")