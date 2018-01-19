import boto3
import os
import pickle
import json
import numpy as np
import torch
from model import RNN
from torch.autograd import Variable

ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')
BUCKET_NAME = os.environ.get('BUCKET_NAME')
MODEL_KEY = os.environ.get('MODEL_KEY') # model.pth
PARAMS_KEY = os.environ.get('PARAMS_KEY') # params.pkl

max_length = os.environ.get('max_length') # 20
max_length = int(max_length)

s3_client = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

# Load preprocessing parameters
if not os.path.isfile('/tmp/params.pkl'):
    s3_client.download_file(BUCKET_NAME, 'params.pkl', '/tmp/params.pkl')
with open('/tmp/params.pkl', 'rb') as pkl:
    params = pickle.load(pkl)
all_categories = params['all_categories']
n_categories = params['n_categories']
all_letters = params['all_letters']
n_letters = params['n_letters']

# Check if models are available
# Download model from S3 if model is not already present
if not os.path.isfile('/tmp/model.pth'):
    s3_client.download_file(BUCKET_NAME, 'model.pth', '/tmp/model.pth')
rnn = RNN(n_letters, 128, n_letters, n_categories=n_categories)
rnn.load_state_dict(torch.load("/tmp/model.pth"))
rnn.eval()

def inputTensor(line):
    tensor = torch.zeros(len(line), 1, n_letters)
    for li in range(len(line)):
        letter = line[li]
        tensor[li][0][all_letters.find(letter)] = 1
    return tensor

def categoryTensor(category):
    li = all_categories.index(category)
    tensor = torch.zeros(1, n_categories)
    tensor[0][li] = 1
    return tensor

# Sample from a category and starting letter
def sample(category, start_letter='A'):
    category_tensor = Variable(categoryTensor(category))
    input = Variable(inputTensor(start_letter))
    hidden = rnn.initHidden()

    output_name = start_letter

    for i in range(max_length):
        output, hidden = rnn(category_tensor, input[0], hidden)
        topv, topi = output.data.topk(1)
        topi = topi[0][0]
        if topi == n_letters - 1:
            break
        else:
            letter = all_letters[topi]
            output_name += letter
        input = Variable(inputTensor(letter))

    return output_name

# Get multiple samples from one category and multiple starting letters
def samples(category, start_letters='ABC'):
    for start_letter in start_letters:
        yield sample(category, start_letter)

def lambda_handler(event, context):

    print('event:', event)
    output_names = list(samples(event['category'], event['start_letters']))
    print('output_names', output_names)
    
    # return results formatted for AWS API Gateway
    result = {"statusCode": 200, \
            "headers": {"Content-Type": "application/json"}, \
             "body": json.dumps(output_names)}
    return result