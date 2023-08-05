#include <torch/extension.h>
#include <cstdint>    // int64_t
#include <memory>     // std::unique_ptr
#include <stdexcept>  // std::invalid_argument
#include <tuple>      // std::tie, std::tuple
#include <vector>     // std::vector

#include "free_lie_algebra_ops.hpp"
#include "logsignature.hpp"
#include "misc.hpp"
#include "pycapsule.hpp"
#include "signature.hpp"
#include "tensor_algebra_ops.hpp"


namespace signatory {
    namespace detail {
        struct LyndonInfo {
            LyndonInfo(std::unique_ptr<fla_ops::LyndonWords> lyndon_words,
                       std::vector<std::tuple<int64_t, int64_t, int64_t>>&& transforms,
                       std::vector<std::tuple<int64_t, int64_t, int64_t>>&& transforms_backward) :
                lyndon_words{std::move(lyndon_words)},
                transforms{transforms},
                transforms_backward{transforms_backward}
            {};

            std::unique_ptr<fla_ops::LyndonWords> lyndon_words;
            std::vector<std::tuple<int64_t, int64_t, int64_t>> transforms;
            std::vector<std::tuple<int64_t, int64_t, int64_t>> transforms_backward;

            constexpr static auto capsule_name = "signatory.LyndonInfoCapsule";
        };
    }  // namespace signatory::detail

    py::object make_lyndon_info(int64_t channels, s_size_type depth, LogSignatureMode mode) {
        misc::checkargs_channels_depth(channels, depth);
        std::unique_ptr<fla_ops::LyndonWords> lyndon_words;
        std::vector<std::tuple<int64_t, int64_t, int64_t>> transforms;
        std::vector<std::tuple<int64_t, int64_t, int64_t>> transforms_backward;
        misc::LyndonSpec lyndonspec{channels, depth};

        // no make_unique in C++11
        if (mode == LogSignatureMode::Words) {
            lyndon_words.reset(new fla_ops::LyndonWords(lyndonspec, fla_ops::LyndonWords::word_tag));
        }
        else if (mode == LogSignatureMode::Brackets) {
            lyndon_words.reset(new fla_ops::LyndonWords(lyndonspec, fla_ops::LyndonWords::bracket_tag));
            lyndon_words->to_lyndon_basis(transforms, transforms_backward);
            lyndon_words->delete_extra();
        }

        return misc::wrap_capsule<detail::LyndonInfo>(std::move(lyndon_words), std::move(transforms),
                                                      std::move(transforms_backward));
    }

    std::tuple<torch::Tensor, py::object>
    logsignature_forward(torch::Tensor path, s_size_type depth, bool stream, bool basepoint,
                         torch::Tensor basepoint_value, LogSignatureMode mode, py::object lyndon_info_capsule)
    {
        if (depth == 1) {
            return signature_forward(path, depth, stream, basepoint, basepoint_value);
        }  // this isn't just a fast return path: we also can't index the reciprocals tensor if depth == 1, so we'd need
        // faffier code below - and it's already quite faffy enough

        // first call the regular signature
        torch::Tensor signature;
        py::object backwards_info_capsule;
        std::tie(signature, backwards_info_capsule) = signature_forward(path, depth, stream, basepoint,
                                                                        basepoint_value);

        // unpack sigspec
        misc::BackwardsInfo* backwards_info = misc::unwrap_capsule<misc::BackwardsInfo>(backwards_info_capsule);
        const misc::SigSpec& sigspec = backwards_info->sigspec;

        // undo the transposing we just did in signature_forward...
        signature = misc::transpose_reverse(signature, sigspec);

        // organise the memory into a vector
        std::vector<torch::Tensor> signature_vector;
        misc::slice_by_term(signature, signature_vector, sigspec.output_channel_dim, sigspec);

        // and allocate memory for the logsignature
        // TODO: only invert the lowest terms? The higher terms aren't used?
        torch::Tensor logsignature = signature * ta_ops::log_coefficient_at_depth(depth - 2, sigspec);
        std::vector<torch::Tensor> logsignature_vector;
        misc::slice_by_term(logsignature, logsignature_vector, sigspec.output_channel_dim, sigspec);

        if (stream) {
            // allocate vectors for the signature and logsignature by stream index
            std::vector<torch::Tensor> signature_stream_vector;
            std::vector<torch::Tensor> logsignature_stream_vector;
            for (int64_t stream_index = 0; stream_index < sigspec.output_stream_size; ++stream_index) {
                misc::slice_at_stream(signature_vector, signature_stream_vector, stream_index);
                misc::slice_at_stream(logsignature_vector, logsignature_stream_vector, stream_index);
                ta_ops::compute_log(logsignature_stream_vector, signature_stream_vector, sigspec);
            }
        }
        else {
            ta_ops::compute_log(logsignature_vector, signature_vector, sigspec);
        }

        // Brackets and Words are the two possible compressed forms of the logsignature. So here we perform the
        // compression.
        if (lyndon_info_capsule.is_none()) {
            lyndon_info_capsule = make_lyndon_info(sigspec.input_channels, sigspec.depth, mode);
        }
        detail::LyndonInfo* lyndon_info = misc::unwrap_capsule<detail::LyndonInfo>(lyndon_info_capsule);
        if (mode == LogSignatureMode::Words) {
            logsignature = fla_ops::compress(*lyndon_info->lyndon_words, logsignature, sigspec);
        }
        else if (mode == LogSignatureMode::Brackets){
            logsignature = fla_ops::compress(*lyndon_info->lyndon_words, logsignature, sigspec);
            // Then apply the transforms. We rely on the triangularity property of the Lyndon basis for this to work.
            for (const auto& transform : lyndon_info->transforms) {
                int64_t source_index = std::get<0>(transform);
                int64_t target_index = std::get<1>(transform);
                int64_t coefficient = std::get<2>(transform);
                torch::Tensor source = logsignature.narrow(/*dim=*/sigspec.output_channel_dim,
                        /*start=*/source_index,
                        /*length=*/1);
                torch::Tensor target = logsignature.narrow(/*dim=*/sigspec.output_channel_dim,
                        /*start=*/target_index,
                        /*length=*/1);
                target.sub_(source, coefficient);
            }
        }

        backwards_info->set_logsignature_data(std::move(signature_vector),
                                              // Important: the capsule, not the lyndon_info itself! Then the resource
                                              // (i.e. the lyndon_info) is managed Python-style, so it doesn't matter
                                              // whether this is a capsule that was given to us, or that we generated
                                              // ourselves.
                                              lyndon_info_capsule,
                                              mode,
                                              logsignature.size(sigspec.output_channel_dim));

        logsignature = misc::transpose(logsignature, sigspec);
        return {logsignature, backwards_info_capsule};
    }

    std::tuple<torch::Tensor, torch::Tensor>
    logsignature_backward(torch::Tensor grad_logsignature, py::object backwards_info_capsule) {
        // Unpack sigspec
        misc::BackwardsInfo* backwards_info = misc::unwrap_capsule<misc::BackwardsInfo>(backwards_info_capsule);
        const misc::SigSpec& sigspec = backwards_info->sigspec;
        if (sigspec.depth == 1) {
            return signature_backward(grad_logsignature, backwards_info_capsule);
        }

        // Unpack everything else from backwards_info
        torch::Tensor signature = backwards_info->out;
        const std::vector<torch::Tensor>& signature_vector = backwards_info->signature_vector;
        LogSignatureMode mode = backwards_info->mode;
        int64_t logsignature_channels = backwards_info->logsignature_channels;
        detail::LyndonInfo* lyndon_info = misc::unwrap_capsule<detail::LyndonInfo>(backwards_info->lyndon_info_capsule);
        const std::vector<std::tuple<int64_t, int64_t, int64_t>>& transforms_backward = lyndon_info->transforms_backward;

        misc::checkargs_backward(grad_logsignature, sigspec, logsignature_channels);

        grad_logsignature = misc::transpose_reverse(grad_logsignature, sigspec);
        if (!grad_logsignature.is_floating_point()) {
            grad_logsignature = grad_logsignature.to(torch::kFloat32);
        }

        // Decompress the logsignature
        if (mode == LogSignatureMode::Expand) {
            grad_logsignature = grad_logsignature.clone();  // Clone so we don't leak changes through grad_logsignature.
        }
        else if (mode == LogSignatureMode::Words){
            grad_logsignature = fla_ops::compress_backward(grad_logsignature, *lyndon_info->lyndon_words, sigspec);
        }
        else {  // mode == LogSignatureMode::Brackets
            grad_logsignature = fla_ops::compress_backward(grad_logsignature, *lyndon_info->lyndon_words, sigspec);

            /* This is a deliberate asymmetry between the forwards and backwards: in the forwards pass we applied the
             * linear transformation after compression, but on the backwards we don't apply the transforms before
             * decompressing. Instead we apply a different (equivalent) transformation after decompressing. This is
             * because otherwise we would have to clone the grad_logsignature we were given, to be sure that the
             * transformations (which necessarily operate in-place) don't leak out. By doing it this way the memory that
             * we operate on is internal memory that we've claimed, not memory that we've been given in an input.
             */
            for (auto tptr = transforms_backward.rbegin(); tptr != transforms_backward.rend(); ++tptr) {
                int64_t source_index = std::get<0>(*tptr);
                int64_t target_index = std::get<1>(*tptr);
                int64_t coefficient = std::get<2>(*tptr);
                torch::Tensor grad_source = grad_logsignature.narrow(/*dim=*/sigspec.output_channel_dim,
                                                                     /*start=*/source_index,
                                                                     /*length=*/1);
                torch::Tensor grad_target = grad_logsignature.narrow(/*dim=*/sigspec.output_channel_dim,
                                                                     /*start=*/target_index,
                                                                     /*length=*/1);
                grad_source.sub_(grad_target, coefficient);
            }
        }

        torch::Tensor grad_signature = torch::zeros_like(grad_logsignature);
        torch::Tensor scratch = torch::empty({sigspec.output_channels, sigspec.batch_size}, sigspec.opts);
        std::vector<torch::Tensor> grad_logsignature_vector;
        std::vector<torch::Tensor> grad_signature_vector;
        std::vector<torch::Tensor> scratch_vector;
        misc::slice_by_term(grad_logsignature, grad_logsignature_vector, sigspec.output_channel_dim, sigspec);
        misc::slice_by_term(grad_signature, grad_signature_vector, sigspec.output_channel_dim, sigspec);
        misc::slice_by_term(scratch, scratch_vector, sigspec.output_channel_dim, sigspec);

        if (sigspec.stream) {
            // allocate vectors for the signature and logsignature by stream index
            std::vector<torch::Tensor> grad_logsignature_stream_vector;
            std::vector<torch::Tensor> grad_signature_stream_vector;
            std::vector<torch::Tensor> signature_stream_vector;
            for (int64_t stream_index = 0; stream_index < sigspec.output_stream_size; ++stream_index) {
                misc::slice_at_stream(grad_logsignature_vector, grad_logsignature_stream_vector, stream_index);
                misc::slice_at_stream(grad_signature_vector, grad_signature_stream_vector, stream_index);
                misc::slice_at_stream(signature_vector, signature_stream_vector, stream_index);
                torch::Tensor signature_at_stream = signature.narrow(/*dim=*/0,
                                                                     /*start=*/stream_index,
                                                                     /*len=*/1).squeeze(0);

                ta_ops::compute_log_backward(grad_logsignature_stream_vector, grad_signature_stream_vector,
                                             scratch_vector, signature_stream_vector, scratch,
                                             signature_at_stream, sigspec);
            }
        }
        else {
            ta_ops::compute_log_backward(grad_logsignature_vector, grad_signature_vector, scratch_vector,
                                         signature_vector, scratch, signature, sigspec);
        }

        grad_signature.add_(grad_logsignature, ta_ops::log_coefficient_at_depth(sigspec.depth - 2, sigspec));

        grad_signature = misc::transpose(grad_signature, sigspec);
        return signature_backward(grad_signature, backwards_info_capsule, false);
    }
}  // namespace signatory