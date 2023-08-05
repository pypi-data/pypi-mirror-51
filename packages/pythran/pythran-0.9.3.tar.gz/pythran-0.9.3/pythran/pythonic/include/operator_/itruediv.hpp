#ifndef PYTHONIC_INCLUDE_OPERATOR_ITRUEDIV_HPP
#define PYTHONIC_INCLUDE_OPERATOR_ITRUEDIV_HPP

#include "pythonic/include/utils/functor.hpp"
#include "pythonic/include/operator_/truediv.hpp"

PYTHONIC_NS_BEGIN

namespace operator_
{
  template <class A, class B>
  auto itruediv(A const &a, B const &b) -> decltype(truediv(a, b));

  template <class A, class B>
  auto itruediv(A &a, B const &b) ->
      typename std::enable_if<std::is_same<A, decltype(truediv(a, b))>::value,
                              A &>::type;

  template <class A, class B>
  auto itruediv(A &a, B const &b) ->
      typename std::enable_if<!std::is_same<A, decltype(truediv(a, b))>::value,
                              decltype(truediv(a, b))>::type;

  DEFINE_FUNCTOR(pythonic::operator_, itruediv);
}
PYTHONIC_NS_END

#endif
