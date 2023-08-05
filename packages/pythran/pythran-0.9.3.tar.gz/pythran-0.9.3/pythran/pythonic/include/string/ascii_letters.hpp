#ifndef PYTHONIC_INCLUDE_STRING_ASCII_LETTERS_HPP
#define PYTHONIC_INCLUDE_STRING_ASCII_LETTERS_HPP

#include "pythonic/types/str.hpp"

PYTHONIC_NS_BEGIN

namespace string
{

  types::str constexpr ascii_letters(
      "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ");
}
PYTHONIC_NS_END

#endif
