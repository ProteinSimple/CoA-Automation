# -*- mode: python ; coding: utf-8 -*-
import os
import glob

res_dir = "src/res"
res_files = []

for file in glob.glob(f"{res_dir}/**/*", recursive=True):
    if os.path.isfile(file):
        relative_path = os.path.relpath(file, res_dir)
        res_files.append((file, os.path.join("res", os.path.dirname(relative_path))))

a = Analysis(
    ['src\\main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/config.yaml', '.'),
        *res_files,
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
    destdir='target'
)
