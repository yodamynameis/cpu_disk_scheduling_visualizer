import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import hashlib

class PlotUtils:
    @staticmethod
    def get_process_color(process_name):
        """Generate consistent color for each process based on its name"""
        # Create a color map based on process name hash
        color_map = {
            'P1': '#1f77b4',  # blue
            'P2': '#ff7f0e',  # orange
            'P3': '#2ca02c',  # green
            'P4': '#d62728',  # red
            'P5': '#9467bd',  # purple
            'P6': '#8c564b',  # brown
            'P7': '#e377c2',  # pink
            'P8': '#7f7f7f',  # gray
            'P9': '#bcbd22',  # yellow-green
            'P10': '#17becf', # cyan
            'A': '#1f77b4',
            'B': '#ff7f0e', 
            'C': '#2ca02c',
            'D': '#d62728',
            'E': '#9467bd',
            'F': '#8c564b',
            'G': '#e377c2',
            'H': '#7f7f7f',
            'I': '#bcbd22',
            'J': '#17becf'
        }
        
        if process_name in color_map:
            return color_map[process_name]
        else:
            # Generate consistent color for custom process names
            hash_obj = hashlib.md5(process_name.encode())
            hash_num = int(hash_obj.hexdigest()[:8], 16)
            return f'#{hash_num % 0xffffff:06x}'
    
    @staticmethod
    def create_figure(parent, width=8, height=4):
        fig, ax = plt.subplots(figsize=(width, height))
        fig.patch.set_facecolor('#f0f0f0')
        ax.set_facecolor('#fafafa')
        return fig, ax
    
    @staticmethod
    def draw_cpu_gantt(ax, processes, title="CPU Scheduling Gantt Chart"):
        ax.clear()
        
        if not processes:
            ax.text(0.5, 0.5, 'No processes to display', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=12)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_title(title)
            return
        
        # Create multiple rows for better visualization
        process_rows = {}
        current_row = 0
        
        for i, (name, start, end) in enumerate(processes):
            if name not in process_rows:
                process_rows[name] = current_row
                current_row += 1
        
        # Calculate bar height based on number of processes
        bar_height = 0.6 / max(1, len(process_rows))
        
        # Create a set to track which processes we've already added to legend
        legend_added = set()
        legend_handles = []
        legend_labels = []
        
        for i, (name, start, end) in enumerate(processes):
            row = process_rows[name]
            color = PlotUtils.get_process_color(name)
            
            # Draw the main bar
            bar = ax.barh(row, end-start, left=start, height=bar_height, color=color, 
                         edgecolor='black', alpha=0.8)
            
            # Add process name in the middle of the bar
            ax.text((start + end)/2, row, name, ha='center', va='center', 
                   fontweight='bold', fontsize=9, color='white')
            
            # Add time labels
            ax.text(start, row + bar_height/2 + 0.1, f'{start}', 
                   ha='center', va='bottom', fontsize=8)
            ax.text(end, row + bar_height/2 + 0.1, f'{end}', 
                   ha='center', va='bottom', fontsize=8)
            
            # Add to legend if not already added
            if name not in legend_added:
                legend_handles.append(bar[0])
                legend_labels.append(name)
                legend_added.add(name)
        
        ax.set_xlabel('Time')
        ax.set_ylabel('Processes')
        ax.set_yticks(list(process_rows.values()))
        ax.set_yticklabels(list(process_rows.keys()))
        ax.set_title(title)
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add legend with all processes
        if legend_handles:
            ax.legend(legend_handles, legend_labels, 
                     bbox_to_anchor=(1.05, 1), loc='upper left',
                     title="Processes")
    
    @staticmethod
    def draw_disk_sequence(ax, requests, head_start, title="Disk Scheduling"):
        ax.clear()
        
        if not requests:
            ax.text(0.5, 0.5, 'No disk requests to display', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=12)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_title(title)
            return
            
        # Plot head movement
        x_points = list(range(len(requests) + 1))
        y_points = [head_start] + requests
        
        ax.plot(x_points, y_points, 'bo-', linewidth=2, 
               markersize=8, label='Head Movement', alpha=0.7)
        
        # Mark start and end points
        ax.plot(0, head_start, 'go', markersize=10, label=f'Start ({head_start})')
        ax.plot(len(requests), requests[-1], 'ro', markersize=10, 
               label=f'End ({requests[-1]})')
        
        ax.set_xlabel('Step')
        ax.set_ylabel('Cylinder Number')
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Add step numbers and values
        for i, (x, y) in enumerate(zip(x_points, y_points)):
            ax.annotate(f'{y}', (x, y), textcoords="offset points", 
                       xytext=(0,10), ha='center', fontsize=8)
            ax.annotate(f'Step {i}', (x, y), textcoords="offset points", 
                       xytext=(0,-15), ha='center', fontsize=7, color='gray')

class InputValidator:
    @staticmethod
    def validate_process_input(processes_str):
        try:
            processes = []
            for line in processes_str.strip().split('\n'):
                if line.strip():
                    parts = line.strip().split()
                    if len(parts) >= 3:
                        name = parts[0]
                        arrival = int(parts[1])
                        burst = int(parts[2])
                        priority = int(parts[3]) if len(parts) > 3 else 0
                        processes.append((name, arrival, burst, priority))
            return processes
        except Exception as e:
            print(f"Error validating process input: {e}")
            return None
    
    @staticmethod
    def validate_disk_input(requests_str, head_start_str):
        try:
            requests = [int(x) for x in requests_str.strip().split()]
            head_start = int(head_start_str)
            return requests, head_start
        except Exception as e:
            print(f"Error validating disk input: {e}")
            return None, None