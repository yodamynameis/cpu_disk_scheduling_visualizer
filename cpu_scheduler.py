class CPUScheduler:
    def __init__(self):
        self.processes = []
    
    def add_process(self, name, arrival_time, burst_time, priority=0):
        self.processes.append({
            'name': name,
            'arrival_time': arrival_time,
            'burst_time': burst_time,
            'remaining_time': burst_time,
            'priority': priority,
            'start_time': -1,
            'completion_time': -1,
            'first_execution': -1
        })
    
    def reset_processes(self):
        for process in self.processes:
            process['remaining_time'] = process['burst_time']
            process['start_time'] = -1
            process['completion_time'] = -1
            process['first_execution'] = -1
    
    def get_process_by_name(self, name):
        """Get the original process object by name"""
        for process in self.processes:
            if process['name'] == name:
                return process
        return None
    
    def update_process_state(self, name, **kwargs):
        """Update the state of the original process"""
        process = self.get_process_by_name(name)
        if process:
            for key, value in kwargs.items():
                process[key] = value
    
    def fcfs(self):
        if not self.processes:
            return []
        
        self.reset_processes()
        # Sort by arrival time
        sorted_processes = sorted(self.processes, key=lambda x: x['arrival_time'])
        
        gantt_chart = []
        current_time = 0
        
        for process in sorted_processes:
            if current_time < process['arrival_time']:
                current_time = process['arrival_time']
            
            start_time = current_time
            end_time = current_time + process['burst_time']
            gantt_chart.append((process['name'], start_time, end_time))
            current_time = end_time
            
            # Update the original process
            self.update_process_state(process['name'], 
                                    start_time=start_time,
                                    completion_time=end_time,
                                    first_execution=start_time)
        
        return gantt_chart
    
    def sjf(self):
        if not self.processes:
            return []
        
        self.reset_processes()
        # Work with original processes, not copies
        current_time = 0
        completed = 0
        n = len(self.processes)
        gantt_chart = []
        
        while completed < n:
            # Get available processes that haven't completed
            available = [p for p in self.processes 
                        if p['arrival_time'] <= current_time and p['remaining_time'] > 0]
            
            if not available:
                current_time += 1
                continue
            
            # Select process with shortest burst time
            next_process = min(available, key=lambda x: x['burst_time'])
            
            start_time = current_time
            end_time = current_time + next_process['burst_time']
            gantt_chart.append((next_process['name'], start_time, end_time))
            
            current_time = end_time
            next_process['remaining_time'] = 0
            next_process['start_time'] = start_time
            next_process['completion_time'] = end_time
            next_process['first_execution'] = start_time
            completed += 1
        
        return gantt_chart
    
    def srtf(self):
        if not self.processes:
            return []
        
        self.reset_processes()
        current_time = 0
        completed = 0
        n = len(self.processes)
        gantt_chart = []
        current_process = None
        last_time = 0
        
        while completed < n:
            # Get available processes
            available = [p for p in self.processes 
                        if p['arrival_time'] <= current_time and p['remaining_time'] > 0]
            
            if not available:
                if current_process:
                    # End the current process segment
                    gantt_chart.append((current_process['name'], last_time, current_time))
                    current_process = None
                current_time += 1
                continue
            
            # Select process with shortest remaining time
            next_process = min(available, key=lambda x: x['remaining_time'])
            
            if current_process != next_process:
                if current_process is not None and current_process['remaining_time'] > 0:
                    # Add previous process to gantt chart
                    gantt_chart.append((current_process['name'], last_time, current_time))
                
                current_process = next_process
                last_time = current_time
                
                if current_process['first_execution'] == -1:
                    current_process['first_execution'] = current_time
                if current_process['start_time'] == -1:
                    current_process['start_time'] = current_time
            
            # Execute for 1 time unit
            current_time += 1
            current_process['remaining_time'] -= 1
            
            if current_process['remaining_time'] == 0:
                gantt_chart.append((current_process['name'], last_time, current_time))
                current_process['completion_time'] = current_time
                completed += 1
                current_process = None
        
        return gantt_chart
    
    def round_robin(self, time_quantum=2):
        if not self.processes:
            return []
        
        self.reset_processes()
        current_time = 0
        queue = []
        n = len(self.processes)
        completed = 0
        gantt_chart = []
        
        # Sort by arrival time initially
        sorted_processes = sorted(self.processes, key=lambda x: x['arrival_time'])
        
        while completed < n:
            # Add arriving processes to queue
            for p in sorted_processes:
                if (p['arrival_time'] <= current_time and 
                    p not in queue and p['remaining_time'] > 0):
                    queue.append(p)
            
            if not queue:
                current_time += 1
                continue
            
            current_process = queue.pop(0)
            
            if current_process['first_execution'] == -1:
                current_process['first_execution'] = current_time
            if current_process['start_time'] == -1:
                current_process['start_time'] = current_time
            
            start_time = current_time
            
            if current_process['remaining_time'] <= time_quantum:
                # Process completes
                execution_time = current_process['remaining_time']
                end_time = current_time + execution_time
                gantt_chart.append((current_process['name'], start_time, end_time))
                current_time = end_time
                current_process['remaining_time'] = 0
                current_process['completion_time'] = end_time
                completed += 1
            else:
                # Process uses full quantum
                end_time = current_time + time_quantum
                gantt_chart.append((current_process['name'], start_time, end_time))
                current_time = end_time
                current_process['remaining_time'] -= time_quantum
                
                # Add arriving processes during this execution
                for p in sorted_processes:
                    if (p['arrival_time'] <= current_time and 
                        p not in queue and p['remaining_time'] > 0 and p != current_process):
                        queue.append(p)
                
                # Add back to queue if not finished
                if current_process['remaining_time'] > 0:
                    queue.append(current_process)
        
        return gantt_chart
    
    def priority_scheduling(self):
        if not self.processes:
            return []
        
        self.reset_processes()
        current_time = 0
        completed = 0
        n = len(self.processes)
        gantt_chart = []
        
        while completed < n:
            # Get available processes
            available = [p for p in self.processes 
                        if p['arrival_time'] <= current_time and p['remaining_time'] > 0]
            
            if not available:
                current_time += 1
                continue
            
            # Select process with highest priority (lowest number = highest priority)
            next_process = min(available, key=lambda x: x['priority'])
            
            start_time = current_time
            end_time = current_time + next_process['burst_time']
            gantt_chart.append((next_process['name'], start_time, end_time))
            
            current_time = end_time
            next_process['remaining_time'] = 0
            next_process['start_time'] = start_time
            next_process['completion_time'] = end_time
            next_process['first_execution'] = start_time
            completed += 1
        
        return gantt_chart
    
    def priority_preemptive(self):
        if not self.processes:
            return []
        
        self.reset_processes()
        current_time = 0
        completed = 0
        n = len(self.processes)
        gantt_chart = []
        current_process = None
        last_time = 0
        
        while completed < n:
            # Get available processes
            available = [p for p in self.processes 
                        if p['arrival_time'] <= current_time and p['remaining_time'] > 0]
            
            if not available:
                if current_process:
                    # End the current process segment
                    gantt_chart.append((current_process['name'], last_time, current_time))
                    current_process = None
                current_time += 1
                continue
            
            # Select process with highest priority (lowest number)
            next_process = min(available, key=lambda x: x['priority'])
            
            if current_process != next_process:
                if current_process is not None and current_process['remaining_time'] > 0:
                    # Add previous process to gantt chart
                    gantt_chart.append((current_process['name'], last_time, current_time))
                
                current_process = next_process
                last_time = current_time
                
                if current_process['first_execution'] == -1:
                    current_process['first_execution'] = current_time
                if current_process['start_time'] == -1:
                    current_process['start_time'] = current_time
            
            # Execute for 1 time unit
            current_time += 1
            current_process['remaining_time'] -= 1
            
            if current_process['remaining_time'] == 0:
                gantt_chart.append((current_process['name'], last_time, current_time))
                current_process['completion_time'] = current_time
                completed += 1
                current_process = None
        
        return gantt_chart
    
    def calculate_metrics(self, gantt_chart):
        if not self.processes:
            return {}
        
        metrics = {}
        total_tat = 0
        total_wt = 0
        total_rt = 0
        count = 0
        
        print(f"\n=== Calculating Metrics for {len(self.processes)} processes ===")
        
        for process in self.processes:
            name = process['name']
            
            # Check if process was completed
            if process.get('completion_time', -1) == -1:
                print(f"❌ Process {name} has no completion time!")
                print(f"   Arrival: {process['arrival_time']}, Burst: {process['burst_time']}")
                print(f"   Remaining: {process['remaining_time']}, First Exec: {process.get('first_execution', 'N/A')}")
                print(f"   Start Time: {process.get('start_time', 'N/A')}")
                continue
            
            completion_time = process['completion_time']
            arrival_time = process['arrival_time']
            burst_time = process['burst_time']
            first_execution = process.get('first_execution', completion_time)
            
            turnaround_time = completion_time - arrival_time
            waiting_time = turnaround_time - burst_time
            response_time = first_execution - arrival_time
            
            # Ensure non-negative values
            waiting_time = max(0, waiting_time)
            response_time = max(0, response_time)
            
            metrics[name] = {
                'arrival_time': arrival_time,
                'burst_time': burst_time,
                'priority': process.get('priority', 0),
                'completion_time': completion_time,
                'turnaround_time': turnaround_time,
                'waiting_time': waiting_time,
                'response_time': response_time
            }
            
            total_tat += turnaround_time
            total_wt += waiting_time
            total_rt += response_time
            count += 1
            
            print(f"✅ {name}: AT={arrival_time}, BT={burst_time}, CT={completion_time}")
            print(f"   First Exec: {first_execution}, TAT={turnaround_time}, WT={waiting_time}, RT={response_time}")
        
        # Calculate averages
        if count > 0:
            metrics['_averages'] = {
                'avg_turnaround_time': total_tat / count,
                'avg_waiting_time': total_wt / count,
                'avg_response_time': total_rt / count
            }
            
            print(f"\n📊 Averages: TAT={metrics['_averages']['avg_turnaround_time']:.2f}, "
                  f"WT={metrics['_averages']['avg_waiting_time']:.2f}, "
                  f"RT={metrics['_averages']['avg_response_time']:.2f}")
        else:
            print("❌ No processes were completed successfully!")
            # Debug all processes
            for i, process in enumerate(self.processes):
                print(f"Process {i}: {process['name']} - "
                      f"arrival={process['arrival_time']}, burst={process['burst_time']}, "
                      f"remaining={process['remaining_time']}, completion={process.get('completion_time', 'Not set')}, "
                      f"first_exec={process.get('first_execution', 'Not set')}")
        
        return metrics