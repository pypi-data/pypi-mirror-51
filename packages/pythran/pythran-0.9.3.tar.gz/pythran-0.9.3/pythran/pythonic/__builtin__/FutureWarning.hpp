#ifndef PYTHONIC_BUILTIN_FUTUREWARNING_HPP
#define PYTHONIC_BUILTIN_FUTUREWARNING_HPP

#include "pythonic/include/__builtin__/FutureWarning.hpp"

#include "pythonic/types/exceptions.hpp"

PYTHONIC_NS_BEGIN

namespace __builtin__
{

  PYTHONIC_EXCEPTION_IMPL(FutureWarning)
}
PYTHONIC_NS_END

#endif
