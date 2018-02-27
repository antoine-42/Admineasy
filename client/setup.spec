# -*- mode: python -*-

block_cipher = None


setup_a = Analysis(['installer\\setup.py'],
             pathex=['C:\\Users\\Antoin\\Documents\\GitHub\\admineasy\\client'],
             binaries=[],
             datas=[ ('nssm.exe', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
setup_pyz = PYZ(setup_a.pure, setup_a.zipped_data,
             cipher=block_cipher)
setup_exe = EXE(setup_pyz,
          setup_a.scripts,
          exclude_binaries=True,
          name='harvester-setup',
          debug=False,
          strip=False,
          upx=True,
          console=True )
setup_coll = COLLECT(setup_exe,
               setup_a.binaries,
               setup_a.zipfiles,
               setup_a.datas,
               strip=False,
               upx=True,
               name='harvester-setup')
