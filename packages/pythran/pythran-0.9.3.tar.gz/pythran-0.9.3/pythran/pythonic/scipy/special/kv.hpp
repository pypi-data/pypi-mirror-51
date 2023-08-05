#ifndef PYTHONIC_SCIPY_SPECIAL_KV_HPP
#define PYTHONIC_SCIPY_SPECIAL_KV_HPP

#include "pythonic/include/scipy/special/kv.hpp"

#include "pythonic/types/ndarray.hpp"
#include "pythonic/utils/functor.hpp"
#include "pythonic/utils/numpy_traits.hpp"

#define BOOST_MATH_THREAD_LOCAL thread_local
#include <boost/math/special_functions/bessel.hpp>

PYTHONIC_NS_BEGIN

namespace scipy
{
  namespace special
  {
    namespace details
    {
      template <class T0, class T1>
      double kv(T0 x, T1 y)
      {
        using namespace boost::math::policies;
        return boost::math::cyl_bessel_k(x, y,
                                         make_policy(promote_double<true>()));
      }
    }

#define NUMPY_NARY_FUNC_NAME kv
#define NUMPY_NARY_FUNC_SYM details::kv
#include "pythonic/types/numpy_nary_expr.hpp"
  }
}
PYTHONIC_NS_END

#endif
