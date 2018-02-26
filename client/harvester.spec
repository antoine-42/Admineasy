# -*- mode: python -*-

block_cipher = None


harvester_a = Analysis(['harvester\\harvester.py'],
             pathex=['C:\\Users\\Antoin\\Documents\\GitHub\\admineasy\\client'],
             binaries=[],
             datas=[ ('harvester/settings.json', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
setup_a = Analysis(['installer\\setup.py'],
             pathex=['C:\\Users\\Antoin\\Documents\\GitHub\\admineasy\\client'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
uninstaller_a = Analysis(['uninstaller\\uninstaller.py'],
             pathex=['C:\\Users\\Antoin\\Documents\\GitHub\\admineasy\\client'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

MERGE((harvester_a, "harvester", "harvester"), (setup_a, "setup", "setup"), (uninstaller_a, "uninstaller", "uninstaller"))

harvester_pyz = PYZ(harvester_a.pure, harvester_a.zipped_data,
             cipher=block_cipher)
harvester_exe = EXE(harvester_pyz,
          harvester_a.scripts,
          exclude_binaries=True,
          name='harvester',
          debug=False,
          strip=False,
          upx=True,
          console=True )
harvester_coll = COLLECT(harvester_exe,
               harvester_a.binaries,
               harvester_a.zipfiles,
               harvester_a.datas,
               strip=False,
               upx=True,
               name='harvester')

setup_pyz = PYZ(setup_a.pure, setup_a.zipped_data,
             cipher=block_cipher)
setup_exe = EXE(setup_pyz,
          setup_a.scripts,
          exclude_binaries=True,
          name='harvester setup',
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
               name='harvester setup')

uninstaller_pyz = PYZ(uninstaller_a.pure, uninstaller_a.zipped_data,
             cipher=block_cipher)
uninstaller_exe = EXE(uninstaller_pyz,
          uninstaller_a.scripts,
          exclude_binaries=True,
          name='harvester uninstaller',
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
               name='harvester uninstaller')
