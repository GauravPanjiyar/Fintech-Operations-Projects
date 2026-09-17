import pandas as pd
import numpy as np

np.random.seed(42)
n_tasks = 150

data = {
    'Task_ID': [f'TSK_{i:03d}' for i in range(1, n_tasks + 1)],
    'Required_Man_Hours': np.random.randint(10, 60, size=n_tasks),
    'Base_Cost_Per_Hour': np.random.randint(250, 700, size=n_tasks),
    'Priority_Level': np.random.choice([1, 2, 3], size=n_tasks, p=[0.2, 0.5, 0.3])
}

df_tasks = pd.DataFrame(data)
df_tasks['Total_Cost'] = df_tasks['Required_Man_Hours'] * df_tasks['Base_Cost_Per_Hour']

total_budget_limit = 500000

df_tasks['Cost_Efficiency_Score'] = (df_tasks['Priority_Level'] * 1000) / df_tasks['Total_Cost']
df_sorted = df_tasks.sort_values(by='Cost_Efficiency_Score', ascending=False).reset_index(drop=True)

allocated_budget = 0
selected_tasks = []

for index, row in df_sorted.iterrows():
    if allocated_budget + row['Total_Cost'] <= total_budget_limit:
        allocated_budget += row['Total_Cost']
        selected_tasks.append({
            'Task_ID': row['Task_ID'],
            'Priority_Level': row['Priority_Level'],
            'Required_Man_Hours': row['Required_Man_Hours'],
            'Total_Cost': row['Total_Cost'],
            'Status': 'Approved & Allocated'
        })
    else:
        selected_tasks.append({
            'Task_ID': row['Task_ID'],
            'Priority_Level': row['Priority_Level'],
            'Required_Man_Hours': row['Required_Man_Hours'],
            'Total_Cost': row['Total_Cost'],
            'Status': 'Deferred / Unallocated'
        })

df_report = pd.DataFrame(selected_tasks)
df_report.to_csv('optimized_allocation_report.csv', index=False)

!pip install simpy

import simpy
import random
import pandas as pd

def process_workflow_task(env, task_id, processing_server, metrics_log):
    arrival_time = env.now

    with processing_server.request() as request_slot:
        yield request_slot
        wait_time = env.now - arrival_time

        service_time = max(1.0, random.normalvariate(6.0, 1.5))
        yield env.timeout(service_time)

        total_completion_time = env.now - arrival_time

        metrics_log.append({
            'Task_ID': task_id,
            'Arrival_Time': round(arrival_time, 2),
            'Wait_Time_In_Queue': round(wait_time, 2),
            'Service_Duration': round(service_time, 2),
            'Total_Turnaround_Time': round(total_completion_time, 2)
        })

def task_generator(env, servers_capacity, arrival_rate, metrics_log):
    server = simpy.Resource(env, capacity=servers_capacity)
    task_id = 1
    while True:
        yield env.timeout(random.expovariate(arrival_rate))
        env.process(process_workflow_task(env, f"REQ_{task_id:04d}", server, metrics_log))
        task_id += 1

simulation_metrics = []
environment = simpy.Environment()

environment.process(task_generator(env=environment, servers_capacity=4, arrival_rate=0.8, metrics_log=simulation_metrics))
environment.run(until=200)

df_sim_results = pd.DataFrame(simulation_metrics)
df_sim_results.to_csv('workflow_simulation_metrics.csv', index=False)
