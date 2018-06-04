import json
import os.path
import numpy as np
from time import localtime, strftime
from pynput.keyboard import Key, Controller

class Memory():
    """
    Atributtes
    """
    def __init__(self):
        self.steps = 0
        self.episode = 0
        self.evolution = {'episode': [], 'steps': [], 'start_point': [], 'started_at': [], 'ended_at': []}

    """
    Methods
    """
    #get last episode executed from JSON q_evolution file
    def get_last_episode(self):
        
        if os.path.exists('q_evolution.json'):
            with open('q_evolution.json', 'r') as e:
                self.evolution = json.load(e)
            self.episode = max(self.evolution['episode'])
            return self.episode
        else:
            return 0
    
    #record total of steps and current episode ended in JSON file
    def record_steps(self, steps, episode, start_point, started_time):
        
        self.episode = self.episode + 1
        self.evolution['episode'].append(self.episode)
        self.evolution['steps'].append(steps)
        self.evolution['start_point'].append(start_point)
        self.evolution['started_at'].append(started_time)
        self.evolution['ended_at'].append(strftime("%Y-%m-%d %H:%M:%S", localtime()))
        #send current episode data to json file
        with open('q_evolution.json', 'w') as fp:
            json.dump(self.evolution, fp)

        #return self.evolution
    
    def reset_agent(self, steps, episode, start_point, start_time, tableQ):
        self.episode = episode
        self.steps = steps
        self.record_steps(self.steps, self.episode, start_point, start_time)
        tablename = "tableq_ep_%d.csv" % self.episode
        np.savetxt(tablename, tableQ, fmt='%.2f', delimiter=',', header=" #1,  #2,  #3,  #4 ")
        Controller().press(Key.f11)
        Controller().press(Key.f11)
        Controller().press(Key.f11)
        Controller().press('a')
        Controller().release('a')

"""
#How to get data from q_evolution.json file with pandas
with open('q_evolution.json', 'r') as f:a
        datastore = json.load(f)

print datastore

df_evolution = pd.DataFrame(datastore, columns=datastore.keys())
df_evolution = df_evolution[["episode", "steps", "start_point", "started_at", "ended_at"]]
print df_evolution"""
