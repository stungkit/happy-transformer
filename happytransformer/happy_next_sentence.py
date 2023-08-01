from typing import Union

import torch
from transformers import AutoModelForNextSentencePrediction

from happytransformer.adaptors import get_adaptor
from happytransformer.happy_transformer import HappyTransformer

class HappyNextSentence(HappyTransformer):
    def __init__(self, model_type="BERT",
                 model_name="bert-base-uncased", 
                 load_path: str = "", 
                 use_auth_token:  Union[bool, str]  = None):

        self.adaptor = get_adaptor(model_type)
        model_class = AutoModelForNextSentencePrediction

        super().__init__(model_type, model_name, model_class, use_auth_token=use_auth_token, load_path=load_path)

        self._pipeline_class = None  # we don't use a pipeline for inference

        self._type = "ns"

    def predict_next_sentence(self, sentence_a: str, sentence_b: str) -> float:
        encoded = self.tokenizer(sentence_a, sentence_b, return_tensors='pt')
        encoded.to(self.device)

        with torch.no_grad():
            scores = self.model(encoded['input_ids'], token_type_ids=encoded['token_type_ids']).logits[0]

        probabilities = torch.softmax(scores, dim=0)
        # probability that sentence B follows sentence A
        score = probabilities[0].item()

        if self.device.type == 'cuda':
            torch.cuda.empty_cache()

        return score

    def train(self, input_filepath,  args=None,  eval_filepath: str = ""):
        raise NotImplementedError("train() is currently not available")

    def eval(self, input_filepath, args=None):
        raise NotImplementedError("eval() is currently not available")

    def test(self, input_filepath, args=None):
        raise NotImplementedError("test() is currently not available")
