# gpt2
API client for GPT-2 text generator hosted on the cloud by Open Medical IO

Generate synthetic text from your custom prompt with  the latest released 774M model of OpenAI's GPT-2.
We take care of the GPU backend.
See [openmedical.io/gpt2](https://openmedical.io/gpt2) for product demo and obtaining an API key!

## Installation 
pip install --upgrade gpt2

## Usage
```python
from gpt2 import Client
c = Client('API SECRET')
output_list = c.fast_generate(prompt='On a perfect summer day we went to')

"""
Generate text on the large 774M model using your own prompt and standard parameters.
This only takes a few seconds per query.
We're training additional models for your use in the near future, such as 774M finetuned on Chinese, Spanish, Wikipedia...
We're also releasing finetuning APIs in September 2019.
Stay tuned :)
"""
```
