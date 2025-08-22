block_cipher = None

from PyInstaller.utils.hooks import collect_all

datas, binaries, hiddenimports = [], [], []
for module in ['torch', 'cv2', 'mss', 'torchvision', 'numpy']:
    tmp_datas, tmp_binaries, tmp_hidden = collect_all(module)
    datas += tmp_datas
    binaries += tmp_binaries
    hiddenimports += tmp_hidden

hiddenimports += ['torch.fx', 'torch.fx.experimental', 'torch.fx.experimental._config', 'torch._C._distributed_c10d']

binaries += [
    (r'C:\Users\SystemX\AppData\Local\Programs\Python\Python313\Lib\site-packages\cv2\opencv_videoio_ffmpeg4120_64.dll', 'cv2')
]

a = Analysis(
    ['sniker.pyw'],
    pathex=['.'],
    binaries=binaries,
    datas=datas + [('images', 'images'), ('themes.json', '.'), ('neyro', 'neyro')],
    hiddenimports=hiddenimports + [
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'mss',
        'cv2',
        'numpy',
        'pyautogui',
        'telegram',
        'telegram.ext',
        'telegram.Update',
        'telegram.ext.Application',        
        'telegram.ext.CommandHandler',     
        'telegram.ext.MessageHandler',     
        'telegram.ext.CallbackContext',
        'PIL',
        'PIL.Image',
        'PIL.ImageGrab',
        'PIL.ImageTk',
        'configparser',
        'threading',
        'time',
        'os',
        'ctypes',
        'datetime',
        'random',
        'sys',
        'socket',
        'io',
        'win32gui',
        'win32con',
        'pynput',
        'pynput.keyboard',
        'pynput.keyboard.Key',            
        'pynput.keyboard.Controller',     
        'pynput.keyboard.Listener',       
        'pynput.mouse',
        'pynput.mouse.Controller',        
        'pynput.mouse.Button',            
        'pynput.mouse.Listener',          
        'argparse',
        'mouse',                          
        'csv',                            
        'asyncio',
        'ttkthemes',
        're',
        'psutil',
        'json',
        'logging',
        'multiprocessing.connection',
        'GPUtil',
        'keyboard',
        'pyperclip',
        'torch',
        'torch.nn',
        'torchvision',
        'torchvision.transforms',
        'torch._C',  
        'torch.utils',
        'torchvision.models',
        'numpy.core.multiarray',  
        'scipy',  
        'wmi'
    ],
    runtime_hooks=['runtime_hook.py'],
    excludes=['torch.distributed'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='sniker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=['*.pyd', '*.dll'],
    runtime_tmpdir=None,
    console=False,
    icon='logo.ico',
    uac_admin=True
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='sniker'
)