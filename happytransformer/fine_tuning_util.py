"""
Contains functions that are shared amongst the children of the HappyTrainer class.

Based on
https://github.com/huggingface/transformers/blob/master/examples/pytorch/language-modeling/run_mlm.py
and
https://github.com/huggingface/transformers/blob/master/examples/pytorch/language-modeling/run_clm.py
"""


def preprocess_concatenate(tokenizer, datasets, args, mlm=True):
    """
    :param tokenizer: tokenizer for a transformer model
    :param datasets: a datasets.Dataset object
    :param args: A dictionary that contains settings
    :return:
    """

    max_input_length = tokenizer.model_max_length


    def tokenize_function(example):
        return tokenizer(example["text"],
                         add_special_tokens=True, truncation=True,)

    tokenized_datasets = datasets.map(tokenize_function, batched=True,
                                      num_proc=args["preprocessing_processes"],
                                      remove_columns=["text"])

    def group_texts(examples):
        concatenated_examples = {k: sum(examples[k], []) for k in examples.keys()}
        total_length = len(concatenated_examples[list(examples.keys())[0]])
        output_length = (total_length // max_input_length) * max_input_length

        # if  total_length is less than the max_input_length length
        # then it causes an error unless the code below is used.
        # this is due to total_length being truncated to 0
        if output_length == 0:
            output_length = total_length

        result = {
            k: [t[i: i + max_input_length] for i in range(0, output_length, max_input_length)]
            for k, t in concatenated_examples.items()
        }

        if not mlm:
            # Masked language models don't need labels. Text generation models do
            result["labels"] = result["input_ids"].copy()
        return result

    tokenized_datasets = tokenized_datasets.map(
        group_texts,
        batched=True,
        num_proc=args["preprocessing_processes"],
    )


    return tokenized_datasets