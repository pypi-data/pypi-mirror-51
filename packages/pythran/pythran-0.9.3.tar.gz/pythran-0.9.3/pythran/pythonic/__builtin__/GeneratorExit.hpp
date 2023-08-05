#ifndef PYTHONIC_BUILTIN_GENERATOREXIT_HPP
#define PYTHONIC_BUILTIN_GENERATOREXIT_HPP

#include "pythonic/include/__builtin__/GeneratorExit.hpp"

#include "pythonic/types/exceptions.hpp"

PYTHONIC_NS_BEGIN

namespace __builtin__
{

  PYTHONIC_EXCEPTION_IMPL(GeneratorExit)
}
PYTHONIC_NS_END

#endif
