# -*- mode: python -*-

block_cipher = None


harvester_a = Analysis(['../../harvester/harvester.py'],
             pathex=['/home/antoine/git/admineasy/client'],
             binaries=[],
             datas=[ ('../../harvester/settings.json', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
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
