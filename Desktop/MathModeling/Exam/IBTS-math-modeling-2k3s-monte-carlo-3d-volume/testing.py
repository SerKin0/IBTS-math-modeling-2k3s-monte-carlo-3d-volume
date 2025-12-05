from monte_carlo import monte_carlo_3rd
import time
import csv
import json

def check_inside_function(x: float, y: float, z: float) -> bool:
    return (x*x + y*y - 1 <= z*z) & (z*z <= 3/5 * (x*x + y*y + 1))

def std(data: list[float]) -> float:
    n = len(data)
    middle = sum(data) / n
    numerical = sum([(middle - i)**2 for i in data])
    return (numerical / n)**0.5 

N = 100
k_student = 1.95
count_points_param = (0, 1_000_001, 2_000)

filename = f"tests/test_count_points_{count_points_param[0]}-{count_points_param[1]}-{count_points_param[2]}_N-{N}.csv"

with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([
        "N",
        "count_points",
        "std_data",
        "mean_data",
        "min_data",
        "max_data",
        "random_error_data",
        "data",
        "std_time",
        "mean_time",
        "min_time",
        "max_time",
        "random_error_time",
        "time"
    ])
    
    for count_points in range(*count_points_param):
        if count_points_param == 0:
            continue
        data_list = []
        time_list = []
        
        for _ in range(N):
            start_time = time.time()
            value_monte_carlo = monte_carlo_3rd(
                func=check_inside_function, 
                x_lim=(-3, 3), 
                y_lim=(-3, 3), 
                z_lim=(-3, 3), 
                n=count_points
                ) 
            end_time = time.time()
            
            delta_time = end_time - start_time
            data_list.append(value_monte_carlo)
            time_list.append(delta_time)
            
        std_data = std(data_list)
        mean_data = sum(data_list) / len(data_list)
        min_data = min(data_list)
        max_data = max(data_list)
        random_error_data = 1.95 * std_data / 3
        
        std_time = std(time_list)
        mean_time = sum(time_list) / len(time_list)
        min_time = min(time_list)
        max_time = max(time_list)
        random_error_time = 1.95 * std_time / 3
        
        writer.writerow(
            [
                N,
                count_points,
                std_data,
                mean_data,
                min_data,
                max_data,
                random_error_data,
                json.dumps(data_list),
                std_time,
                mean_time,
                min_time,
                max_time,
                random_error_time,
                json.dumps(time_list)
            ]
        )
        
        print(f"Finish: {count_points=}")