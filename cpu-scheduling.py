import tkinter as tk
from tkinter import messagebox

def simulate_fcfs():
    processes = entry_processes.get().split(',')
    arrival_times = list(map(int, entry_arrival.get().split(',')))
    burst_times = list(map(int, entry_burst.get().split(',')))

    if len(processes) != len(arrival_times) or len(processes) != len(burst_times):
        messagebox.showerror("Input Error", "Mismatch in the number of processes, arrival times, or burst times.")
        return None

    n = len(processes)
    completion_times = [0] * n
    turnaround_times = [0] * n
    waiting_times = [0] * n

    zipped = sorted(zip(arrival_times, burst_times, processes), key=lambda x: x[0])
    arrival_times, burst_times, processes = map(list, zip(*zipped))

    for i in range(n):
        if i == 0:
            completion_times[i] = arrival_times[i] + burst_times[i]
        else:
            completion_times[i] = max(completion_times[i - 1], arrival_times[i]) + burst_times[i]

    for i in range(n):
        turnaround_times[i] = completion_times[i] - arrival_times[i]
        waiting_times[i] = turnaround_times[i] - burst_times[i]

    return processes, arrival_times, burst_times, completion_times, turnaround_times, waiting_times

def simulate_sjf():
    processes = entry_processes.get().split(',')
    arrival_times = list(map(int, entry_arrival.get().split(',')))
    burst_times = list(map(int, entry_burst.get().split(',')))

    if len(processes) != len(arrival_times) or len(processes) != len(burst_times):
        messagebox.showerror("Input Error", "Mismatch in the number of processes, arrival times, or burst times.")
        return None

    n = len(processes)
    completion_times = [0] * n
    turnaround_times = [0] * n
    waiting_times = [0] * n

    zipped = sorted(zip(arrival_times, burst_times, processes), key=lambda x: (x[0], x[1]))
    arrival_times, burst_times, processes = map(list, zip(*zipped))

    current_time = 0
    completed = 0
    is_completed = [False] * n

    while completed != n:
        idx = -1
        min_burst = float('inf')
        for i in range(n):
            if arrival_times[i] <= current_time and not is_completed[i]:
                if burst_times[i] < min_burst:
                    min_burst = burst_times[i]
                    idx = i

        if idx != -1:
            current_time += burst_times[idx]
            completion_times[idx] = current_time
            turnaround_times[idx] = completion_times[idx] - arrival_times[idx]
            waiting_times[idx] = turnaround_times[idx] - burst_times[idx]
            is_completed[idx] = True
            completed += 1
        else:
            current_time += 1

    return processes, arrival_times, burst_times, completion_times, turnaround_times, waiting_times

def simulate_rr():
    processes = entry_processes.get().split(',')
    arrival_times = list(map(int, entry_arrival.get().split(',')))
    burst_times = list(map(int, entry_burst.get().split(',')))

    if len(processes) != len(arrival_times) or len(processes) != len(burst_times):
        messagebox.showerror("Input Error", "Mismatch in the number of processes, arrival times, or burst times.")
        return None

    n = len(processes)
    completion_times = [0] * n
    turnaround_times = [0] * n
    waiting_times = [0] * n
    remaining_burst_times = burst_times[:]
    time_quantum = 2
    current_time = 0
    queue = []
    gantt_chart = []

    while True:
        done = True
        for i in range(n):
            if remaining_burst_times[i] > 0:
                done = False
                if remaining_burst_times[i] > time_quantum:
                    current_time += time_quantum
                    remaining_burst_times[i] -= time_quantum
                    gantt_chart.append((processes[i], current_time))
                else:
                    current_time += remaining_burst_times[i]
                    completion_times[i] = current_time
                    turnaround_times[i] = completion_times[i] - arrival_times[i]
                    waiting_times[i] = turnaround_times[i] - burst_times[i]
                    remaining_burst_times[i] = 0
                    gantt_chart.append((processes[i], current_time))
        if done:
            break

    return processes, arrival_times, burst_times, completion_times, turnaround_times, waiting_times, gantt_chart

def display_results(processes, arrival_times, burst_times, completion_times, turnaround_times, waiting_times):
    result_text.insert(tk.END, f"Process\tArrival\tBurst\tCompletion\tTurnaround\tWaiting\n", "header")
    for i in range(len(processes)):
        result_text.insert(
            tk.END,
            f"{processes[i]}\t{arrival_times[i]}\t{burst_times[i]}\t{completion_times[i]}\t{turnaround_times[i]}\t{waiting_times[i]}\n",
        )

def draw_gantt_chart(processes, arrival_times, burst_times, completion_times, y_offset):
    start_time = 0
    colors = ["#FF9999", "#99FF99", "#9999FF", "#FFFF99", "#FF99FF", "#99FFFF"]
    for i in range(len(processes)):
        color = colors[i % len(colors)]
        canvas.create_rectangle(start_time * 20, y_offset, completion_times[i] * 20, y_offset + 40, fill=color, outline="black")
        canvas.create_text((start_time * 20 + completion_times[i] * 20) / 2, y_offset + 20, text=processes[i], fill="black")
        start_time = completion_times[i]

def draw_gantt_chart_rr(gantt_chart, y_offset):
    colors = ["#FF9999", "#99FF99", "#9999FF", "#FFFF99", "#FF99FF", "#99FFFF"]
    start_time = 0
    for process, end_time in gantt_chart:
        color = colors[hash(process) % len(colors)]
        canvas.create_rectangle(start_time * 20, y_offset, end_time * 20, y_offset + 40, fill=color, outline="black")
        canvas.create_text((start_time * 20 + end_time * 20) / 2, y_offset + 20, text=process, fill="black")
        start_time = end_time

def run_all_simulations():
    result_text.delete(1.0, tk.END)
    canvas.delete("all")
    result_text.tag_configure("header", font=("Arial", 10, "bold"), foreground="blue")

    y_offset = 20

    fcfs_result = simulate_fcfs()
    if fcfs_result:
        processes, arrival_times, burst_times, completion_times, turnaround_times, waiting_times = fcfs_result
        result_text.insert(tk.END, "FCFS Results:\n", "header")
        display_results(processes, arrival_times, burst_times, completion_times, turnaround_times, waiting_times)
        canvas.create_text(400, y_offset - 10, text="FCFS Gantt Chart", font=("Arial", 12, "bold"))
        draw_gantt_chart(processes, arrival_times, burst_times, completion_times, y_offset)
        y_offset += 60

    sjf_result = simulate_sjf()
    if sjf_result:
        processes, arrival_times, burst_times, completion_times, turnaround_times, waiting_times = sjf_result
        result_text.insert(tk.END, "SJF Results:\n", "header")
        display_results(processes, arrival_times, burst_times, completion_times, turnaround_times, waiting_times)
        canvas.create_text(400, y_offset - 10, text="SJF Gantt Chart", font=("Arial", 12, "bold"))
        draw_gantt_chart(processes, arrival_times, burst_times, completion_times, y_offset)
        y_offset += 60

    rr_result = simulate_rr()
    if rr_result:
        processes, arrival_times, burst_times, completion_times, turnaround_times, waiting_times, gantt_chart = rr_result
        result_text.insert(tk.END, "RR Results:\n", "header")
        display_results(processes, arrival_times, burst_times, completion_times, turnaround_times, waiting_times)
        canvas.create_text(400, y_offset - 10, text="RR Gantt Chart", font=("Arial", 12, "bold"))
        draw_gantt_chart_rr(gantt_chart, y_offset)

root = tk.Tk()
root.title("CPU Scheduling Simulation")
root.geometry("1000x800")
root.config(bg="#F5F5F5")

frame_inputs = tk.Frame(root, bg="#F5F5F5")
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Processes:", bg="#F5F5F5", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
entry_processes = tk.Entry(frame_inputs, width=40)
entry_processes.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Arrival Times:", bg="#F5F5F5", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
entry_arrival = tk.Entry(frame_inputs, width=40)
entry_arrival.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Burst Times:", bg="#F5F5F5", font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
entry_burst = tk.Entry(frame_inputs, width=40)
entry_burst.grid(row=2, column=1, padx=5, pady=5)

tk.Button(root, text="Simulate All", command=run_all_simulations, bg="#007BFF", fg="white", font=("Arial", 12), padx=10, pady=5).pack(pady=10)

frame_results = tk.Frame(root, bg="#F5F5F5")
frame_results.pack(fill=tk.BOTH, expand=True)

result_text = tk.Text(frame_results, height=15, width=80, wrap=tk.WORD, font=("Courier", 10))
result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)

scrollbar = tk.Scrollbar(frame_results, command=result_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_text.config(yscrollcommand=scrollbar.set)

canvas = tk.Canvas(root, bg="white", height=300)
canvas.pack(fill=tk.BOTH, expand=True, pady=10)

root.mainloop()
