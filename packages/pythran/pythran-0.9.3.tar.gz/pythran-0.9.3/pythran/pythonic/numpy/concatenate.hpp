#ifndef PYTHONIC_NUMPY_CONCATENATE_HPP
#define PYTHONIC_NUMPY_CONCATENATE_HPP

#include "pythonic/include/numpy/concatenate.hpp"

#include "pythonic/utils/functor.hpp"
#include "pythonic/types/ndarray.hpp"
#include "pythonic/__builtin__/sum.hpp"
#include "pythonic/__builtin__/ValueError.hpp"

PYTHONIC_NS_BEGIN

namespace numpy
{

  namespace details
  {

    template <size_t N>
    struct concatenate_helper {
      // list version
      template <class Out, class A>
      void operator()(Out &&out, A const &from, long axis) const
      {
        if (axis == 0) {
          auto out_iter = out.begin();
          for (auto &&ifrom : from)
            out_iter = std::copy(ifrom.begin(), ifrom.end(), out_iter);
        } else {
          std::vector<typename std::decay<decltype(from[0].begin())>::type>
              ifroms;
          for (auto &&ifrom : from)
            ifroms.emplace_back(ifrom.begin());
          std::vector<typename std::decay<decltype(*from[0].begin())>::type>
              difroms;

          for (auto &&iout : out) {
            difroms.clear();
            for (auto &&ifrom : ifroms)
              difroms.emplace_back(*ifrom);
            concatenate_helper<N - 1>()(iout, difroms, axis - 1);
            for (auto &ifrom : ifroms)
              ++ifrom;
          }
        }
      }
      // array version
      template <class Out, class A, size_t... I>
      void operator()(Out &&out, A const &from, long axis,
                      utils::index_sequence<I...>) const
      {
        if (axis == 0) {
          auto out_iter = out.begin();
          int _[] = {(out_iter = std::copy(std::get<I>(from).begin(),
                                           std::get<I>(from).end(), out_iter),
                      1)...};
        } else {
          types::array<typename A::value_type::const_iterator, sizeof...(I)>
              ifroms = {std::get<I>(from).begin()...};

          for (auto &&iout : out) {
            types::array<
                typename std::iterator_traits<
                    typename A::value_type::const_iterator>::value_type,
                sizeof...(I)> difroms = {*std::get<I>(ifroms)...};
            concatenate_helper<N - 1>()(iout, difroms, axis - 1,
                                        utils::index_sequence<I...>{});
            int _[] = {(++std::get<I>(ifroms), 0)...};
          }
        }
      }
      // tuple version
      template <class Out, class... Ts, size_t... I>
      void operator()(Out &&out, std::tuple<Ts...> const &from, long axis,
                      utils::index_sequence<I...>) const
      {
        if (axis == 0) {
          auto out_iter = out.begin();
          int _[] = {(out_iter = std::copy(std::get<I>(from).begin(),
                                           std::get<I>(from).end(), out_iter),
                      1)...};
        } else {
          auto ifroms = std::make_tuple(std::get<I>(from).begin()...);

          for (auto &&iout : out) {
            auto difroms = std::make_tuple(*std::get<I>(ifroms)...);
            concatenate_helper<N - 1>()(iout, difroms, axis - 1,
                                        utils::index_sequence<I...>{});
            int _[] = {(++std::get<I>(ifroms), 0)...};
          }
        }
      }
    };

    template <>
    struct concatenate_helper<0> {
      // list version - sentinel
      template <class Out, class A>
      void operator()(Out &&buffer, A const &from, long axis) const
      {
      }
      // array version
      template <class Out, class E, size_t... I>
      void operator()(Out &&, E const &, long,
                      utils::index_sequence<I...>) const
      {
      }
      // tuple version - sentinel
      template <class Out, class... Ts, size_t... I>
      void operator()(Out &&, std::tuple<Ts...> const &, long,
                      utils::index_sequence<I...>) const
      {
      }
    };

    template <class A, size_t... I>
    long concatenate_axis_size(A const &from, long axis,
                               utils::index_sequence<I...>)
    {
      long sizes[] = {sutils::array(std::get<I>(from).shape())[axis]...};
      return std::accumulate(std::begin(sizes), std::end(sizes), 0L,
                             std::plus<long>());
    }
  }

  template <class... Types>
  auto concatenate(std::tuple<Types...> const &args, long axis)
      -> types::ndarray<
          typename __combined<typename std::decay<Types>::type::dtype...>::type,
          types::array<
              long, std::tuple_element<0, std::tuple<Types...>>::type::value>>
  {
    using T =
        typename __combined<typename std::decay<Types>::type::dtype...>::type;
    auto constexpr N = std::decay<decltype(std::get<0>(args))>::type::value;
    auto shape = sutils::array(std::get<0>(args).shape());
    shape[axis] = details::concatenate_axis_size(
        args, axis, utils::make_index_sequence<sizeof...(Types)>{});

    types::ndarray<
        typename __combined<typename std::decay<Types>::type::dtype...>::type,
        types::array<
            long, std::decay<decltype(std::get<0>(args))>::type::value>> result{
        shape, types::none_type{}};
    details::concatenate_helper<N>()(
        result, args, axis, utils::make_index_sequence<sizeof...(Types)>{});
    return result;
  }

  template <class E, size_t M, class V>
  types::ndarray<typename E::dtype, types::array<long, E::value>>
  concatenate(types::array_base<E, M, V> const &args, long axis)
  {
    using T = typename E::dtype;
    auto constexpr N = E::value;
    auto shape = sutils::array(std::get<0>(args).shape());
    shape[axis] = details::concatenate_axis_size(
        args, axis, utils::make_index_sequence<M>{});
    types::ndarray<typename E::dtype, types::array<long, E::value>> out(
        shape, types::none_type{});
    details::concatenate_helper<N>()(out, args, axis,
                                     utils::make_index_sequence<M>{});
    return out;
  }

  template <class E>
  types::ndarray<typename E::dtype, types::array<long, E::value>>
  concatenate(types::list<E> const &ai, long axis)
  {
    using return_type =
        types::ndarray<typename E::dtype, types::array<long, E::value>>;
    using T = typename return_type::dtype;
    auto constexpr N = return_type::value;
    auto shape = sutils::array(ai[0].shape());
    shape[axis] = std::accumulate(
        ai.begin(), ai.end(), 0L, [axis](long v, E const &from) {
          return v + sutils::array(from.shape())[axis];
        });

    return_type out{shape, types::none_type{}};
    details::concatenate_helper<N>()(out, ai, axis);
    return out;
    ;
  }
}
PYTHONIC_NS_END

#endif
