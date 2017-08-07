# -*- mode: python -*-

block_cipher = None


data_files = [("img", "img")]

a = Analysis(['editor.py'],
             pathex=['/home/marek/Desktop/blockly-master'],
             binaries=[],
             datas=data_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='editor',
          debug=False,
          strip=False,
          upx=True,
          console=True,
          icon="win_icon.ico" )
