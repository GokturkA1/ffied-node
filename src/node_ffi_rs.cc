#include "node_api.h"

// Rust tarafındaki özel giriş kapısı
extern "C" napi_value ffi_rs_extension_entry(napi_env env, napi_value exports);

// Wrapper fonksiyonu
napi_value Init(napi_env env, napi_value exports) {
    return ffi_rs_extension_entry(env, exports);
}


void RegisterFFI() {
    static napi_module _module = {
        NAPI_MODULE_VERSION,
        0,              // nm_flags
        __FILE__,       // nm_filename
        Init,           // nm_register_func (Bizim wrapper)
        "ffi",       // nm_modname (JS tarafında _linkedBinding('ffi_rs') ile çağırılacak)
        0,              // nm_priv
        {0},            // reserved
    };
    
    // N-API'nin kayıt defterine ekle
    napi_module_register(&_module);
}

// Bu struct program başlar başlamaz (main'den önce) oluşur 
// ve constructor içinde kayıt işlemini yapar.
struct AutoRegister {
    AutoRegister() {
        RegisterFFI();
    }
};

static AutoRegister _auto_register;