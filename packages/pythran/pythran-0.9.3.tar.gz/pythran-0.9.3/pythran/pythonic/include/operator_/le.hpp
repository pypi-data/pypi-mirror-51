#ifndef PYTHONIC_INCLUDE_OPERATOR_LE_HPP
#define PYTHONIC_INCLUDE_OPERATOR_LE_HPP

#include "pythonic/include/utils/functor.hpp"

PYTHONIC_NS_BEGIN

namespace operator_
{
  template <class A, class B>
  auto le(A const &a, B const &b) -> decltype(a <= b);
  bool le(char const *self, char const *other);

  DEFINE_FUNCTOR(pythonic::operator_, le);
}
PYTHONIC_NS_END

#endif
