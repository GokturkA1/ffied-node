{
  'targets': [
    # ----------------------------------------------------------------------
    # HEDEF 1: RUST STATİK KÜTÜPHANESİNİ DERLEYEN VE HAZIRLAYAN HEDEF ('ffi')
    # ----------------------------------------------------------------------
    {
      'target_name': 'ffi',
      'type': 'none',
      
      'conditions': [
        # === WINDOWS MSVC ===
        ['OS=="win"', {
          'actions': [
            {
              'action_name': 'build_rust_win',
              'inputs': ['Cargo.toml', 'src/lib.rs'],
              'outputs': ['<(PRODUCT_DIR)/ffi_rs.lib'],
              'action': [
                'cmd', '/c',
                'cargo build --release --target x86_64-pc-windows-msvc && ' +
                'copy /Y target\\x86_64-pc-windows-msvc\\release\\ffi_rs.lib <(PRODUCT_DIR)\\ffi_rs.lib'
              ],
              'message': 'Building Rust FFI-RS (Windows MSVC)...',
            }
          ],
          'direct_dependent_settings': {
            'libraries': [
              'ffi_rs.lib',
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

        # === UNIX / LINUX (Düzeltilen Kısım) ===
        ['OS!="win"', {
          'actions': [
            {
              'action_name': 'build_rust_unix',
              'inputs': ['Cargo.toml', 'src/lib.rs'],
              # Çıktı libffi_rs.a
              'outputs': ['<(PRODUCT_DIR)/libffi_rs.a'],
              'action': [
                'sh', '-c',
                'cargo build --release && ' +
                'cp target/release/libffi_rs.a <(PRODUCT_DIR)/libffi_rs.a'
              ],
              'message': 'Building Rust FFI-RS (Unix/Linux)...',
            }
          ],
          'direct_dependent_settings': {
            'libraries': [
              # STATİK KÜTÜPHANEYİ ZORLA DAHİL ETME (CRITICAL PATCH)
              '-Wl,--whole-archive',
              '<(PRODUCT_DIR)/libffi_rs.a',
              '-Wl,--no-whole-archive',
            ],
            'conditions': [
              ['OS=="linux"', {
                'libraries': [
                  # Rust Runtime ve libc bağımlılıkları
                  '-ldl',       
                  '-lpthread',  
                  '-lm',        
                  '-lrt',       
                  '-lc',       
                  '-lutil'
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
    },

    # ----------------------------------------------------------------------
    # HEDEF 2: NODE ADDON HEDEFİ ('ffi_rs')
    # ----------------------------------------------------------------------
    # Varsayılan olarak Node Addon hedefi (`binding.gyp`'de yer alan) 
    # bu 'ffi' hedefine bağımlı olmalıdır (dependencies: ['ffi']).
    # Eğer bu dosyayı (ffi.gyp) doğrudan Node'un ana derlemesine dahil ediyorsanız, 
    # bu hedefi burada tanımlamanıza gerek yoktur, ancak standart bir Node.js Addon yapısında 
    # bu hedef ana binding.gyp tarafından kullanılacaktır. 
    # Eğer bu ffi.gyp tek başına çalışıyorsa ve bir .node dosyası üretmek istiyorsa 
    # (ancak sorunuzdaki kodlar bunu yapmıyor, sadece Rust'ı hazırlıyor), 
    # aşağıdakine benzer bir hedef gereklidir:
    
    # {
    #   'target_name': 'ffi_rs',
    #   'type': 'shared_library', 
    #   'sources': [ 'node_ffi_rs.cc' ],
    #   'dependencies': [ 'ffi' ],
    # }
  ]
}