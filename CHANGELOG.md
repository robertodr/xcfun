# Change Log

## [Unreleased]

### Added

- The macro `XCFun_ERROR` to report error conditions and quit program execution.
- The macro `XCFun_WARNING` to warn library users.

### Changed

- **BREAKING** Rather than returning error codes, the library now directly
  aborts with an error message pointing to the function, file, and line that
  generated the error condition.

### Removed

- The `xcfun::die` function.

### Fixed

## [Version 2.0.0a3] - 2020-01-31

We have introduced a number of breaking changes, motivated by the need to
modernize the library. See the [migration guide](docs/migration.rst).

### Added

- API functions `xcfun_which_vars` and `xcfun_which_mode`.
- A full example, based on CMake as build system generator, showing how to use
  the library from a Fortran host.
- A full example, based on CMake as build system generator, showing how to use
  the library from a C host.

### Changed

- **BREAKING** All API functions are uniformly namespaced with the `xcfun_` prefix.
- **BREAKING** The Fortran interface has been completely rewritten using
  `iso_c_binding`: the library can now be compiled without the use of neither a
  C nor a Fortran compiler. :confetti_ball:
- **BREAKING** CMake option `XCFun_XC_MAX_ORDER` renamed to `XCFUN_MAX_ORDER`. New default value of 6.
- **BREAKING** CMake option `XCFun_ENABLE_PYTHON_INTERFACE` renamed to `XCFUN_PYTHON_INTERFACE`.

### Deprecated

### Removed

- **BREAKING** API functions `xc_serialize`, `xc_deserialize`, `xc_set_fromstring`, and `xc_derivative_index`.
- **BREAKING** The CMake options `ENABLE_FC_SUPPORT` and `ENABLE_64BIT_INTEGERS`.

### Fixed

### Security

## [Version 2.0.0a2] - 2020-01-21

## [Version 2.0.0a1] - 2019-12-15

### Added

- A user-friendly API function to set up functional evaluation `xc_user_eval_setup`. Thanks @ilfreddy.

### Changed

- **BREAKING** A compiler compliant with the C++11 (or later) standard is required.
- **BREAKING** CMake >= 3.11 is required to configure the code. 
- **BREAKING** The Python bindings are now generated using [pybind11] instead of
  SWIG. The dependency will be fetched at configuration time if not found on
  your system.
- **BREAKING** The Fortran interface is no longer build with the code, but
  shipped as a separate file to be compiled within your own Fortran code.

[Unreleased]: https://github.com/dftlibs/xcfun/compare/v2.0.0a3...HEAD
[Version 2.0.0a3]: https://github.com/dftlibs/xcfun/compare/v2.0.0a2...v2.0.0a3
[Version 2.0.0a2]: https://github.com/dftlibs/xcfun/compare/v2.0.0a1...v2.0.0a2
[Version 2.0.0a1]: https://github.com/dftlibs/xcfun/releases/tag/v2.0.0a1

[GitHub]: https://github.com/dftlibs/xcfun
[pybind11]: https://pybind11.readthedocs.io
