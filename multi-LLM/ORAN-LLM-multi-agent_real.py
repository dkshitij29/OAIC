import openai
from dotenv import dotenv_values
# from langchain.schema import HumanMessage
# from langchain.chat_models import AzureChatOpenA
import chardet
import warnings
import numpy as np
import re
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TKAgg')
import json
import random
import argparse
from env_multi import Environ
import os
import time


random.seed(123)
def extract_float_numbers(input_string):
    # Use regular expression to find all float numbers in the string
    float_numbers = re.findall(r"[-+]?\d*\.\d+|\d+", input_string)
    
    # Convert the strings to actual float values
    float_numbers = [float(number) for number in float_numbers]
    
    return float_numbers
  
# Detect the encoding of the file
with open('.env', 'rb') as file:
    result = chardet.detect(file.read())

# Use the detected encoding to open the file
with open('.env', 'r', encoding=result['encoding']) as file:
    secrets = dotenv_values(stream=file)


# Sorting the list in descending order and getting corresponding indices

def optimization_cache(action_list, state_list, score_list):
    sorted_indices = sorted(enumerate(score_list), key=lambda x: x[1], reverse=False)
    sorted_indices = [index for index, value in sorted_indices]
    Range = 25
    if len(sorted_indices)>Range:
        action_list_sorted = [action_list[idx] for idx in range(len(score_list)-Range, len(score_list))]
        state_list_sorted = [state_list[idx] for idx in range(len(score_list)-Range, len(score_list))]
        score_list_sorted = [score_list[idx] for idx in range(len(score_list)-Range, len(score_list))]
    else: 
        action_list_sorted = action_list
        state_list_sorted = state_list
        score_list_sorted = score_list
    optimized_solution_history=''
    for i in range(len(score_list_sorted)):
        optimized_solution_history+=""" action: A="""+str(action_list_sorted[i])+', state: '+str(state_list_sorted[i]) + ', reward score: ='+str(round(score_list_sorted[i],4))+'\n'


    return optimized_solution_history

def LLM_agent1(s, optimized_solution_history):
    instruction = ' You will help me optimize the policy of resource allocation agent. The state and action pairs are arranged together with their reward scores, where higher scores are better. With previous state action pair list: '+ optimized_solution_history +', generate a new action\
                    given the current state: '+ str(s) +'\
                    Output must only have the action index, there are only total 2 actions:\
                    output:\
                    A=<value>\
                    Replace the <value> with your corresponding action index value selected from {0,1}\
                    Do not write code or steps or addtional explaining words.'


    optimizer_response = openai.ChatCompletion.create(
        api_key=secrets['OPENAI_API_KEY'],
        organization=secrets['OPENAI_organization'],
        api_base=secrets['openai_api_base'],
        api_type=secrets['openai_api_type'],
        api_version=secrets['API_VERSION'],
        engine=secrets['model_2'],
        messages=[{"role": "system", "content": "You are an optimizer bot."},
                    {"role": "user", "content": instruction}],
        temperature=2,
        max_tokens=500,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )

    # Extract the solution from the optimizer response.
    optimized_solution = optimizer_response['choices'][0]['message']['content']
    result = extract_float_numbers(optimized_solution)
    action=result[0]
    return action

def LLM_agent2(s, optimized_solution_history):
    instruction = ' You will help me optimize the policy of resource allocation agent. The state and action pairs are arranged together with their reward scores, where higher scores are better. With previous state action pair list: '+ optimized_solution_history +', generate a new action\
                    given the current state: '+ str(s) +'\
                    Output must only have the action index, there are only total 2 actions:\
                    output:\
                    A=<value>\
                    Replace the <value> with your corresponding action index value selected from {0,1}\
                    Do not write code or steps or addtional explaining words.'


    optimizer_response = openai.ChatCompletion.create(
        api_key=secrets['OPENAI_API_KEY'],
        organization=secrets['OPENAI_organization'],
        api_base=secrets['openai_api_base'],
        api_type=secrets['openai_api_type'],
        api_version=secrets['API_VERSION'],
        engine=secrets['model_2'],
        messages=[{"role": "system", "content": "You are an optimizer bot."},
                    {"role": "user", "content": instruction}],
        temperature=2,
        max_tokens=500,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )

    # Extract the solution from the optimizer response.
    optimized_solution = optimizer_response['choices'][0]['message']['content']
    result = extract_float_numbers(optimized_solution)
    action=result[0]
    return action



parser = argparse.ArgumentParser()
parser.add_argument('--save_path', type=str, default='mallm-test', help='min explore noise')
opt = parser.parse_args()
opt.Max_train_steps=1
opt.random_steps=4
total_steps = 0
time_stamp=1000
if not os.path.exists(opt.save_path):
    os.makedirs(opt.save_path)

env = Environ(flow_number_highest=3, flow_number_lowest=2, path = opt.save_path, time_stamp=time_stamp)

while total_steps < opt.Max_train_steps:
    s_list = env.Reset(eps=total_steps) # Do not use opt.seed directly, or it can overfit to opt.seed
    state_list=[]
    action_list1=[]
    reward_list1=[]
    action_list2=[]
    reward_list2=[]
    '''Interact & trian'''
    # while not done:
    for ts in range(time_stamp):
        s=s_list

        # if total_steps < opt.random_steps: 
        #     a = env.randsample()
        # else:
        # a = agent.select_action(s)
        if ts<5:
           action1=np.random.randint(0,2)
           action2=np.random.randint(0,2)

        else:
            # optimized_solution_history += '\n'+optimized_solution_best
            time.sleep(2)
            Ts_theshold=np.max([100-ts,10])
            
            if np.random.randint(0,100)<Ts_theshold:
                action1=np.random.randint(0,2)
                action2=np.random.randint(0,2)
            else: 
                action1 = LLM_agent1(s, optimized_solution_history1)
                time.sleep(1.5)

                action2 = LLM_agent2(s, optimized_solution_history2)

        s_list, r_list = env.step(action1, action2, ts, option='test') # dw: dead&win; tr: truncated

        reward1 = r_list[0]
        reward2 = r_list[1]
        state_list.append(s)
        action_list1.append(action1)
        action_list2.append(action2)

        reward_list1.append(reward1)
        reward_list2.append(reward2)
        optimized_solution_history1 = optimization_cache(action_list1, state_list, reward_list1)
        optimized_solution_history2 = optimization_cache(action_list2, state_list, reward_list2)

        # if ts>20:
        #     i=np.random.randint()
        #     optimized_solution_history_batch = optimized_solution_history[i:]
        # else: 
        #     optimized_solution_history_batch = optimization_cache(s, action, reward)
        # Use scoring information to guide the next iteration or stop if satisfied.
        print(f"Time step {ts+1}: reward Score: agent1 {reward1}, agent2 {reward2}")


        # You can add logic here to decide whether to continue refining or stop based on the scorer's feedback.

