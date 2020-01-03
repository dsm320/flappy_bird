# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
    ('imgs/*.png', 'imgs'),
    ('config-feedforward.txt', '.'),
    ('highscore.txt', '.')
]

a = Analysis(['flappy_bird.py'],
             pathex=['/home/dsmancuso/Code/Python/flappy_bird'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='flappy_bird',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
