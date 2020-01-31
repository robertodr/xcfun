/*
 * XCFun, an arbitrary order exchange-correlation library
 * Copyright (C) 2020 Ulf Ekström and contributors.
 *
 * This file is part of XCFun.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 * For information on the complete list of contributors to the
 * XCFun library, see: <https://xcfun.readthedocs.io/>
 */

#pragma once

#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <string>

namespace xcfun {
namespace detail {
inline auto message_to_user(const char * message,
                            const char * func,
                            int line,
                            const char * fname,
                            bool report_issue) -> std::string {
  std::ostringstream err;
  err << "XCFun fatal error.\n"
      << " In function " << func << " at line " << line << " of file " << fname
      << "\n"
      << message << std::endl;
  if (report_issue) {
    err << "Please report this issue: https://github.com/dftlibs/xcfun/issues"
        << std::endl;
  }
  return err.str();
}

inline auto message_to_user(const std::string & message,
                            const char * func,
                            int line,
                            const char * fname,
                            bool report_issue) -> std::string {
  return message_to_user(message.c_str(), func, line, fname, report_issue);
}

inline auto message_to_user(const std::ostringstream & message,
                            const char * func,
                            int line,
                            const char * fname,
                            bool report_issue) -> std::string {
  return message_to_user(message.str().c_str(), func, line, fname, report_issue);
}
} // namespace detail
} // namespace xcfun

/// Macro to be used to signal error conditions
#define XCFun_ERROR(message)                                                        \
  {                                                                                 \
    auto errmsg = xcfun::detail::message_to_user(                                   \
        message, __func__, __LINE__, __FILE__, false);                              \
    std::fprintf(stderr, "%s\n", errmsg.c_str());                                   \
    std::exit(EXIT_FAILURE);                                                        \
  }

/// Macro to be used to signal non-fatal error conditions
#define XCFun_WARNING(message)                                                      \
  {                                                                                 \
    auto errmsg = xcfun::detail::message_to_user(                                   \
        message, __func__, __LINE__, __FILE__, true);                               \
    std::fprintf(stderr, "%s\n", errmsg.c_str());                                   \
  }
