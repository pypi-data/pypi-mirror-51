/* Copyright 2019 Patrick Kidger. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *    http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ========================================================================= */
 

#include <torch/extension.h>
#include <cstdint>    // int64_t
#include <memory>     // std::unique_ptr
#include <stdexcept>  // std::invalid_argument
#include <tuple>      // std::tie, std::tuple
#include <utility>     // std::pair
#include <vector>     // std::vector

#include "free_lie_algebra_ops.hpp"
#include "logsignature.hpp"
#include "misc.hpp"
#include "pycapsule.hpp"
#include "signature.hpp"
#include "tensor_algebra_ops.hpp"


namespace signatory {
    namespace detail {
        // This struct will be wrapped into a PyCapsule. Using it allows for computing certain aspects of the 
        // logsignature transformation just once, so that repeated use of the logsignature transformation is more
        // efficient.
        struct LyndonInfo {
            LyndonInfo(std::unique_ptr<fla_ops::LyndonWords> lyndon_words,
                       std::vector<std::vector<std::tuple<int64_t, int64_t, int64_t>>>&& transforms,
                       std::vector<std::vector<std::tuple<int64_t, int64_t, int64_t>>>&& transforms_backward) :
                lyndon_words{std::move(lyndon_words)},
                transforms{transforms},
                transforms_backward{transforms_backward}
            {};

            // A list of Lyndon words
            std::unique_ptr<fla_ops::LyndonWords> lyndon_words;
            
            // The transforms for going from Lyndon words to Lyndon basis
            // This is in terms of the 'compressed' index, i.e. in the free Lie algebra
            // They are grouped (the outermost vector) by anagram class
            std::vector<std::vector<std::tuple<int64_t, int64_t, int64_t>>> transforms;
            
            // The transforms for going from Lyndon basis to Lyndon words
            // This is in terms of the tensor algebra index
            // They are grouped (the outermost vector) by anagram class
            std::vector<std::vector<std::tuple<int64_t, int64_t, int64_t>>> transforms_backward;

            constexpr static auto capsule_name = "signatory.LyndonInfoCapsule";
        };
    }  // namespace signatory::detail

    py::object make_lyndon_info(int64_t channels, s_size_type depth, LogSignatureMode mode) {
        misc::checkargs_channels_depth(channels, depth);
        std::unique_ptr<fla_ops::LyndonWords> lyndon_words;
        std::vector<std::vector<std::tuple<int64_t, int64_t, int64_t>>> transforms;
        std::vector<std::vector<std::tuple<int64_t, int64_t, int64_t>>> transforms_backward;
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

        // No sense keeping track of gradients when we have a dedicated backwards function (and in-place operations mean
        // that in any case one cannot autograd through this function)
        path = path.detach();
        basepoint_value = basepoint_value.detach();

        // first call the regular signature
        torch::Tensor signature;
        py::object backwards_info_capsule;
        std::tie(signature, backwards_info_capsule) = signature_forward(path, depth, stream, basepoint,
                                                                        basepoint_value);

        // unpack sigspec
        misc::BackwardsInfo* backwards_info = misc::unwrap_capsule<misc::BackwardsInfo>(backwards_info_capsule);
        const misc::SigSpec& sigspec = backwards_info->sigspec;

        // TODO: uncomment when 24413 is fixed
        // We have to do the transpose in the Python side to avoid a PyTorch bug.
        // https://github.com/pytorch/pytorch/issues/24413
        // (In particular this means we don't have a transpose to undo here.)
        // // undo the transposing we just did in signature_forward...
        // signature = misc::transpose_reverse(signature, sigspec);

        // organise the memory into a vector
        std::vector<torch::Tensor> signature_vector;
        misc::slice_by_term(signature, signature_vector, sigspec);

        // and allocate memory for the logsignature
        torch::Tensor logsignature = torch::empty_like(signature);
        std::vector<torch::Tensor> logsignature_vector;
        misc::slice_by_term(logsignature, logsignature_vector, sigspec);

        if (stream) {
            std::vector<torch::Tensor> signature_stream_vector;
            std::vector<torch::Tensor> logsignature_stream_vector;
            for (int64_t stream_index = 0;
                 stream_index < sigspec.output_stream_size;
                 ++stream_index) {
                misc::slice_at_stream(signature_vector, signature_stream_vector,
                                      stream_index);
                misc::slice_at_stream(logsignature_vector, logsignature_stream_vector,
                                      stream_index);
                ta_ops::compute_log(logsignature_stream_vector, signature_stream_vector,
                                    sigspec);
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
            bool cuda = logsignature.is_cuda();
            if (cuda) {
                logsignature = logsignature.cpu();
            }
            // This is essentially solving a sparse linear system... and it's horrendously slow on a GPU.
            for (const auto& transform_class : lyndon_info->transforms) {
                for (const auto& transform : transform_class) {
                    int64_t source_index = std::get<0>(transform);
                    int64_t target_index = std::get<1>(transform);
                    int64_t coefficient = std::get<2>(transform);
                    torch::Tensor source = logsignature.narrow(/*dim=*/channel_dim,
                                                               /*start=*/source_index,
                                                               /*length=*/1);
                    torch::Tensor target = logsignature.narrow(/*dim=*/channel_dim,
                                                               /*start=*/target_index,
                                                               /*length=*/1);
                    target.sub_(source, coefficient);
                }
            }
            if (cuda) {
                logsignature = logsignature.cuda();
            }
        }

        backwards_info->set_logsignature_data(signature_vector,
                                              // Important: the capsule, not the lyndon_info itself! Then the resource
                                              // (i.e. the lyndon_info) is managed Python-style, so it doesn't matter
                                              // whether this is a capsule that was given to us, or that we generated
                                              // ourselves.
                                              lyndon_info_capsule,
                                              mode,
                                              logsignature.size(channel_dim));

        // TODO: uncomment when 24413 is fixed
        // We have to do the transpose in the Python side to avoid a PyTorch bug.
        // https://github.com/pytorch/pytorch/issues/24413
        // logsignature = misc::transpose(logsignature, sigspec);
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

        // TODO: Remove this line when PyTorch bug 24413 is fixed. Here we undo the transposing that has been
        //  automatically done via autograd outside
        grad_logsignature = misc::transpose_reverse(grad_logsignature, sigspec);

        // Unpack everything else from backwards_info
        torch::Tensor signature = backwards_info->out;
        const std::vector<torch::Tensor>& signature_vector = backwards_info->signature_vector;
        LogSignatureMode mode = backwards_info->mode;
        int64_t logsignature_channels = backwards_info->logsignature_channels;
        detail::LyndonInfo* lyndon_info = misc::unwrap_capsule<detail::LyndonInfo>(backwards_info->lyndon_info_capsule);

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
            bool cuda = grad_logsignature.is_cuda();
            if (cuda) {
                grad_logsignature = grad_logsignature.cpu();
            }
            // This is essentially solving a sparse linear system... and it's horrendously slow on a GPU.
            for (const auto& transform_class : lyndon_info->transforms_backward) {
                for (auto tptr = transform_class.rbegin();
                     tptr != transform_class.rend();
                     ++tptr)  {
                    int64_t source_index = std::get<0>(*tptr);
                    int64_t target_index = std::get<1>(*tptr);
                    int64_t coefficient = std::get<2>(*tptr);
                    torch::Tensor grad_source = grad_logsignature.narrow(/*dim=*/channel_dim,
                                                                         /*start=*/source_index,
                                                                         /*length=*/1);
                    torch::Tensor grad_target = grad_logsignature.narrow(/*dim=*/channel_dim,
                                                                         /*start=*/target_index,
                                                                         /*length=*/1);
                    grad_source.sub_(grad_target, coefficient);
                }
            }
            if (cuda) {
                grad_logsignature = grad_logsignature.to(sigspec.opts);
            }
        }

        torch::Tensor grad_signature = torch::zeros_like(grad_logsignature);
        std::vector<torch::Tensor> grad_logsignature_vector;
        std::vector<torch::Tensor> grad_signature_vector;
        misc::slice_by_term(grad_logsignature, grad_logsignature_vector, sigspec);
        misc::slice_by_term(grad_signature, grad_signature_vector, sigspec);

        if (sigspec.stream) {
            std::vector<torch::Tensor> grad_logsignature_stream_vector;
            std::vector<torch::Tensor> grad_signature_stream_vector;
            std::vector<torch::Tensor> signature_stream_vector;
            for (int64_t stream_index = 0;
                 stream_index < sigspec.output_stream_size;
                 ++stream_index) {
                misc::slice_at_stream(grad_logsignature_vector,
                                      grad_logsignature_stream_vector,
                                      stream_index);
                misc::slice_at_stream(grad_signature_vector,
                                      grad_signature_stream_vector,
                                      stream_index);
                misc::slice_at_stream(signature_vector,
                                      signature_stream_vector,
                                      stream_index);

                ta_ops::compute_log_backward(grad_logsignature_stream_vector,
                                             grad_signature_stream_vector,
                                             signature_stream_vector,
                                             sigspec);
            }
        }
        else {
            ta_ops::compute_log_backward(grad_logsignature_vector, grad_signature_vector, signature_vector, sigspec);
        }

        // TODO: uncomment this line once PyTorch bug 24413 is fixed
//        grad_signature = misc::transpose(grad_signature, sigspec);
        return signature_backward(grad_signature, backwards_info_capsule, false);
    }
}  // namespace signatory