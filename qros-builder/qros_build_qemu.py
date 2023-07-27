import glob
import gzip
import base64
from pyzbar.pyzbar import decode
from PIL import Image
import subprocess
import time
import os

def decode_qr_code(file_path):
    # Open the QR code image file
    img = Image.open(file_path)

    # Decode the QR code
    decoded_objects = decode(img)

    # Extract the data from the first QR code
    data = decoded_objects[0].data.decode("utf-8")

    return base64.urlsafe_b64decode(data)

def decompress_data(encoded_data):
    # Decompress the data
    decompressed_data = gzip.decompress(encoded_data)

    return decompressed_data

def write_to_file(data, file_path):
    # Write the data to a file
    with open(file_path, "wb") as f:
        f.write(data)

def launch_qemu(img_file_path):
    # Define the QEMU command
    qemu_command = ["qemu-system-i386", "-m", "512", "-boot", "a", "-fda", img_file_path]

    # Launch QEMU as a subprocess without redirecting the standard streams
    qemu_process = subprocess.Popen(qemu_command)

    # Wait for QEMU process to finish, this will ensure that Python releases file lock
    qemu_process.wait()

    # Note: we're not handling QEMU's exit code here,
    # you may want to add code to handle it if necessary

# Define the path to the output .img file
img_file_path = "kolibri.img"

# Check if the img_file_path already exists
if os.path.exists(img_file_path):
    print(f"IMG file '{img_file_path}' already exists. Skipping QEMU launch.")
    launch_qemu(img_file_path)
else:
    # Get a list of all .png files in the current directory
    qr_code_file_paths = glob.glob("./qrs/compressed_qr_code_base64_*.png")

    # Define a custom sorting function
    def sort_key(file_path):
        # Extract the number from the filename
        number = int(file_path.split('_')[-1].split('.')[0])
        return number

    # Sort the file paths in numeric order
    qr_code_file_paths.sort(key=sort_key)

    # Initialize an empty list to hold the data from each QR code
    data_chunks = []

    # Decode each QR code and append it to the list
    for file_path in qr_code_file_paths:
        decoded_data = decode_qr_code(file_path)
        print(f"Size of data from {file_path}: {len(decoded_data)}")
        data_chunks.append(decoded_data)

    # Concatenate the data chunks
    data = b"".join(data_chunks)

    # Print the total size of data after concatenation
    print(f"Total size of data after concatenation: {len(data)}")

    # Decompress the data
    decompressed_data = decompress_data(data)

    # Write the data to the .img file
    write_to_file(decompressed_data, img_file_path)

    # Launch QEMU
    launch_qemu(img_file_path)

    # After launching QEMU, the script will continue to execute and release resources
    print("QEMU has been launched.")
