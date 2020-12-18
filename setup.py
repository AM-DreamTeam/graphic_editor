import os
import platform


if platform.system() == 'Windows':
    path = os.path.join(os.getcwd(), 'plugins','ghostscript.exe')
    os.chdir(os.getcwd())
    os.system(f'chcp 65001>nul&&"{path}"')
