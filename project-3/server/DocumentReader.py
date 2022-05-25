import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from collections import OrderedDict

"""
This DocumentReader class comes from a blog, Building a QA System with BERT
on Wikipedia. I only made minor changes to it.
See:
https://qa.fastforwardlabs.com/pytorch/hugging%20face/wikipedia/bert/transformers/2020/05/19/Getting_Started_with_QA.html#QA-on-Wikipedia-pages
"""


class DocumentReader:
    def __init__(
        self, pretrained_model_name_or_path='bert-large-uncased', model=None
    ):
        self.READER_PATH = pretrained_model_name_or_path
        self.tokenizer = AutoTokenizer.from_pretrained(self.READER_PATH)
        self.model = model or \
            AutoModelForQuestionAnswering.from_pretrained(self.READER_PATH)
        self.max_len = self.model.config.max_position_embeddings
        self.chunked = False
        self.model.eval()

    def tokenize(self, question, text):
        self.inputs = self.tokenizer.encode_plus(
            question, text, add_special_tokens=True, return_tensors="pt")
        self.input_ids = self.inputs["input_ids"].tolist()[0]

        if len(self.input_ids) > self.max_len:
            self.inputs = self.chunkify()
            self.chunked = True

    def chunkify(self):
        """
        Break up a long article into chunks that fit within the max token
        requirement for that Transformer model.

        Calls to BERT / RoBERTa / ALBERT require the following format:
        [CLS] question tokens [SEP] context tokens [SEP].
        """

        # create question mask based on token_type_ids
        # value is 0 for question tokens, 1 for context tokens
        qmask = self.inputs['token_type_ids'].lt(1)
        qt = torch.masked_select(self.inputs['input_ids'], qmask)
        # the "-1" accounts for having to add an ending [SEP] token to the end
        chunk_size = self.max_len - qt.size()[0] - 1

        # create dict of dicts
        # each sub-dict mimics the structure of pre-chunked model input
        chunked_input = OrderedDict()
        for k, v in self.inputs.items():
            q = torch.masked_select(v, qmask)
            c = torch.masked_select(v, ~qmask)
            chunks = torch.split(c, chunk_size)

            for i, chunk in enumerate(chunks):
                if i not in chunked_input:
                    chunked_input[i] = {}

                thing = torch.cat((q, chunk))
                if i != len(chunks)-1:
                    if k == 'input_ids':
                        thing = torch.cat((thing, torch.tensor([102])))
                    else:
                        thing = torch.cat((thing, torch.tensor([1])))

                chunked_input[i][k] = torch.unsqueeze(thing, dim=0)
        return chunked_input

    def get_answer(self):
        if self.chunked:
            answer = ''
            for k, chunk in self.inputs.items():
                answer_start_scores, answer_end_scores = \
                    self.model(**chunk, return_dict=False)

                answer_start = torch.argmax(answer_start_scores)
                answer_end = torch.argmax(answer_end_scores) + 1

                ans = self.convert_ids_to_string(
                    chunk['input_ids'][0][answer_start:answer_end])
                print(ans)
                if ans != '[CLS]' and not answer:
                    answer = ans
            return answer
        else:
            answer_start_scores, answer_end_scores = self.model(**self.inputs)

            # get most likely beginning of answer with the argmax of the score
            answer_start = torch.argmax(answer_start_scores)
            # get the most likely end of answer with the argmax of the score
            answer_end = torch.argmax(answer_end_scores) + 1

            return self.convert_ids_to_string(self.inputs['input_ids'][0][
                                            answer_start:answer_end])

    def convert_ids_to_string(self, input_ids):
        return self.tokenizer.convert_tokens_to_string(
            self.tokenizer.convert_ids_to_tokens(input_ids))


custom_model = "bert-large-uncased"
pretrained_model = "deepset/bert-base-cased-squad2"

pretrained_reader = DocumentReader(pretrained_model)
custom_trained_reader = DocumentReader(custom_model)
