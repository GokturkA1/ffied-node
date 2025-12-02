{
  'targets': [
    {
      'target_name': 'ffi',
      'type': 'none',
      
      'conditions': [
        # ======================================================================
        # 1. WINDOWS (MSVC)
        # ======================================================================
        ['OS=="win"', {
          'actions': [
            {
              'action_name': 'build_rust_win',
              'inputs': ['Cargo.toml', 'src/lib.rs'],
              'outputs': ['<(PRODUCT_DIR)/ffi.lib'],
              'action': [
                'cmd', '/c',
                'cargo build --release --target x86_64-pc-windows-msvc && ' +
                'copy /Y target\\x86_64-pc-windows-msvc\\release\\ffi.lib <(PRODUCT_DIR)\\ffi.lib'
              ],
              'message': 'Building Rust FFI-RS (Windows MSVC)...',
            }
          ],
          'direct_dependent_settings': {
            'libraries': [
              'ffi.lib',
              'ntdll.lib',
              'userenv.lib',
              'bcrypt.lib',
              'advapi32.lib',
              'ws2_32.lib',
              'user32.lib',
              'dbghelp.lib'
            ],
          },
        }],

        # ======================================================================
        # 2. UNIX (LINUX - CODESPACE)
        # ======================================================================
        ['OS!="win"', {
          'actions': [
            {
              'action_name': 'build_rust_unix',
              'inputs': ['Cargo.toml', 'src/lib.rs'],
              # GYP'ye çıktının ffi.a olacağını söylüyoruz
              'outputs': ['<(PRODUCT_DIR)/ffi.a'],
              'action': [
                'sh', '-c',
                # 1. Derle (Cargo linux'ta libffi.a üretir)
                'cargo build --release && ' +
                # 2. Kopyalarken adını ffi.a yap (Sistem libffi.a ile karışmasın)
                'cp target/release/libffi.a <(PRODUCT_DIR)/ffi.a'
              ],
              'message': 'Building Rust FFI-RS (Unix/Linux)...',
            }
          ],
          'direct_dependent_settings': {
            'libraries': [
              # Linker'a tam yol veriyoruz
              '<(PRODUCT_DIR)/ffi.a',
            ],
            'conditions': [
              ['OS=="linux"', {
                'libraries': [
                  '-ldl',       # Dynamic Linker
                  '-lpthread',  # Threading
                  '-lm',        # Math
                  '-lrt'        # Realtime extensions
                ]
              }],
              ['OS=="mac"', {
                'libraries': [
                  '-framework CoreFoundation',
                  '-framework Security',
                  '-liconv',
                  '-lSystem'
                ]
              }]
            ]
          }
        }]
      ]
    }
  ]
}