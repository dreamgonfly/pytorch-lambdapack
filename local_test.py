import os
os.environ['ACCESS_KEY'] = 'AKIAIQMNSIERHGC7EMWQ'
os.environ['SECRET_KEY'] = '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'
os.environ['MODEL_KEY'] = 'model.pth'
os.environ['PARAMS_KEY'] = 'params.pkl'
os.environ['BUCKET_NAME'] = 'pytorch-lambda'
os.environ['max_length'] = '20'


event = {'category':'Russian', 'start_letters':'RUS'}

from lambda_function import lambda_handler
lambda_handler(event=event, context=None)