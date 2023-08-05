# -*- mode: python -*-

block_cipher = None


a = Analysis(['run.py'],
             pathex=['/home/johntourtellott/projects/misc/git/sidegears/examples/webruntime'],
             binaries=[],
             datas=[('wr-venv/lib/python3.7/site-packages/jsonrpcserver/request-schema.json',
                'jsonrpcserver')],
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
          [],
          exclude_binaries=True,
          name='run',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='run')
