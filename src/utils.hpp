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

#include <algorithm>
#include <string>

namespace xcfun {
namespace detail {
// Hand-rolled std::equal, which is otherwise available only since C++14
template <class InputIt1, class InputIt2, class BinaryPredicate>
auto equal(InputIt1 first1, InputIt1 last1, InputIt2 first2, BinaryPredicate p)
    -> bool {
  for (; first1 != last1; ++first1, ++first2) {
    if (!p(*first1, *first2)) {
      return false;
    }
  }
  return true;
}

auto iequals(const std::string & a, const std::string & b) -> bool {
  return equal(a.cbegin(), a.cend(), b.cbegin(), b.cend(), [](char a, char b) {
    return std::tolower(a) == std::tolower(b);
  });
}

auto lowercase(std::string s) noexcept -> std::string {
  std::transform(
      s.begin(), s.end(), s.begin(), std::ptr_fun<int, int>(std::tolower));
  return s;
}

auto lowercase(const char * src) noexcept -> std::string {
  std::string tmp(src);
  return lowercase(tmp);
}

auto uppercase(std::string s) noexcept -> std::string {
  std::transform(
      s.begin(), s.end(), s.begin(), std::ptr_fun<int, int>(std::toupper));
  return s;
}

auto uppercase(const char * src) noexcept -> std::string {
  std::string tmp(src);
  return uppercase(tmp);
}
} // namespace detail
} // namespace xcfun
