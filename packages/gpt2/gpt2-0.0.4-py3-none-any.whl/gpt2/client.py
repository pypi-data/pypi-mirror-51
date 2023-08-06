import requests, json, time, copy, os
from pathlib import Path

dot = Path(__file__).parent
default_model_name = '774M'


class Client():
    def __init__(self, secret):
        self.secret = secret
        # self.url = 'http://127.0.0.1:8000/gpt2/api'
        self.url='https://www.openmedical.io/gpt2/api'
        self.session = requests.Session()

    def fast_generate(self,
                      prompt,
                      model_name=default_model_name,
                      ):
        kwargs = copy.deepcopy(locals())
        del kwargs['self']
        return self.generate(**kwargs, shared=True)

    def generate(self,
                 prompt='',
                 nsamples=1,
                 length=100,
                 temperature=.7,
                 top_k=0,
                 model_name=default_model_name,
                 shared=False,

                 ):
        nsamples_max = 15
        length_max = 200
        prompt = prompt.strip()
        assert nsamples < nsamples_max, f'nsamples must be less than {nsamples_max}'
        if shared:
            assert length < length_max, f'length must be less than {length_max}'

        kwargs = copy.deepcopy(locals())
        del kwargs['self']
        return self._send_message('generate', kwargs=kwargs)

    def finetune(self,
                 target_model_name,
                 dataset_path='',
                 base_model_name=default_model_name,
                 upload=True,
                 steps=500,
                 ):
        if target_model_name == default_model_name:
            print(f'Cannot overwrite default model {default_model_name}.')
            raise AssertionError
        dataset_name = os.path.basename(dataset_path)
        if upload:
            dataset = Path(dataset_path).read_text()
        kwargs = copy.deepcopy(locals())
        del kwargs['self']
        return self._send_message('finetune', kwargs=kwargs)

    def _send_message(self, method, kwargs):
        print(method)
        print(kwargs)
        url = self.url
        data = {}
        data['secret'] = self.secret
        data['kwargs'] = kwargs
        data['method'] = method
        data['result'] = ''
        data['tag'] = ''
        data['charge'] = True
        data['status'] = 'pending'
        data['messages'] = []
        data['id'] = str(time.time())

        load1 = {'blob': json.dumps({**data, 'mode': 'post'})}
        load2 = {'blob': json.dumps({**{x: data[x] for x in ('secret', 'id')}, 'mode': 'get'})}

        r = self.session.post(url=url, json=load1, ).json()

        # polling to be replaced by socket streaming in future
        while True:
            result = r['result']
            status = r['status']
            messages = ('\n'.join(r['messages']))
            if messages:
                print(messages)
            if status in ['done', 'failed']:
                print(f'Status: {status}')
                if status == 'done':
                    print(f'Result\n{result}\n')
                    return result
                elif status == 'failed':

                    raise AssertionError
            time.sleep(1)
            try:
                r = self.session.post(url=url, json=load2, ).json()
            except:
                pass

# from gpt2 import Client
# c = Client('API SECRET')
#
# """
# Generate text on the large 774M model using your own prompt and standard parameters.
# This only takes around 5 seconds per query.
# We're training additional models for your use in the near future, such as ones finetuned on Chinese, Spanish, Wikipedia...
# """
# output_list = c.fast_generate(prompt='On a perfect summer day we went to')
#
###########################
