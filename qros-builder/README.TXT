Step 1:

Build the qr codes from the .img file

python3 qros_build.py

Step 2: *MOVE ORIGINAL IMG FILE BEFORE THIS STEP*

Build a new .img file from the qr codes and launch it with qemu.

python3 qros_build_qemu.py


NOTES:

Good for testing from terminal:

qemu-system-i386 -m 512 -fda kolibri.img -boot a

Needed in script:
qemu_command = ["qemu-system-i386", "-m", "512", "-boot", "a", "-fda", img_file_path]