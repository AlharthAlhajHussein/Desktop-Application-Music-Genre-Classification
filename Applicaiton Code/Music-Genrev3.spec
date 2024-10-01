# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Music-Genrev3.py'],
    pathex=[],
    binaries=[],
    datas=[('stacking_modelv3.pkl', '.'), ('scalerv2.pkl', '.'), ('window_icon.png', '.'), ('app_icon.ico', '.')],
    hiddenimports=['sklearn', 'sklearn.pipeline', 'sklearn.ensemble', 'sklearn.tree', 'sklearn.utils._typedefs', 'mlxtend', 'mlxtend.classifier'],
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
    a.binaries,
    a.datas,
    [],
    name='Music-Genrev3',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.ico',

)
