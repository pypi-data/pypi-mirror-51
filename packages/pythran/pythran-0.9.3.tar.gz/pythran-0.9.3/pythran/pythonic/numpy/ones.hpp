#ifndef PYTHONIC_NUMPY_ONES_HPP
#define PYTHONIC_NUMPY_ONES_HPP

#include "pythonic/include/numpy/ones.hpp"

#include "pythonic/utils/functor.hpp"
#include "pythonic/types/ndarray.hpp"

PYTHONIC_NS_BEGIN

namespace numpy
{

  template <class pS, class dtype>
  types::ndarray<typename dtype::type, sutils::shape_t<pS>>
  ones(pS const &shape, dtype d)
  {
    return {(sutils::shape_t<pS>)shape, typename dtype::type(1)};
  }

  template <class dtype>
  types::ndarray<typename dtype::type, types::pshape<long>> ones(long size,
                                                                 dtype d)
  {
    return ones(types::pshape<long>(size), d);
  }
}
PYTHONIC_NS_END

#endif
