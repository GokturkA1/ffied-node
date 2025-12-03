'use strict';

// Doğrudan C++ katmanındaki 'ffi_rs' modülüne bağlanıyoruz.
// Bu modülü src/node_ffi_rs.cc içinde NODE_MODULE_CONTEXT_AWARE_BUILTIN ile kaydettik.
const nativeBinding = process._linkedBinding('ffi_rs');

const { DataType, createPointer, restorePointer, unwrapPointer, wrapPointer, freePointer, open, close, load, isNullPointer, FFITypeTag } = nativeBinding;

DataType.StackStruct = 999;
DataType.Function = 998;
DataType.Array = 997;
DataType.StackArray = 996;

const arrayDataType = [DataType.I16Array, DataType.I32Array, DataType.StringArray, DataType.DoubleArray, DataType.U8Array, DataType.FloatArray];

const arrayConstructor = (options) => ({
  ffiTypeTag: FFITypeTag.Array,
  ...options
});

const processParamsTypeForArray = (params) => {
  params.paramsType = params.paramsType?.map((paramType, index) => {
    if (arrayDataType.includes(paramType)) {
      return arrayConstructor({
        type: paramType,
        length: params.paramsValue[index].length,
      });
    }
    return paramType;
  });
  return params;
};

const setFreePointerTag = (params) => {
  params.paramsType = params.paramsType?.map((paramType, index) => {
    if (paramType.ffiTypeTag === FFITypeTag.Function) {
      paramType.needFree = true;
    }
    return paramType;
  });
  return params;
};

const wrapLoad = (params) => {
  if (params.freeResultMemory === undefined) {
    params.freeResultMemory = false;
  }
  return load(processParamsTypeForArray(params));
};

// EXPORTS
// Buradaki exports, require('ffi-rs') çağrıldığında dönecek objedir.
module.exports = {
  DataType,
  PointerType: nativeBinding.PointerType,
  open,
  close,
  load: wrapLoad,
  isNullPointer,
  FFITypeTag,
  createPointer: (params) => createPointer(processParamsTypeForArray(params)),
  restorePointer: (params) => restorePointer(processParamsTypeForArray(params)),
  unwrapPointer: (params) => unwrapPointer(processParamsTypeForArray(params)),
  wrapPointer: (params) => wrapPointer(processParamsTypeForArray(params)),
  freePointer: (params) => freePointer(setFreePointerTag(processParamsTypeForArray(params))),
  arrayConstructor,
  funcConstructor: (options) => ({
    ffiTypeTag: FFITypeTag.Function,
    needFree: false,
    freeCFuncParamsMemory: false,
    ...options,
  }),
  define: (obj) => {
    const res = {};
    Object.entries(obj).map(([funcName, funcDesc]) => {
      res[funcName] = (paramsValue = []) => wrapLoad({
        ...funcDesc,
        funcName,
        paramsValue
      });
    });
    return res;
  }
};