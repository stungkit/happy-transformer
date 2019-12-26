"""
We will finish HappyXLM in January 2020
# pylint: disable=W0511
from transformers import XLMWithLMHeadModel, XLMTokenizer

from happy_transformer.happy_transformer import HappyTransformer


class HappyXLM(HappyTransformer):
    \"""
    Implementation of XLM for masked word prediction
    masked_token = '<special1>'
    sep_token =  '</s>'
    cls_token =  '</s>'
    \"""

    def __init__(self, model='xlm-mlm-en-2048', initial_transformers=[]):
        super().__init__(model)
        self.mlm = XLMWithLMHeadModel.from_pretrained(model)
        self.tokenizer = XLMTokenizer.from_pretrained(model)
        self.masked_token = self.tokenizer.mask_token
        self.sep_token = self.tokenizer.sep_token
        self.cls_token = self.tokenizer.cls_token
        self.model = 'XLM'
        self._get_initial_transformers(initial_transformers)

    def _get_masked_language_model(self):
        \"""
        Initializes the XLMWithLMHeadModel transformer
        \"""
        self.mlm = XLMWithLMHeadModel.from_pretrained(self.model_to_use)
        self.mlm.eval()
"""