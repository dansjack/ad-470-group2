import torch
from transformers import BertTokenizerFast


# From Abenezer + Jeff's colab
def predict(model, query, context):
    with torch.no_grad():
        tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')
        model.eval()
        inputs = tokenizer.encode_plus(
            text=context,
            text_pair=query,
            max_length=512,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
            ).to(torch.device('cpu'))

        outputs = model(
            input_ids=inputs['input_ids'],
            attention_mask=inputs['attention_mask'],
            token_type_ids=inputs['token_type_ids']
            )

        ans_start = torch.argmax(outputs[0])
        ans_end = torch.argmax(outputs[1])
        ans = tokenizer.convert_tokens_to_string(
            tokenizer.convert_ids_to_tokens(
                inputs['input_ids'][0][ans_start:ans_end+1]
                )
            )
        return ans
