#ifndef PYTHONIC_BUILTIN_STR_ISALPHA_HPP
#define PYTHONIC_BUILTIN_STR_ISALPHA_HPP

#include "pythonic/include/__builtin__/str/isalpha.hpp"

#include "pythonic/types/str.hpp"
#include "pythonic/utils/functor.hpp"

PYTHONIC_NS_BEGIN

namespace __builtin__
{

  namespace str
  {

    bool isalpha(types::str const &s)
    {
      return !s.empty() && std::all_of(s.chars().begin(), s.chars().end(),
                                       (int (*)(int))std::isalpha);
    }
  }
}
PYTHONIC_NS_END
#endif
