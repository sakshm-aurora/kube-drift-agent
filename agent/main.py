# agent/main.py

from agent.collector import KubeCollector
from agent.transmitter import Transmitter
from agent.config import config as agent_config  # If you need to use agent_config here

def run_agent():
    collector = KubeCollector()
    data = collector.collect_all()
    transmitter = Transmitter()
    transmitter.send_data(data)

if __name__ == '__main__':
    run_agent()