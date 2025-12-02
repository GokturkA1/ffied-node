// ffi_rs_binding.d.ts (Node Internal Typings)

// 1. TEMEL TİPLER VE ENUMLAR (Dependencies First)
// ---------------------------------------------------------

interface RawPointer { }

export interface JsExternal {
  _externalDataPlaceholder: RawPointer;
}

export enum DataType {
  String = 0, WString = 15, I32 = 1, Double = 2, I32Array = 3, StringArray = 4, DoubleArray = 5,
  Boolean = 6, Void = 7, I64 = 8, U8 = 9, U8Array = 10, External = 11, U64 = 12, FloatArray = 13,
  Float = 14, BigInt = 16, I16 = 17, StructArray = 18, I16Array = 19, U32 = 20, 
  StackStruct = 999, StackArray = 996, Function = 998, Array = 997,
}

export enum PointerType { 
  RsPointer = 0, 
  CPointer = 1 
}

export enum FFITypeTag {
  StackStruct = DataType.StackStruct,
  StackArray = DataType.StackArray,
}

export interface OpenParams { 
  library: string; 
  path: string; 
}

// 2. KOMPLEKS TİPLER (Recursive Types)
// ---------------------------------------------------------

// Recursive tip tanımları (FieldType -> RecordFieldType -> FieldType)
export type FieldType = DataType | ArrayConstructorOptions | FuncConstructorOptions | RecordFieldType;

export interface RecordFieldType extends Record<string, FieldType> { }

export interface ArrayConstructorOptions {
  type: DataType;
  length: number;
  ffiTypeTag?: FFITypeTag;
  dynamicArray?: boolean;
  structItemType?: RecordFieldType;
}

export interface FuncConstructorOptions {
    paramsType: FieldType[];
    retType: FieldType;
    needFree?: boolean;
    freeCFuncParamsMemory?: boolean;
}

// 3. ANA ARAYÜZ (The Main Interface)
// ---------------------------------------------------------
// process.binding('ffi') çağrısı bu yapıyı döndürür.

export interface FfiRsBinding {
  // Enum Referansları (JS Runtime'da erişilebilir objeler)
  DataType: typeof DataType;
  PointerType: typeof PointerType;
  FFITypeTag: typeof FFITypeTag;

  // --- Pointer Manipülasyonları ---
  createPointer(params: {
    paramsType: FieldType[];
    paramsValue: unknown[];
  }): JsExternal[];
  
  restorePointer(params: {
    retType: FieldType[];
    paramsValue: JsExternal[];
  }): unknown;
  
  unwrapPointer(params: JsExternal[]): JsExternal[];
  wrapPointer(params: JsExternal[]): JsExternal[];
  freePointer(params: any): void; // 'any' kalabilir, karmaşık yapı

  // --- FFI Operasyonları ---
  open(params: OpenParams): void;
  close(library: string): void;
  
  // Ham Load Fonksiyonu
  load(params: {
      library: string;
      funcName: string;
      retType: FieldType;
      paramsType: FieldType[];
      paramsValue: unknown[];
  }): unknown;
  
  isNullPointer(params: JsExternal): boolean;
}