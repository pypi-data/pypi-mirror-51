#ifndef SIGNATORY_BACKWARDS_INFO_HPP
#define SIGNATORY_BACKWARDS_INFO_HPP

#include <torch/extension.h>
#include <cstdint>      // int64_t
#include <tuple>        // std::tuple
#include <vector>       // std::vector

#include "free_lie_algebra_ops.hpp"


namespace signatory { namespace misc {
    // Retains information needed for the backwards pass.
    struct BackwardsInfo{
        BackwardsInfo(SigSpec&& sigspec, std::vector<torch::Tensor>&& out_vector, torch::Tensor out,
                      torch::Tensor path_increments);

        void set_logsignature_data(std::vector<torch::Tensor>&& signature_vector_,
                                   std::vector<std::tuple<int64_t, int64_t, int64_t>>&& transforms_,
                                   LogSignatureMode mode_,
                                   int64_t logsignature_channels_);

        SigSpec sigspec;
        std::vector<torch::Tensor> out_vector;
        torch::Tensor out;
        torch::Tensor path_increments;

        std::vector<torch::Tensor> signature_vector;  // will be the same as out_vector when computing logsignatures
        // with stream==true. But we provide a separate vector here
        // for a consistent interface with the stream==false case as
        // well.
        std::vector<std::tuple<int64_t, int64_t, int64_t>> transforms;
        LogSignatureMode mode;
        int64_t logsignature_channels;
    };

    // Makes a BackwardsInfo object and wraps it into a PyCapsule and wraps that into a py::object
    py::object make_backwards_info(std::vector<torch::Tensor>& out_vector, torch::Tensor out,
                                   torch::Tensor path_increments, SigSpec& sigspec);

    // Unwraps a py::object to unwrap a PyCapsule to get a BackwardsInfo object
    BackwardsInfo* get_backwards_info(py::object backwards_info_capsule);
}  /* namespace signatory::misc */ }  // namespace signatory

#endif //SIGNATORY_BACKWARDS_INFO_HPP
