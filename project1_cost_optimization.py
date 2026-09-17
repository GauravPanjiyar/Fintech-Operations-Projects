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
