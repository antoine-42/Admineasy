# -*- mode: python -*-

block_cipher = None


uninstaller_a = Analysis(['../../uninstaller/uninstaller.py'],
             pathex=['/home/antoine/git/admineasy/client'],
             binaries=[],
             datas=[ ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
uninstaller_pyz = PYZ(uninstaller_a.pure, uninstaller_a.zipped_data,
             cipher=block_cipher)
uninstaller_exe = EXE(uninstaller_pyz,
          uninstaller_a.scripts,
          exclude_binaries=True,
          name='harvester-uninstaller',
          debug=False,
          strip=False,
          upx=True,
          console=True )
uninstaller_coll = COLLECT(uninstaller_exe,
               uninstaller_a.binaries,
               uninstaller_a.zipfiles,
               uninstaller_a.datas,
               strip=False,
               upx=True,
               name='harvester-uninstaller')
