from typing import List, Dict, Tuple
from dataclasses import dataclass, field
from enum import Enum
import copy


class AllocationStatus(Enum):
    """Status of resource allocation request"""
    SAFE = "SAFE"
    UNSAFE = "UNSAFE"
    GRANTED = "GRANTED"
    DENIED = "DENIED"


@dataclass
class Process:
    """Represents a process in the system"""
    pid: int
    max_claim: Dict[str, int] = field(default_factory=dict)
    allocated: Dict[str, int] = field(default_factory=dict)
    needed: Dict[str, int] = field(default_factory=dict)
    
    def calculate_needed(self):
        """Calculate needed resources: Max - Allocated"""
        self.needed = {
            resource: self.max_claim.get(resource, 0) - self.allocated.get(resource, 0)
            for resource in self.max_claim
        }
    
    def can_finish(self, available: Dict[str, int]) -> bool:
        """Check if process can finish with available resources"""
        return all(available.get(r, 0) >= self.needed.get(r, 0) for r in self.needed)
    
    def release_resources(self) -> Dict[str, int]:
        """Release all allocated resources"""
        released = self.allocated.copy()
        self.allocated = {r: 0 for r in self.allocated}
        self.calculate_needed()
        return released


class BankersAlgorithm:
    """Implementation of Banker's Algorithm for deadlock avoidance"""
    
    def __init__(self, resources: Dict[str, int]):
        """
        Initialize the Banker's Algorithm
        
        Args:
            resources: Dictionary of resource types and their total instances
        """
        self.total_resources = resources.copy()
        self.available = resources.copy()
        self.processes: Dict[int, Process] = {}
        self.history: List[Dict] = []
        self.safe_sequence: List[int] = []
    
    def add_process(self, pid: int, max_claim: Dict[str, int]):
        """Add a new process to the system"""
        if pid in self.processes:
            raise ValueError(f"Process {pid} already exists")
        
        process = Process(
            pid=pid,
            max_claim=max_claim.copy(),
            allocated={r: 0 for r in max_claim},
            needed=max_claim.copy()
        )
        self.processes[pid] = process
    
    def remove_process(self, pid: int):
        """Remove a process and release its resources"""
        if pid not in self.processes:
            raise ValueError(f"Process {pid} not found")
        
        process = self.processes[pid]
        released = process.release_resources()
        
        for resource, amount in released.items():
            self.available[resource] = self.available.get(resource, 0) + amount
        
        del self.processes[pid]
    
    def request_resources(self, pid: int, request: Dict[str, int]) -> Tuple[AllocationStatus, str]:
        """
        Handle a resource request using Banker's Algorithm
        
        Args:
            pid: Process ID
            request: Dictionary of requested resources
        
        Returns:
            Tuple of (status, message)
        """
        if pid not in self.processes:
            return AllocationStatus.DENIED, f"Process {pid} not found"
        
        process = self.processes[pid]
        
        # Check if request exceeds need
        for resource, amount in request.items():
            if amount > process.needed.get(resource, 0):
                return AllocationStatus.DENIED, f"Request exceeds need for {resource}"
        
        # Check if request exceeds available
        for resource, amount in request.items():
            if amount > self.available.get(resource, 0):
                return AllocationStatus.DENIED, f"Insufficient {resource} available"
        
        # Tentatively allocate
        old_state = self._save_state()
        
        for resource, amount in request.items():
            process.allocated[resource] = process.allocated.get(resource, 0) + amount
            self.available[resource] = self.available.get(resource, 0) - amount
        
        process.calculate_needed()
        
        # Check if system remains in safe state
        if self.is_safe():
            self.history.append({
                'action': 'allocate',
                'pid': pid,
                'request': request,
                'status': 'granted'
            })
            return AllocationStatus.GRANTED, "Request granted - system remains safe"
        else:
            # Restore previous state
            self._restore_state(old_state)
            return AllocationStatus.DENIED, "Request denied - would lead to unsafe state"
    
    def is_safe(self) -> bool:
        """
        Check if the current system state is safe using Banker's Algorithm
        
        Returns:
            True if safe, False otherwise
        """
        available = self.available.copy()
        work = available.copy()
        finish = {pid: False for pid in self.processes}
        safe_sequence = []
        
        while len(safe_sequence) < len(self.processes):
            found = False
            
            for pid in self.processes:
                if finish[pid]:
                    continue
                
                process = self.processes[pid]
                
                # Check if process can finish
                if process.can_finish(work):
                    # Release resources
                    for resource, amount in process.allocated.items():
                        work[resource] = work.get(resource, 0) + amount
                    
                    finish[pid] = True
                    safe_sequence.append(pid)
                    found = True
                    break
            
            if not found:
                self.safe_sequence = []
                return False
        
        self.safe_sequence = safe_sequence
        return True
    
    def get_safe_sequence(self) -> List[int]:
        """Get the safe sequence if system is safe"""
        if self.is_safe():
            return self.safe_sequence.copy()
        return []
    
    def explore_what_if(self, pid: int, request: Dict[str, int]) -> Dict:
        """
        Explore what would happen if a request is made without actually allocating
        
        Args:
            pid: Process ID
            request: Requested resources
        
        Returns:
            Dictionary with analysis results
        """
        if pid not in self.processes:
            return {'feasible': False, 'reason': f'Process {pid} not found'}
        
        old_state = self._save_state()
        
        try:
            status, message = self.request_resources(pid, request)
            feasible = status == AllocationStatus.GRANTED
            
            if feasible:
                safe_seq = self.get_safe_sequence()
            else:
                safe_seq = []
            
            result = {
                'feasible': feasible,
                'message': message,
                'safe_sequence': safe_seq,
                'would_be_safe': feasible
            }
        finally:
            self._restore_state(old_state)
        
        return result
    
    def release_resources(self, pid: int) -> bool:
        """Release all resources held by a process"""
        if pid not in self.processes:
            return False
        
        process = self.processes[pid]
        released = process.release_resources()
        
        for resource, amount in released.items():
            self.available[resource] = self.available.get(resource, 0) + amount
        
        self.history.append({
            'action': 'release',
            'pid': pid,
            'released': released
        })
        
        return True
    
    def get_system_state(self) -> Dict:
        """Get current system state"""
        return {
            'total_resources': self.total_resources.copy(),
            'available': self.available.copy(),
            'processes': {
                pid: {
                    'max_claim': proc.max_claim.copy(),
                    'allocated': proc.allocated.copy(),
                    'needed': proc.needed.copy()
                }
                for pid, proc in self.processes.items()
            },
            'is_safe': self.is_safe(),
            'safe_sequence': self.get_safe_sequence()
        }
    
    def _save_state(self) -> Dict:
        """Save current system state"""
        return {
            'available': self.available.copy(),
            'processes': copy.deepcopy(self.processes)
        }
    
    def _restore_state(self, state: Dict):
        """Restore system to a previous state"""
        self.available = state['available'].copy()
        self.processes = copy.deepcopy(state['processes'])
