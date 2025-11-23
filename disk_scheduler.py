class DiskScheduler:
    def __init__(self):
        self.requests = []
        self.head_start = 0
    
    def set_requests(self, requests, head_start):
        self.requests = requests.copy()
        self.head_start = head_start
    
    def fcfs(self):
        if not self.requests:
            return []
        
        sequence = [self.head_start] + self.requests
        return sequence
    
    def sstf(self):
        if not self.requests:
            return []
        
        sequence = [self.head_start]
        current_position = self.head_start
        remaining_requests = self.requests.copy()
        
        while remaining_requests:
            # Find closest request
            closest = min(remaining_requests, 
                         key=lambda x: abs(x - current_position))
            sequence.append(closest)
            current_position = closest
            remaining_requests.remove(closest)
        
        return sequence
    
    def scan(self, disk_size=200):
        if not self.requests:
            return []
        
        sequence = [self.head_start]
        current_position = self.head_start
        
        # Separate requests into left and right of current position
        left_requests = [r for r in self.requests if r <= current_position]
        right_requests = [r for r in self.requests if r > current_position]
        
        # Sort left in descending, right in ascending
        left_requests.sort(reverse=True)
        right_requests.sort()
        
        # Go to 0 first if there are left requests
        if left_requests:
            sequence.extend(left_requests)
        
        # Then go to disk_size if there are right requests
        if right_requests:
            sequence.extend(right_requests)
        
        return sequence
    
    def c_scan(self, disk_size=200):
        if not self.requests:
            return []
        
        sequence = [self.head_start]
        current_position = self.head_start
        
        # Separate requests
        left_requests = [r for r in self.requests if r <= current_position]
        right_requests = [r for r in self.requests if r > current_position]
        
        # Sort both in ascending order
        left_requests.sort()
        right_requests.sort()
        
        # Service right requests first
        sequence.extend(right_requests)
        
        # Then jump to beginning and service left requests
        if left_requests:
            sequence.extend(left_requests)
        
        return sequence
    
    def calculate_seek_time(self, sequence):
        if len(sequence) < 2:
            return 0
        
        seek_time = 0
        for i in range(1, len(sequence)):
            seek_time += abs(sequence[i] - sequence[i-1])
        
        return seek_time