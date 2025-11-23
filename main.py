import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cpu_scheduler import CPUScheduler
from disk_scheduler import DiskScheduler
from utils import PlotUtils, InputValidator

class SchedulerVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced CPU and Disk Scheduler Visualizer")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize schedulers
        self.cpu_scheduler = CPUScheduler()
        self.disk_scheduler = DiskScheduler()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # CPU Scheduler Tab
        cpu_frame = ttk.Frame(notebook)
        notebook.add(cpu_frame, text="CPU Scheduler")
        
        # Disk Scheduler Tab
        disk_frame = ttk.Frame(notebook)
        notebook.add(disk_frame, text="Disk Scheduler")
        
        self.setup_cpu_tab(cpu_frame)
        self.setup_disk_tab(disk_frame)
    
    def setup_cpu_tab(self, parent):
        # Main container with left and right panes
        main_paned = ttk.PanedWindow(parent, orient=tk.HORIZONTAL)
        main_paned.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Left frame for inputs
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=1)
        
        # Right frame for visualization
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=2)
        
        # Process input section - Matching your image layout
        input_frame = ttk.LabelFrame(left_frame, text="Process Input", padding=10)
        input_frame.pack(fill='x', padx=5, pady=5)
        
        # Manual input section
        manual_frame = ttk.Frame(input_frame)
        manual_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(manual_frame, text="Add Process:", 
                 font=('Arial', 9, 'bold')).grid(row=0, column=0, columnspan=5, sticky='w', pady=(0, 5))
        
        # Input labels
        ttk.Label(manual_frame, text="Name", width=8).grid(row=1, column=0, padx=2)
        ttk.Label(manual_frame, text="Arrival", width=8).grid(row=1, column=1, padx=2)
        ttk.Label(manual_frame, text="Burst", width=8).grid(row=1, column=2, padx=2)
        ttk.Label(manual_frame, text="Priority", width=8).grid(row=1, column=3, padx=2)
        ttk.Label(manual_frame, text="Action", width=8).grid(row=1, column=4, padx=2)
        
        # Input fields
        self.process_name_var = tk.StringVar(value="P1")
        self.arrival_var = tk.StringVar(value="0")
        self.burst_var = tk.StringVar(value="5")
        self.priority_var = tk.StringVar(value="0")
        
        name_entry = ttk.Entry(manual_frame, textvariable=self.process_name_var, width=8)
        name_entry.grid(row=2, column=0, padx=2, pady=2)
        
        arrival_entry = ttk.Entry(manual_frame, textvariable=self.arrival_var, width=8)
        arrival_entry.grid(row=2, column=1, padx=2, pady=2)
        
        burst_entry = ttk.Entry(manual_frame, textvariable=self.burst_var, width=8)
        burst_entry.grid(row=2, column=2, padx=2, pady=2)
        
        priority_entry = ttk.Entry(manual_frame, textvariable=self.priority_var, width=8)
        priority_entry.grid(row=2, column=3, padx=2, pady=2)
        
        ttk.Button(manual_frame, text="Add", 
                  command=self.add_process_manual, width=8).grid(row=2, column=4, padx=2, pady=2)
        
        # Process list section
        list_frame = ttk.Frame(input_frame)
        list_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(list_frame, text="Current Processes:", 
                 font=('Arial', 9, 'bold')).pack(anchor='w', pady=(0, 5))
        
        # Treeview for processes with exact column names from your image
        tree_frame = ttk.Frame(list_frame)
        tree_frame.pack(fill='x')
        
        # Create treeview with your specified column names
        self.process_tree = ttk.Treeview(tree_frame, columns=('Name', 'Arrival', 'Burst', 'Priority'), 
                                        show='headings', height=6)
        
        # Set column headings exactly as in your image
        self.process_tree.heading('Name', text='Name')
        self.process_tree.heading('Arrival', text='Arrival')
        self.process_tree.heading('Burst', text='Burst') 
        self.process_tree.heading('Priority', text='Priority')
        
        self.process_tree.column('Name', width=60)
        self.process_tree.column('Arrival', width=60)
        self.process_tree.column('Burst', width=60)
        self.process_tree.column('Priority', width=60)
        
        self.process_tree.pack(fill='x', side='left')
        
        # Add scrollbar for process tree
        tree_scroll = ttk.Scrollbar(tree_frame, orient='vertical', command=self.process_tree.yview)
        tree_scroll.pack(side='right', fill='y')
        self.process_tree.configure(yscrollcommand=tree_scroll.set)
        
        # Process controls - matching your image layout
        control_frame = ttk.Frame(input_frame)
        control_frame.pack(fill='x', pady=5)
        
        ttk.Button(control_frame, text="Clear All", 
                  command=self.clear_all_processes).pack(side='left', padx=2)
        ttk.Button(control_frame, text="Remove Selected", 
                  command=self.remove_selected_process).pack(side='left', padx=2)
        
        # Quick import section - matching your image
        import_frame = ttk.LabelFrame(input_frame, text="Quick Import", padding=5)
        import_frame.pack(fill='x', pady=(10, 5))
        
        ttk.Label(import_frame, text="Format: Name Arrival Burst [Priority]", 
                 font=('Arial', 8)).pack(anchor='w')
        
        # Sample processes from your image
        sample_processes = "P1 0 11 0\nP2 1 5 0\nP3 2 12 0"
        
        self.quick_import_text = scrolledtext.ScrolledText(import_frame, height=4, width=30)
        self.quick_import_text.pack(fill='x', pady=5)
        self.quick_import_text.insert('1.0', sample_processes)
        
        ttk.Button(import_frame, text="Import Processes", 
                  command=self.import_processes).pack(pady=5)
        
        # Algorithm selection - matching your image layout
        algo_frame = ttk.LabelFrame(left_frame, text="Scheduling Algorithm", padding=10)
        algo_frame.pack(fill='x', padx=5, pady=5)
        
        self.cpu_algorithm = tk.StringVar(value="FCFS")
        
        # Algorithms matching your image
        algorithms = [
            ("First Come First Serve (FCFS)", "FCFS"),
            ("Shortest Job First (SJF)", "SJF"),
            ("Shortest Remaining Time First (SRTF)", "SRTF"),
            ("Round Robin", "RR"),
            ("Priority Scheduling (Non-Preemptive)", "PRIORITY"),
            ("Priority Scheduling (Preemptive)", "PRIORITY_P")
        ]
        
        for text, value in algorithms:
            ttk.Radiobutton(algo_frame, text=text, variable=self.cpu_algorithm, 
                           value=value).pack(anchor='w', pady=2)
        
        # Time quantum for RR
        quantum_frame = ttk.Frame(algo_frame)
        quantum_frame.pack(fill='x', pady=5)
        
        ttk.Label(quantum_frame, text="Time Quantum:").pack(side='left')
        self.quantum_var = tk.StringVar(value="2")
        quantum_entry = ttk.Entry(quantum_frame, textvariable=self.quantum_var, width=5)
        quantum_entry.pack(side='left', padx=5)
        
        # Execute button
        ttk.Button(algo_frame, text="Run CPU Scheduling", 
                  command=self.run_cpu_scheduling, style='Accent.TButton').pack(pady=10)
        
        # Right frame content - Gantt Chart
        chart_frame = ttk.LabelFrame(right_frame, text="Gantt Chart", padding=10)
        chart_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.cpu_fig, self.cpu_ax = PlotUtils.create_figure(chart_frame, 12, 6)
        self.cpu_canvas = FigureCanvasTkAgg(self.cpu_fig, chart_frame)
        self.cpu_canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Metrics section
        metrics_frame = ttk.LabelFrame(right_frame, text="Performance Metrics", padding=10)
        metrics_frame.pack(fill='x', padx=5, pady=5)
        
        # Metrics table
        self.metrics_tree = ttk.Treeview(metrics_frame, 
                                        columns=('Process', 'Arrival', 'Burst', 'Priority', 'Completion', 'TAT', 'WT', 'RT'), 
                                        show='headings', height=6)
        
        columns = [
            ('Process', 80), 
            ('Arrival', 70), 
            ('Burst', 70), 
            ('Priority', 70),
            ('Completion', 90), 
            ('TAT', 80), 
            ('WT', 80), 
            ('RT', 80)
        ]
        
        # Configure column headings and alignment
        for col, width in columns:
            self.metrics_tree.heading(col, text=col)
            self.metrics_tree.column(col, width=width, anchor='center')  # Center alignment
        
        self.metrics_tree.pack(fill='x', pady=5)

        # Average metrics
        self.avg_label = ttk.Label(metrics_frame, text="", font=('Arial', 9, 'bold'))
        self.avg_label.pack(anchor='center', pady=5)  # Center aligned average label

        # Add the sample processes automatically
        self.import_sample_processes()
    
    def import_sample_processes(self):
        """Add the sample processes from the image automatically"""
        sample_processes = [
            ("P1", 0, 11, 0),
            ("P2", 1, 5, 0), 
            ("P3", 2, 12, 0)
        ]
        
        for name, arrival, burst, priority in sample_processes:
            self.process_tree.insert('', 'end', values=(name, arrival, burst, priority))
    
    def setup_disk_tab(self, parent):
        # Left frame for inputs
        left_frame = ttk.Frame(parent)
        left_frame.pack(side='left', fill='y', padx=10, pady=10)
        
        # Disk requests input
        ttk.Label(left_frame, text="Disk Requests:", 
                 font=('Arial', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        
        requests_help = ttk.Label(left_frame, 
                                 text="Enter numbers separated by spaces",
                                 font=('Arial', 8), foreground='gray')
        requests_help.pack(anchor='w', pady=(0, 5))
        
        self.requests_entry = ttk.Entry(left_frame, width=30)
        self.requests_entry.pack(fill='x', pady=(0, 10))
        self.requests_entry.insert(0, "98 183 37 122 14 124 65 67")
        
        # Head start position
        ttk.Label(left_frame, text="Head Start Position:", 
                 font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10, 5))
        
        self.head_start_var = tk.StringVar(value="53")
        head_start_entry = ttk.Entry(left_frame, textvariable=self.head_start_var, width=10)
        head_start_entry.pack(anchor='w', pady=(0, 10))
        
        # Algorithm selection
        ttk.Label(left_frame, text="Disk Scheduling Algorithm:", 
                 font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10, 5))
        
        self.disk_algorithm = tk.StringVar(value="FCFS")
        algorithms = [("FCFS", "FCFS"), ("SSTF", "SSTF"), ("SCAN", "SCAN"), ("C-SCAN", "CSCAN")]
        
        for text, value in algorithms:
            ttk.Radiobutton(left_frame, text=text, variable=self.disk_algorithm, 
                           value=value).pack(anchor='w')
        
        # Execute button
        ttk.Button(left_frame, text="Run Disk Scheduling", 
                  command=self.run_disk_scheduling).pack(pady=10)
        
        # Results
        ttk.Label(left_frame, text="Results:", 
                 font=('Arial', 10, 'bold')).pack(anchor='w', pady=(20, 5))
        
        self.disk_results = scrolledtext.ScrolledText(left_frame, width=30, height=8)
        self.disk_results.pack(fill='both', expand=True)
        
        # Right frame for visualization
        right_frame = ttk.Frame(parent)
        right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(right_frame, text="Disk Head Movement", 
                 font=('Arial', 12, 'bold')).pack(anchor='w')
        
        self.disk_fig, self.disk_ax = PlotUtils.create_figure(right_frame, 10, 6)
        self.disk_canvas = FigureCanvasTkAgg(self.disk_fig, right_frame)
        self.disk_canvas.get_tk_widget().pack(fill='both', expand=True, pady=10)
    
    def add_process_manual(self):
        try:
            name = self.process_name_var.get().strip()
            arrival = int(self.arrival_var.get())
            burst = int(self.burst_var.get())
            priority = int(self.priority_var.get())
            
            if burst <= 0:
                messagebox.showerror("Error", "Burst time must be positive!")
                return
            
            # Add to treeview
            self.process_tree.insert('', 'end', values=(name, arrival, burst, priority))
            
            # Auto-increment process name
            if name.startswith('P') and name[1:].isdigit():
                next_num = int(name[1:]) + 1
                self.process_name_var.set(f"P{next_num}")
            
            # Reset other fields
            self.arrival_var.set(str(arrival + 1))
            self.burst_var.set("5")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for arrival, burst and priority!")
    
    def remove_selected_process(self):
        selected = self.process_tree.selection()
        if selected:
            self.process_tree.delete(selected)
    
    def clear_all_processes(self):
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)
    
    def import_processes(self):
        try:
            text = self.quick_import_text.get("1.0", tk.END).strip()
            lines = text.split('\n')
            
            count = 0
            for line in lines:
                if line.strip():
                    parts = line.strip().split()
                    if len(parts) >= 3:
                        name = parts[0]
                        arrival = int(parts[1])
                        burst = int(parts[2])
                        priority = int(parts[3]) if len(parts) > 3 else 0
                        
                        self.process_tree.insert('', 'end', 
                                               values=(name, arrival, burst, priority))
                        count += 1
            
            messagebox.showinfo("Success", f"Imported {count} processes!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Invalid import format: {str(e)}")
    
    def run_cpu_scheduling(self):
        try:
            # Get processes from treeview
            processes = []
            for item in self.process_tree.get_children():
                values = self.process_tree.item(item)['values']
                if len(values) >= 4:
                    name, arrival, burst, priority = values
                    processes.append((name, int(arrival), int(burst), int(priority)))
            
            if not processes:
                messagebox.showerror("Error", "No processes added!")
                return
            
            # Clear previous data
            self.cpu_scheduler.processes.clear()
            
            # Add processes
            for name, arrival, burst, priority in processes:
                self.cpu_scheduler.add_process(name, arrival, burst, priority)
            
            # Run selected algorithm
            algorithm = self.cpu_algorithm.get()
            print(f"\n🎯 Running {algorithm} algorithm...")
            
            if algorithm == "FCFS":
                gantt_chart = self.cpu_scheduler.fcfs()
                title = "First Come First Serve (FCFS)"
            elif algorithm == "SJF":
                gantt_chart = self.cpu_scheduler.sjf()
                title = "Shortest Job First (SJF) - Non-Preemptive"
            elif algorithm == "SRTF":
                gantt_chart = self.cpu_scheduler.srtf()
                title = "Shortest Remaining Time First (SRTF) - Preemptive"
            elif algorithm == "RR":
                try:
                    quantum = int(self.quantum_var.get())
                    gantt_chart = self.cpu_scheduler.round_robin(quantum)
                    title = f"Round Robin (Quantum={quantum})"
                except ValueError:
                    messagebox.showerror("Error", "Invalid time quantum!")
                    return
            elif algorithm == "PRIORITY":
                gantt_chart = self.cpu_scheduler.priority_scheduling()
                title = "Priority Scheduling - Non-Preemptive"
            elif algorithm == "PRIORITY_P":
                gantt_chart = self.cpu_scheduler.priority_preemptive()
                title = "Priority Scheduling - Preemptive"
            
            print(f"📈 Gantt chart has {len(gantt_chart)} entries")
            
            # Update visualization with consistent colors
            PlotUtils.draw_cpu_gantt(self.cpu_ax, gantt_chart, title)
            self.cpu_canvas.draw()
            
            # Calculate and display metrics
            print("📊 Calculating metrics...")
            metrics = self.cpu_scheduler.calculate_metrics(gantt_chart)
            self.update_metrics_table(metrics)
            
        except Exception as e:
            print(f"❌ Error in run_cpu_scheduling: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    
    def update_metrics_table(self, metrics):
        # Clear existing data
        for item in self.metrics_tree.get_children():
            self.metrics_tree.delete(item)
        
        # Add new data with center-aligned values
        total_tat = 0
        total_wt = 0
        total_rt = 0
        count = 0
        
        print(f"📋 Updating metrics table with {len(metrics)} entries")
        
        for process, data in metrics.items():
            if process == '_averages':
                continue
                
            try:
                arrival = int(data['arrival_time'])
                burst = int(data['burst_time'])
                completion = int(data['completion_time'])
                tat = int(data['turnaround_time'])
                wt = int(data['waiting_time'])
                rt = int(data.get('response_time', 0))
                priority = int(data.get('priority', 0))
                
                # Insert with center-aligned values
                item_id = self.metrics_tree.insert('', 'end', values=(
                    process,
                    arrival,
                    burst,
                    priority,
                    completion,
                    tat,
                    wt,
                    rt
                ))
                
                # Optional: You can also set tags for specific styling
                # This ensures all cells in this row are center-aligned
                self.metrics_tree.set(item_id, 'Process', process)
                self.metrics_tree.set(item_id, 'Arrival', arrival)
                self.metrics_tree.set(item_id, 'Burst', burst)
                self.metrics_tree.set(item_id, 'Priority', priority)
                self.metrics_tree.set(item_id, 'Completion', completion)
                self.metrics_tree.set(item_id, 'TAT', tat)
                self.metrics_tree.set(item_id, 'WT', wt)
                self.metrics_tree.set(item_id, 'RT', rt)
                
                total_tat += tat
                total_wt += wt
                total_rt += rt
                count += 1
                
                print(f"✅ Added {process} to metrics table")
                
            except (ValueError, KeyError) as e:
                print(f"❌ Error processing metrics for {process}: {e}")
                print(f"   Data: {data}")
                continue
        
        # Update average label (center aligned)
        if count > 0:
            avg_tat = total_tat / count
            avg_wt = total_wt / count
            avg_rt = total_rt / count
            
            avg_text = f"Average Turnaround Time: {avg_tat:.2f} | "
            avg_text += f"Average Waiting Time: {avg_wt:.2f} | "
            avg_text += f"Average Response Time: {avg_rt:.2f}"
            
            self.avg_label.config(text=avg_text)
            print(f"📊 Averages calculated: TAT={avg_tat:.2f}, WT={avg_wt:.2f}, RT={avg_rt:.2f}")
        else:
            self.avg_label.config(text="No metrics calculated - check console for errors")
            print("❌ No metrics were calculated!")
            
        # Force update the display
        self.metrics_tree.update_idletasks()
        print("✅ Metrics table updated successfully")

    
    def run_disk_scheduling(self):
        try:
            # Parse input
            requests_text = self.requests_entry.get()
            head_start_text = self.head_start_var.get()
            
            requests, head_start = InputValidator.validate_disk_input(requests_text, head_start_text)
            
            if requests is None:
                messagebox.showerror("Error", "Invalid disk input!")
                return
            
            # Set requests
            self.disk_scheduler.set_requests(requests, head_start)
            
            # Run selected algorithm
            algorithm = self.disk_algorithm.get()
            
            if algorithm == "FCFS":
                sequence = self.disk_scheduler.fcfs()
                title = "FCFS Disk Scheduling"
            elif algorithm == "SSTF":
                sequence = self.disk_scheduler.sstf()
                title = "SSTF Disk Scheduling"
            elif algorithm == "SCAN":
                sequence = self.disk_scheduler.scan()
                title = "SCAN Disk Scheduling"
            elif algorithm == "CSCAN":
                sequence = self.disk_scheduler.c_scan()
                title = "C-SCAN Disk Scheduling"
            
            # Calculate seek time
            seek_time = self.disk_scheduler.calculate_seek_time(sequence)
            
            # Update visualization
            PlotUtils.draw_disk_sequence(self.disk_ax, sequence[1:], head_start, title)
            self.disk_canvas.draw()
            
            # Update results text
            results_text = f"Algorithm: {title}\n"
            results_text += f"Sequence: {' -> '.join(map(str, sequence))}\n"
            results_text += f"Total Seek Time: {seek_time}\n"
            results_text += f"Total Requests: {len(requests)}\n"
            
            self.disk_results.delete("1.0", tk.END)
            self.disk_results.insert("1.0", results_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    app = SchedulerVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()