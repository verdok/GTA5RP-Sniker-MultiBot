import os
import sys

# This hook runs at runtime in the bundled EXE to add the cv2 DLL directory to the PATH
if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS  # PyInstaller temp directory in EXE
    cv2_dir = os.path.join(base_dir, 'cv2')
    if os.path.exists(cv2_dir):
        # Add to DLL search path (Python 3.8+)
        os.add_dll_directory(cv2_dir)
        # Add to PATH for older compatibility
        os.environ['PATH'] = cv2_dir + os.pathsep + os.environ.get('PATH', '')
        # Set OPENCV_DIR for cv2 loader
        os.environ['OPENCV_DIR'] = cv2_dir