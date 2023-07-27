import os

file_path = 'kolibri.img'  # Replace this with the actual file path

# Get the byte size of the file
file_size = os.path.getsize(file_path)

print(f"Size of the file '{file_path}': {file_size} bytes")
