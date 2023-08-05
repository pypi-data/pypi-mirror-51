import os
import random
import tempfile
from copy import copy
from functools import partial
from multiprocessing import cpu_count
import pickle

import numpy as np
import tensorflow as tf
from joblib import Parallel, delayed

from .tokenization import printable_text
from .utils import (BOS_TOKEN, EOS_TOKEN, add_special_tokens_with_seqs,
                    create_instances_from_document, create_mask_and_padding,
                    create_masked_lm_predictions, punc_augument,
                    tokenize_text_with_seqs, truncate_seq_pair)


def create_single_problem_single_instance(problem,
                                          ex_index,
                                          example,
                                          label_encoder,
                                          params,
                                          tokenizer,
                                          mode,
                                          problem_type,
                                          is_seq):

    raw_inputs, raw_target = example

    # punctuation augumentation
    if params.punc_replace_prob > 0 and mode == 'train':
        raw_inputs = punc_augument(raw_inputs, params)

    # tokenize inputs, now the length is fixed, target == raw_target
    if isinstance(raw_inputs, dict):
        tokens_a, target = tokenize_text_with_seqs(
            tokenizer, raw_inputs['a'], raw_target, is_seq)
        tokens_b, _ = tokenize_text_with_seqs(
            tokenizer, raw_inputs['b'], raw_target)
    else:
        tokens_a, target = tokenize_text_with_seqs(
            tokenizer, raw_inputs, raw_target, is_seq)
        tokens_b = None

    if tokens_b is not None and is_seq:
        raise NotImplementedError(
            'Sequence Labeling with tokens b is not implemented')

    if not tokens_a:
        return
    # check whether tokenization changed the length
    if is_seq:
        if len(target) != len(tokens_a):
            tf.logging.warning('Data %d broken' % ex_index)
            return

    # truncate tokens and target to max_seq_len
    tokens_a, tokens_b, target = truncate_seq_pair(
        tokens_a, tokens_b, target, params.max_seq_len, is_seq=is_seq)

    # add [SEP], [CLS] tokens
    tokens, segment_ids, target = add_special_tokens_with_seqs(
        tokens_a, tokens_b, target, is_seq)

    # train mask lm as augument task while training
    if params.augument_mask_lm and mode == 'train':
        rng = random.Random()
        (mask_lm_tokens, masked_lm_positions,
            masked_lm_labels) = create_masked_lm_predictions(
                tokens,
                params.masked_lm_prob,
                params.max_predictions_per_seq,
                list(tokenizer.vocab.keys()), rng)
        _, mask_lm_tokens, _, _ = create_mask_and_padding(
            mask_lm_tokens,
            copy(segment_ids),
            copy(target),
            params.max_seq_len,
            is_seq,
            dynamic_padding=params.dynamic_padding)
        masked_lm_weights, masked_lm_labels, masked_lm_positions, _ = create_mask_and_padding(
            masked_lm_labels, masked_lm_positions, None, params.max_predictions_per_seq)
        mask_lm_input_ids = tokenizer.convert_tokens_to_ids(
            mask_lm_tokens)
        masked_lm_ids = tokenizer.convert_tokens_to_ids(masked_lm_labels)

    input_mask, tokens, segment_ids, target = create_mask_and_padding(
        tokens, segment_ids, target, params.max_seq_len, is_seq, dynamic_padding=params.dynamic_padding)

    # create mask and padding for labels of seq2seq problem
    if problem_type in ['seq2seq_tag', 'seq2seq_text']:

        # tokenize text if target is text
        if problem_type == 'seq2seq_text':

            # assign num_classes for text generation problem
            params.num_classes[problem] = len(label_encoder.vocab)

            target, _ = tokenize_text_with_seqs(
                label_encoder, target, None, False)

        target, _, _ = truncate_seq_pair(
            target, None, None, params.decode_max_seq_len, is_seq=is_seq)
        # since we initialize the id to 0 in prediction, we need
        # to make sure that BOS_TOKEN is [PAD]
        target = [BOS_TOKEN] + target + [EOS_TOKEN]
        label_mask, target, _, _ = create_mask_and_padding(
            target, [0] * len(target), None, params.decode_max_seq_len)

    input_ids = tokenizer.convert_tokens_to_ids(tokens)

    if isinstance(target, list):
        if problem_type == 'seq2seq_text':
            label_id = label_encoder.convert_tokens_to_ids(target)
        elif problem_type == 'multi_cls':
            label_id = label_encoder.transform([target])[0]
        else:
            # seq2seq_tag
            label_id = label_encoder.transform(target).tolist()
            label_id = [np.int32(i) for i in label_id]
    else:
        label_id = label_encoder.transform([target]).tolist()[0]
        label_id = np.int32(label_id)

    if not params.dynamic_padding:
        assert len(input_ids) == params.max_seq_len
        assert len(input_mask) == params.max_seq_len
        assert len(segment_ids) == params.max_seq_len, segment_ids
        if is_seq:
            assert len(label_id) == params.max_seq_len

    # logging in debug mode
    if ex_index < 5:
        tf.logging.debug("*** Example ***")
        tf.logging.debug("tokens: %s" % " ".join(
            [printable_text(x) for x in tokens]))
        tf.logging.debug("input_ids: %s" %
                         " ".join([str(x) for x in input_ids]))
        tf.logging.debug("input_mask: %s" %
                         " ".join([str(x) for x in input_mask]))
        tf.logging.debug("segment_ids: %s" %
                         " ".join([str(x) for x in segment_ids]))
        if is_seq or problem_type in ['seq2seq_tag', 'seq2seq_text']:
            tf.logging.debug("%s_label_ids: %s" %
                             (problem, " ".join([str(x) for x in label_id])))
            tf.logging.debug("%s_label: %s" %
                             (problem, " ".join([str(x) for x in target])))
        else:
            tf.logging.debug("%s_label_ids: %s" %
                             (problem, str(label_id)))
            tf.logging.debug("%s_label: %s" %
                             (problem, str(target)))
        if params.augument_mask_lm and mode == 'train':
            tf.logging.debug("mask lm tokens: %s" % " ".join(
                [printable_text(x) for x in mask_lm_tokens]))
            tf.logging.debug("mask lm input_ids: %s" %
                             " ".join([str(x) for x in mask_lm_input_ids]))
            tf.logging.debug("mask lm label ids: %s" %
                             " ".join([str(x) for x in masked_lm_ids]))
            tf.logging.debug("mask lm position: %s" %
                             " ".join([str(x) for x in masked_lm_positions]))

    # create return dict
    if not params.augument_mask_lm:
        return_dict = {
            'input_ids': input_ids,
            'input_mask': input_mask,
            'segment_ids': segment_ids,
            '%s_label_ids' % problem: label_id
        }
    else:
        if mode == 'train' and random.uniform(0, 1) <= params.augument_rate:
            return_dict = {
                'input_ids': mask_lm_input_ids,
                'input_mask': input_mask,
                'segment_ids': segment_ids,
                '%s_label_ids' % problem: label_id,
                "masked_lm_positions": masked_lm_positions,
                "masked_lm_ids": masked_lm_ids,
                "masked_lm_weights": masked_lm_weights,
            }
        else:
            return_dict = {
                'input_ids': input_ids,
                'input_mask': input_mask,
                'segment_ids': segment_ids,
                '%s_label_ids' % problem: label_id,
                "masked_lm_positions": np.zeros([params.max_predictions_per_seq]),
                "masked_lm_ids": np.zeros([params.max_predictions_per_seq]),
                "masked_lm_weights": np.zeros([params.max_predictions_per_seq]),
            }

    if problem_type in ['seq2seq_tag', 'seq2seq_text']:
        return_dict['%s_mask' % problem] = label_mask

    return return_dict


def _multiprocessing_wrapper(
        problem,
        example_list,
        label_encoder,
        params,
        tokenizer,
        mode,
        problem_type,
        is_seq):
    return_list = []
    for ex_index, example in enumerate(example_list):
        return_list.append(create_single_problem_single_instance(
            problem,
            999,
            example,
            label_encoder,
            params,
            tokenizer,
            mode,
            problem_type,
            is_seq))
    return return_list


def create_single_problem_generator(problem,
                                    inputs_list,
                                    target_list,
                                    label_encoder,
                                    params,
                                    tokenizer,
                                    mode):
    """Function to create iterator for single problem

    This function will:
        1. Do some text cleaning using original bert tokenizer, if
            problem type is sequential tagging, corresponding labels
            will be removed.

            Example:
                Before: inputs: ['a', '&', 'c'] target: [0, 0, 1]
                After: inputs: ['a', 'c'] target: [0, 1]
        2. Add [CLS], [SEP] tokens
        3. Padding
        4. yield result dict

    Arguments:
        problem {str} -- problem name
        inputs_list {list } -- inputs list
        target_list {list} -- target list, should have the same length as inputs list
        label_encoder {LabelEncoder} -- label encoder
        params {Params} -- params
        tokenizer {tokenizer} -- Bert Tokenizer
        epoch {int} -- Deprecate
    """

    problem_type = params.problem_type[problem]

    # whether this problem is sequential labeling
    # for sequential labeling, targets needs to align with any
    # change of inputs
    is_seq = problem_type in ['seq_tag']
    if not params.multiprocess:
        for ex_index, example in enumerate(zip(inputs_list, target_list)):
            return_dict = create_single_problem_single_instance(problem,
                                                                ex_index,
                                                                example,
                                                                label_encoder,
                                                                params,
                                                                tokenizer,
                                                                mode,
                                                                problem_type,
                                                                is_seq)

            yield return_dict
    else:
        return_dict_list = []
        pickle_file = os.path.join(
            params.tmp_file_dir, '{0}_{1}_data.pkl'.format(problem, mode))

        if not os.path.exists(pickle_file):
            # params.tmp_file_dir = tempfile.mkdtemp(dir='.')
            os.makedirs('tmp', exist_ok=True)
            params.tmp_file_dir = 'tmp'
            pickle_file = os.path.join(
                params.tmp_file_dir, '{0}_{1}_data.pkl'.format(problem, mode))
            tf.logging.info(
                'Saving preprocessing files to {0}'.format(pickle_file))
            partial_fn = partial(_multiprocessing_wrapper, problem=problem, label_encoder=label_encoder,
                                 params=params, tokenizer=tokenizer,
                                 mode=mode, problem_type=problem_type, is_seq=is_seq)
            example_list = list(zip(inputs_list, target_list))
            num_process = cpu_count()

            def split(a, n):
                k, m = divmod(len(a), n)
                return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))
            example_list = list(split(example_list, num_process))

            return_dict_list_list = Parallel(num_process)(delayed(partial_fn)(
                example_list=example) for example in example_list
            )

            pickle.dump(return_dict_list_list, open(pickle_file, 'wb'))
        else:
            return_dict_list_list = pickle.load(open(pickle_file, 'rb'))

        for return_dict_list in return_dict_list_list:
            for return_dict in return_dict_list:
                yield return_dict


def create_pretraining_generator(problem,
                                 inputs_list,
                                 target_list,
                                 label_encoder,
                                 params,
                                 tokenizer
                                 ):
    """Slight modification of original code

    Raises:
        ValueError -- Input format not right
    """

    if not isinstance(inputs_list[0][0], list):
        raise ValueError('inputs is expected to be list of list of list.')

    all_documents = []
    for document in inputs_list:
        all_documents.append([])
        for sentence in document:
            all_documents[-1].append(tokenizer.tokenize('\t'.join(sentence)))

    all_documents = [d for d in all_documents if d]
    rng = random.Random()
    rng.shuffle(all_documents)

    vocab_words = list(tokenizer.vocab.keys())
    instances = []

    print_count = 0
    for _ in range(params.dupe_factor):
        for document_index in range(len(all_documents)):
            instances = create_instances_from_document(
                all_documents,
                document_index,
                params.max_seq_len,
                params.short_seq_prob,
                params.masked_lm_prob,
                params.max_predictions_per_seq,
                vocab_words, rng)
            for instance in instances:
                tokens = instance.tokens
                segment_ids = list(instance.segment_ids)

                input_mask, tokens, segment_ids, _ = create_mask_and_padding(
                    tokens, segment_ids, None, params.max_seq_len)
                masked_lm_positions = list(instance.masked_lm_positions)
                masked_lm_weights, masked_lm_labels, masked_lm_positions, _ = create_mask_and_padding(
                    instance.masked_lm_labels, masked_lm_positions, None, params.max_predictions_per_seq)
                input_ids = tokenizer.convert_tokens_to_ids(tokens)
                masked_lm_ids = tokenizer.convert_tokens_to_ids(
                    masked_lm_labels)
                next_sentence_label = 1 if instance.is_random_next else 0

                yield_dict = {
                    "input_ids": input_ids,
                    "input_mask": input_mask,
                    "segment_ids": segment_ids,
                    "masked_lm_positions": masked_lm_positions,
                    "masked_lm_ids": masked_lm_ids,
                    "masked_lm_weights": masked_lm_weights,
                    "next_sentence_label_ids": next_sentence_label
                }

                if print_count < 3:
                    tf.logging.debug('%s : %s' %
                                     ('tokens', ' '.join([str(x) for x in tokens])))
                    for k, v in yield_dict.items():
                        if not isinstance(v, int):
                            tf.logging.debug('%s : %s' %
                                             (k, ' '.join([str(x) for x in v])))
                    print_count += 1

                yield yield_dict


def create_generator(params, mode):
    """Function to create iterator for multiple problem

    This function dose the following things:
    1. Create dummy labels for each problems.
    2. Initialize all generators
    3. Sample a problem to train at this batch. If eval, take turns
    4. Create a loss multiplier
    5. Tried to generate samples for target problem, if failed, init gen
    6. Add dummy label to other problems

    Example:
        Problem: cws|NER|weibo_ner&weibo_cws
        1. Dummy labels: cws_label_ids: [0,0,0] ...
        2. Blablabla
        3. Sample, say (weibo_ner&weibo_cws)
        4. loss multipliers: {'cws_loss_multiplier': 0, ..., 'weibo_ner_loss_multiplier': 1, ...}
        ...

    Arguments:
        params {Params} -- params
        mode {mode} -- mode
    """
    # example
    # problem_list: ['NER', 'cws', 'weibo_ner', 'weibo_cws']
    # problem_chunk: [['NER'], ['cws'], ['weibo_ner', 'weibo_cws']]
    problem_list = []
    problem_chunk = []
    for problem_dict in params.run_problem_list:
        problem_list += list(problem_dict.keys())
        problem_chunk.append(list(problem_dict.keys()))

    # get dummy labels
    def _create_dummpy_label(problem_type, num_classes=None):
        if problem_type == 'cls':
            return 0
        elif problem_type == 'seq_tag':
            return [0]*params.max_seq_len
        elif problem_type == 'mask_lm':
            return [0]*params.max_predictions_per_seq
        elif problem_type == 'multi_cls':
            return [0]*num_classes
        else:
            return [0]*params.decode_max_seq_len
    dummy_label_dict = {problem+'_label_ids': _create_dummpy_label(
        params.problem_type[problem], params.num_classes[problem]) for problem in problem_list if params.problem_type[problem] != 'pretrain'}
    dummy_label_dict.update({problem+'_mask': _create_dummpy_label(
        params.problem_type[problem]) for problem in problem_list if params.problem_type[problem] in ['seq2seq_tag', 'seq2seq_text']})

    pretrain_dummpy_dict = {
        "masked_lm_positions": _create_dummpy_label('mask_lm'),
        "masked_lm_ids": _create_dummpy_label('mask_lm'),
        "masked_lm_weights": _create_dummpy_label('mask_lm'),
        "next_sentence_label_ids": _create_dummpy_label('cls'),
        "next_sentence_loss_multiplier": 0,
        "masked_lm_loss_multiplier": 0}

    # init gen
    try:
        gen_dict = {problem: params.read_data_fn[problem](params, mode)
                    for problem in problem_list}
    except KeyError:
        not_exist_problem = [
            p for p in problem_list if p not in params.read_data_fn]
        raise KeyError(
            'The preprocessing function of {0} not found, make sure you called params.add_problem. If you\'re using train_bert_multitask, please make sure you provided problem_type_dict and processing_fn_dict.'.format(not_exist_problem))

    while gen_dict:
        # sample problem to train
        if len(problem_chunk) > 1:
            data_num_list = [params.data_num_dict[chunk[0]]
                             for chunk in problem_chunk]
            if params.multitask_balance_type == 'data_balanced':
                sample_prob = np.array(data_num_list) / np.sum(data_num_list)
                current_problem_chunk_ind = np.random.choice(
                    list(range(len(problem_chunk))), p=sample_prob)
                current_problem_chunk = problem_chunk[current_problem_chunk_ind]

            elif params.multitask_balance_type == 'problem_balanced':
                sample_prob = np.array(
                    [1]*len(data_num_list)) / np.sum([1]*len(data_num_list))
                current_problem_chunk_ind = np.random.choice(
                    list(range(len(problem_chunk))), p=sample_prob)
                current_problem_chunk = problem_chunk[current_problem_chunk_ind]
        else:
            current_problem_chunk = problem_chunk[0]

        # create loss multiplier
        loss_multiplier = {
            problem+'_loss_multiplier': 0 for problem in problem_list if params.problem_type[problem] != 'pretrain'}
        for problem in current_problem_chunk:
            if params.problem_type[problem] != 'pretrain':
                loss_multiplier[problem+'_loss_multiplier'] = 1
            else:
                loss_multiplier['next_sentence_loss_multiplier'] = 1
                loss_multiplier['masked_lm_loss_multiplier'] = 1

        base_dict = {}
        base_input = None
        for problem in current_problem_chunk:
            try:
                instance = next(gen_dict[problem])
            except StopIteration:
                if mode == 'train':
                    gen_dict[problem] = params.read_data_fn[problem](
                        params, mode)
                    instance = next(gen_dict[problem])
                else:
                    del gen_dict[problem]
                    continue
            except KeyError:
                continue

            if not instance:
                continue

            base_dict.update(instance)
            if base_input is None:
                base_input = instance['input_ids']
            elif not params.augument_mask_lm:
                assert base_input == instance[
                    'input_ids'], 'Inputs id of two chained problem not aligned. Please double check!'

        if not base_dict:
            continue

        for problem in problem_list:
            problem_type = params.problem_type[problem]
            problem_label_name = '{0}_label_ids'.format(problem)

            if problem_label_name not in base_dict:
                if problem_type == 'seq_tag':
                    base_dict[problem_label_name] = dummy_label_dict[problem_label_name][:len(
                        base_dict['input_ids'])]
                elif problem_type == 'pretrain':
                    if 'masked_lm_ids' not in base_dict:
                        base_dict.update(pretrain_dummpy_dict)
                else:
                    base_dict[problem_label_name] = dummy_label_dict[problem_label_name]

                if problem_type in ['seq2seq_tag', 'seq2seq_text']:
                    base_dict['{0}_mask'.format(
                        problem)] = dummy_label_dict['{0}_mask'.format(problem)]

        # add loss multipliers
        base_dict.update(loss_multiplier)
        yield base_dict
