#include <torch/extension.h>
#include <algorithm>  // std::binary_search, std::lower_bound, std::upper_bound
#include <cstdint>    // int64_t
#include <memory>     // std::unique_ptr
#include <set>        // std::multiset
#include <tuple>      // std::tuple
#include <vector>     // std::vector

#include "free_lie_algebra_ops.hpp"
#include "misc.hpp"


namespace signatory { namespace fla_ops {
    namespace detail {
        template<typename T>
        std::vector<T> concat_vectors(const std::vector<T>& vector1, const std::vector<T>& vector2) {
            std::vector<T> concat;
            concat.reserve(vector1.size() + vector2.size());
            concat.insert(concat.end(), vector1.begin(), vector1.end());
            concat.insert(concat.end(), vector2.begin(), vector2.end());
            return concat;
        }

        // Caution! Only suitable for use on LyndonWords which have their extra information set.
        // (Which is why it's not set as operator< on LyndonWord itself.)
        // We could check whether it's been set in this function (extra==nullptr), but we don't, just like [] vs at.
        struct CompareWords {
            bool operator()(const LyndonWord& w1, const LyndonWord& w2) {
                return w1.extra->word < w2.extra->word;
            }
            bool operator()(const LyndonWord* w1, const std::vector<int64_t> w2) {
                return w1->extra->word < w2;
            }
            bool operator()(const std::vector<int64_t> w1, const LyndonWord* w2) {
                return w1 < w2->extra->word;
            }
            bool operator()(const LyndonWord* w1, const LyndonWord* w2) {
                return w1->extra->word < w2->extra->word;
            }
        };
        constexpr CompareWords compare_words {};
    }  // namespace signatory::fla_ops::detail

    LyndonWords::LyndonWords(const misc::LyndonSpec& lyndonspec, WordTag) : lyndonspec{lyndonspec} {
        this->reserve(lyndonspec.depth);
        for (s_size_type depth_index = 0; depth_index < lyndonspec.depth; ++depth_index) {
            this->emplace_back();
        }

        std::vector<int64_t> word;
        word.reserve(lyndonspec.depth);
        word.push_back(-1);

        while (word.size()) {
            ++word.back();
            (*this)[word.size() - 1].emplace_back(word, false, lyndonspec);
            int64_t pos = 0;
            while (word.size() < static_cast<u_size_type>(lyndonspec.depth)) {
                word.push_back(word[pos]);
                ++pos;
            }
            while (word.size() && word.back() == lyndonspec.input_channels - 1) {
                word.pop_back();
            }
        }
        finalise();
    }

    LyndonWords::LyndonWords(const misc::LyndonSpec& lyndonspec, BracketTag) : lyndonspec{lyndonspec} {
        this->reserve(lyndonspec.depth);
        for (s_size_type depth_index = 0; depth_index < lyndonspec.depth; ++depth_index) {
            this->emplace_back();
        }

        (*this)[0].reserve(lyndonspec.input_channels);
        for (int64_t channel_index = 0; channel_index < lyndonspec.input_channels; ++channel_index) {
            (*this)[0].emplace_back(std::vector<int64_t> {channel_index}, true, lyndonspec);
        }

        for (s_size_type target_depth_index = 1; target_depth_index < lyndonspec.depth; ++target_depth_index) {
            auto& target_depth_class = (*this)[target_depth_index];

            auto& depth_class1 = (*this)[0];
            auto& depth_class2 = (*this)[target_depth_index - 1];
            for (auto& elem : depth_class1) {
                auto index_start = std::upper_bound(depth_class2.begin(), depth_class2.end(), elem,
                                                    detail::compare_words);
                for (auto elemptr = index_start; elemptr != depth_class2.end(); ++elemptr) {
                    target_depth_class.emplace_back(&elem, &*elemptr, lyndonspec);
                }
            }

            for (s_size_type depth_index1 = 1; depth_index1 < target_depth_index; ++depth_index1) {
                s_size_type depth_index2 = target_depth_index - depth_index1 - 1;
                auto& depth_class1 = (*this)[depth_index1];
                auto& depth_class2 = (*this)[depth_index2];

                for (auto& elem : depth_class1) {
                    auto index_start = std::upper_bound(depth_class2.begin(), depth_class2.end(), elem,
                                                        detail::compare_words);
                    auto index_end = std::upper_bound(index_start, depth_class2.end(), *elem.extra->second_child,
                                                      detail::compare_words);
                    for (auto elemptr = index_start; elemptr != index_end; ++elemptr) {
                        target_depth_class.emplace_back(&elem, &*elemptr, lyndonspec);
                    }
                }
            }
            std::sort(target_depth_class.begin(), target_depth_class.end(), detail::compare_words);
        }
        finalise();
    }

    void LyndonWords::to_lyndon_basis(std::vector<std::tuple<int64_t, int64_t, int64_t>>& transforms,
                                      std::vector<std::tuple<int64_t, int64_t, int64_t>>& transforms_backward) {

        std::map<std::multiset<int64_t>, std::vector<LyndonWord*>> lyndon_anagrams;
        //       \--------------------/  \----------------------/
        //    Letters in a Lyndon word    All Lyndon words of a particular anagram class, ordered lexicographically

        std::vector<s_size_type> anagram_class_sizes;
        anagram_class_sizes.reserve(amount);
        // First go through and figure out the anagram classes
        for (auto& depth_class : *this) {
            for (auto& lyndon_word : depth_class) {
                auto& word = lyndon_word.extra->word;
                auto& anagram_class = lyndon_anagrams[std::multiset<int64_t> (word.begin(), word.end())];

                anagram_class.push_back(&lyndon_word);
                lyndon_word.extra->anagram_class = &anagram_class;

                anagram_class_sizes.push_back(anagram_class.size());
            }
        }

        // Now go through and set where each Lyndon word appears in its anagram class. By a triangularity property
        // of Lyndon bases we can restrict our search space for anagrams.
        // Note that we couldn't do this in the above for loop because anagram_class was changing size (and thus
        // reallocating memory), so anagram_class.end() ends up becoming invalid.
        s_size_type counter = 0;
        for (auto& depth_class : *this) {
            for (auto& lyndon_word : depth_class) {
                lyndon_word.extra->anagram_limit = lyndon_word.extra->anagram_class->begin() +
                                                   anagram_class_sizes[counter];
                ++counter;
            }
        }

        // Make every length-one Lyndon word have itself as its own expansion (with coefficient 1)
        for (auto& lyndon_word : (*this)[0]) {
            lyndon_word.extra->expansion[lyndon_word.extra->word] = 1;
        }

        // Now unpack each bracket to find the coefficients we're interested in. This takes quite a lot of work.

        // Start at 1 because depth_index == 0 corresponds to the "bracketed words without brackets", at the very
        // lowest level - so we can't decompose them into two pieces yet.
        for (s_size_type depth_index = 1; depth_index < lyndonspec.depth; ++depth_index){
            for (const auto& lyndon_word : (*this)[depth_index]) {
                // Record the coefficients of each word in the expansion
                std::map<std::vector<int64_t>, int64_t> bracket_expansion;

                const auto& first_bracket_expansion = lyndon_word.extra->first_child->extra->expansion;
                const auto& second_bracket_expansion = lyndon_word.extra->second_child->extra->expansion;

                // Iterate over every word in the expansion of the first element of the bracket
                for (const auto& first_word_coeff : first_bracket_expansion) {
                    const std::vector<int64_t>& first_word = first_word_coeff.first;
                    int64_t first_coeff = first_word_coeff.second;

                    // And over every word in the expansion of the second element of the bracket
                    for (const auto& second_word_coeff : second_bracket_expansion) {
                        const std::vector<int64_t>& second_word = second_word_coeff.first;
                        int64_t second_coeff = second_word_coeff.second;

                        // And put them together to get every word in the expansion of the bracket
                        std::vector<int64_t> first_then_second = detail::concat_vectors(first_word, second_word);
                        std::vector<int64_t> second_then_first = detail::concat_vectors(second_word, first_word);


                        int64_t product = first_coeff * second_coeff;

                        // If depth_index == lyndonspec.depth - 1 (i.e. it is the final depth) then we only need to
                        // record the coefficients of Lyndon words. At lower depths we need to record the
                        // coefficients of non-Lyndon words in case some concatenation on to them becomes a Lyndon
                        // word at higher depths.
                        if (depth_index < lyndonspec.depth - 1 ||
                            lyndon_word.is_lyndon_anagram(first_then_second)) {
                            bracket_expansion[first_then_second] += product;
                        }
                        if (depth_index < lyndonspec.depth - 1 ||
                            lyndon_word.is_lyndon_anagram(second_then_first)) {
                            bracket_expansion[second_then_first] -= product;
                        }
                    }
                }

                // Record the transformations we're interested in
                auto end = lyndon_word.extra->anagram_class->end();
                for (const auto& word_coeff : bracket_expansion) {
                    const std::vector<int64_t>& word = word_coeff.first;
                    int64_t coeff = word_coeff.second;

                    // Filter out non-Lyndon words. (If depth_index == lyndonspec.depth - 1 then we've essentially
                    // already done this above so the if statement should always be true, so we check that
                    // preferentially as it's probably faster to check. Probably - I know I know I should time it
                    // but it's not that big a deal either way...)
                    auto ptr_to_word = std::lower_bound(lyndon_word.extra->anagram_limit, end, word,
                                                        detail::compare_words);
                    if (ptr_to_word != end) {
                        if (depth_index == lyndonspec.depth - 1 || (*ptr_to_word)->extra->word == word) {
                            transforms.emplace_back(lyndon_word.compressed_index,
                                                    (*ptr_to_word)->compressed_index,
                                                    coeff);
                            transforms_backward.emplace_back(lyndon_word.tensor_algebra_index,
                                                             (*ptr_to_word)->tensor_algebra_index,
                                                             coeff);
                        }
                    }
                }

                // If depth_index == lyndonspec.depth - 1 then we don't need to record what we've found
                if (depth_index < lyndonspec.depth - 1) {
                    lyndon_word.extra->expansion = std::move(bracket_expansion);
                }
            }
        }

        // Delete everything we don't need any more.
        for (auto& depth_class : *this) {
            for (auto& lyndon_word : depth_class) {
                lyndon_word.extra = nullptr;
            }
        }
    }

    void LyndonWords::delete_extra() {
        for (auto& depth_class : (*this)) {
            for (auto& lyndon_word : depth_class) {
                lyndon_word.extra.reset();
            }
        }
    }

    void LyndonWords::finalise() {
        // Used to set indices for a collection of Lyndon words. In some sense this behaviour really belongs in the
        // constructors of each individual LyndonWord (as without this function call they aren't really completely
        // initialised) but it's a boatload more efficient to do this after all the Lyndon words are generated, rather
        // than applying this to them one-by-one.
        int64_t tensor_algebra_offset = 0;
        int64_t num_words = lyndonspec.input_channels;
        s_size_type compressed_offset = 0;
        for (auto& depth_class : (*this)) {
            for (s_size_type compressed_index = 0;
                 static_cast<u_size_type>(compressed_index) < depth_class.size();
                 ++compressed_index) {
                auto& lyndon_word = depth_class[compressed_index];
                lyndon_word.tensor_algebra_index += tensor_algebra_offset;
                lyndon_word.compressed_index = compressed_offset + compressed_index;
            }
            tensor_algebra_offset += num_words;
            num_words *= lyndonspec.input_channels;
            compressed_offset += depth_class.size();
        }

        // Figure out the total amount of Lyndon words
        if (lyndonspec.input_channels == 1) {
            // In this case there only exists a singe Lyndon word '0', at (*this)[0].back(). There are now
            // higher-depth words, i.e. (*this)[1], (*this)[2], ... etc. are all size-0 vectors.
            amount = 1;
        }
        else {
            amount = this->back().back().compressed_index + 1;
        }
    }

    LyndonWord::ExtraLyndonInformation::ExtraLyndonInformation(const std::vector<int64_t>& word_,
                                                               LyndonWord* first_child_,
                                                               LyndonWord* second_child_) :
            word{word_},
            first_child{first_child_},
            second_child{second_child_}
    {};

    // Constructor for LyndonWords(..., LyndonWords::word_tag) (with extra==false) and
    // constructor for LyndonWords(..., LyndonWords::bracket_tag) for the depth == 1 words (with extra==true).
    LyndonWord::LyndonWord(const std::vector<int64_t>& word, bool extra, const misc::LyndonSpec& lyndonspec)
    {
        init(word, extra, nullptr, nullptr, lyndonspec);
    };

    // Constructor for LyndonWords(..., LyndonWords::bracket_tag) for the depth > 1 words.
    LyndonWord::LyndonWord(LyndonWord* first_child, LyndonWord* second_child, const misc::LyndonSpec& lyndonspec)
    {
        std::vector<int64_t> word = detail::concat_vectors(first_child->extra->word, second_child->extra->word);
        init(word, true, first_child, second_child, lyndonspec);
    };

    // Checks if the given 'word' is:
    // (a) later in the lexicographic order than 'this'
    // (b) also a Lyndon word itself
    // (c) an anagram of 'this'
    bool LyndonWord::is_lyndon_anagram (const std::vector<int64_t>& word) const {
        return std::binary_search(this->extra->anagram_limit,  this->extra->anagram_class->end(), word,
                                  detail::compare_words);
    }

    void LyndonWord::init(const std::vector<int64_t>& word, bool extra_, LyndonWord* first_child,
                          LyndonWord* second_child, const misc::LyndonSpec& lyndonspec) {

        int64_t current_stride = 1;
        for (auto word_index = word.rbegin(); word_index != word.rend(); ++word_index) {
            tensor_algebra_index += *word_index * current_stride;
            current_stride *= lyndonspec.input_channels;
        }
        // We still need to add on to tensor_algebra_index the offset corresponding to number of all smaller
        // words.
        // We also need to set compressed_index, but we don't know that until we've generated all Lyndon words.
        // Thus both of these are handled by the set_indices function, called after all Lyndon words have been
        // generated.

        if (extra_) {
            // no make_unique in C++11
            extra.reset(new LyndonWord::ExtraLyndonInformation(word, first_child, second_child));
        }
    }

    torch::Tensor compress(const LyndonWords& lyndon_words, torch::Tensor input, const misc::SigSpec& sigspec) {
        torch::Tensor compressed;
        if (sigspec.stream) {
            compressed = torch::empty({sigspec.output_stream_size,
                                       lyndon_words.amount,
                                       sigspec.batch_size},
                                      sigspec.opts);
        }
        else {
            compressed = torch::empty({lyndon_words.amount,
                                       sigspec.batch_size},
                                      sigspec.opts);
        }

        // Extract terms corresponding to Lyndon words
        // This does mean that we just did a whole bunch of computation that isn't actually used in the output. We
        // don't really have good ways to compute logsignatures. Even the Baker-Campbell-Hausdoff formula is
        // expensive, and not obviously better than what we do.
        // It also means that we're holding on to a lot of memory until the backward pass.
        for (s_size_type depth_index = 0; depth_index < sigspec.depth; ++depth_index){
            for (auto& lyndon_word : lyndon_words[depth_index]) {
                compressed.narrow(/*dim=*/sigspec.output_channel_dim,
                                  /*start=*/lyndon_word.compressed_index,
                                  /*length=*/1).copy_(input.narrow(/*dim=*/sigspec.output_channel_dim,
                                                                   /*start=*/lyndon_word.tensor_algebra_index,
                                                                   /*length=*/1)
                                                      );
            }
        }
        return compressed;
    }

    torch::Tensor compress_backward(torch::Tensor grad_compressed, const LyndonWords& lyndon_words,
                                    const misc::SigSpec& sigspec) {
        torch::Tensor grad_expanded;
        if (sigspec.stream) {
            grad_expanded = torch::zeros({sigspec.output_stream_size,
                                         sigspec.output_channels,
                                         sigspec.batch_size},
                                        sigspec.opts);
        }
        else {
            grad_expanded = torch::zeros({sigspec.output_channels,
                                         sigspec.batch_size},
                                        sigspec.opts);
        }

        for (s_size_type depth_index = 0; depth_index < sigspec.depth; ++depth_index){
            for (auto& lyndon_word: lyndon_words[depth_index]) {
                grad_expanded.narrow(/*dim=*/sigspec.output_channel_dim,
                                     /*start=*/lyndon_word.tensor_algebra_index,
                                     /*length=*/1).copy_(
                                           grad_compressed.narrow(/*dim=*/sigspec.output_channel_dim,
                                                                  /*start=*/lyndon_word.compressed_index,
                                                                  /*length=*/1)
                                                         );
            }
        }
        return grad_expanded;
    }
}  /* namespace signatory::fla_ops */ }  // namespace signatory
