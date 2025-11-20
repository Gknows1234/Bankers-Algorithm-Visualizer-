"""
Advanced visualization utilities for Banker's Algorithm
Includes resource allocation graphs and state diagrams
"""

from typing import Dict, List, Tuple
from bankers_algorithm import BankersAlgorithm


class ResourceAllocationGraph:
    """Generate resource allocation graph data"""
    
    def __init__(self, banker: BankersAlgorithm):
        self.banker = banker
    
    def get_allocation_matrix(self) -> Dict[str, List[int]]:
        """Get allocation matrix for visualization"""
        state = self.banker.get_system_state()
        resources = list(state['total_resources'].keys())
        
        matrix = {}
        for pid in sorted(state['processes'].keys()):
            proc = state['processes'][pid]
            matrix[f"P{pid}"] = [proc['allocated'].get(r, 0) for r in resources]
        
        return matrix
    
    def get_need_matrix(self) -> Dict[str, List[int]]:
        """Get need matrix for visualization"""
        state = self.banker.get_system_state()
        resources = list(state['total_resources'].keys())
        
        matrix = {}
        for pid in sorted(state['processes'].keys()):
            proc = state['processes'][pid]
            matrix[f"P{pid}"] = [proc['needed'].get(r, 0) for r in resources]
        
        return matrix
    
    def get_resource_utilization(self) -> Dict[str, Tuple[int, int]]:
        """Get resource utilization (used, total) for each resource"""
        state = self.banker.get_system_state()
        
        utilization = {}
        for resource, total in state['total_resources'].items():
            used = total - state['available'].get(resource, 0)
            utilization[resource] = (used, total)
        
        return utilization
    
    def get_process_status(self) -> Dict[str, Dict]:
        """Get detailed status for each process"""
        state = self.banker.get_system_state()
        
        status = {}
        for pid, proc in state['processes'].items():
            total_allocated = sum(proc['allocated'].values())
            total_needed = sum(proc['needed'].values())
            total_max = sum(proc['max_claim'].values())
            
            status[f"P{pid}"] = {
                'allocated': total_allocated,
                'needed': total_needed,
                'max': total_max,
                'progress': (total_allocated / total_max * 100) if total_max > 0 else 0
            }
        
        return status
    
    def generate_ascii_graph(self) -> str:
        """Generate ASCII representation of resource allocation"""
        state = self.banker.get_system_state()
        resources = list(state['total_resources'].keys())
        
        output = "\n" + "="*70 + "\n"
        output += "RESOURCE ALLOCATION GRAPH\n"
        output += "="*70 + "\n\n"
        
        # Header
        output += f"{'Resource':<15} {'Available':<12} {'Allocated':<12} {'Total':<12} {'Usage %':<10}\n"
        output += "-"*70 + "\n"
        
        # Resource rows
        for resource in resources:
            total = state['total_resources'].get(resource, 0)
            available = state['available'].get(resource, 0)
            allocated = total - available
            usage_pct = (allocated / total * 100) if total > 0 else 0
            
            # Visual bar
            bar_length = 20
            filled = int(bar_length * usage_pct / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            
            output += f"{resource:<15} {available:<12} {allocated:<12} {total:<12} {usage_pct:>6.1f}%\n"
            output += f"{'':15} [{bar}]\n"
        
        output += "\n"
        return output
    
    def generate_process_table(self) -> str:
        """Generate ASCII table of process states"""
        state = self.banker.get_system_state()
        resources = list(state['total_resources'].keys())
        
        output = "\n" + "="*70 + "\n"
        output += "PROCESS STATE TABLE\n"
        output += "="*70 + "\n\n"
        
        # Header
        header = f"{'PID':<5} {'Status':<10}"
        for res in resources:
            header += f" {res:<8}"
        output += header + "\n"
        output += "-"*70 + "\n"
        
        # Process rows - Allocated
        output += "ALLOCATED:\n"
        for pid in sorted(state['processes'].keys()):
            proc = state['processes'][pid]
            row = f"P{pid:<4} {'':10}"
            for res in resources:
                row += f" {proc['allocated'].get(res, 0):<8}"
            output += row + "\n"
        
        output += "\n"
        
        # Process rows - Needed
        output += "NEEDED:\n"
        for pid in sorted(state['processes'].keys()):
            proc = state['processes'][pid]
            row = f"P{pid:<4} {'':10}"
            for res in resources:
                row += f" {proc['needed'].get(res, 0):<8}"
            output += row + "\n"
        
        output += "\n"
        
        # Process rows - Max Claim
        output += "MAX CLAIM:\n"
        for pid in sorted(state['processes'].keys()):
            proc = state['processes'][pid]
            row = f"P{pid:<4} {'':10}"
            for res in resources:
                row += f" {proc['max_claim'].get(res, 0):<8}"
            output += row + "\n"
        
        output += "\n"
        return output
    
    def generate_safety_report(self) -> str:
        """Generate detailed safety analysis report"""
        state = self.banker.get_system_state()
        
        output = "\n" + "="*70 + "\n"
        output += "SAFETY ANALYSIS REPORT\n"
        output += "="*70 + "\n\n"
        
        if state['is_safe']:
            output += "✓ SYSTEM IS SAFE\n\n"
            output += "Safe Execution Sequence:\n"
            for i, pid in enumerate(state['safe_sequence'], 1):
                output += f"  {i}. Process {pid}\n"
        else:
            output += "✗ SYSTEM IS UNSAFE\n\n"
            output += "No safe sequence exists. Deadlock is possible.\n"
        
        output += "\n"
        return output
    
    def generate_full_report(self) -> str:
        """Generate complete system report"""
        report = "\n" + "█"*70 + "\n"
        report += "█" + "BANKER'S ALGORITHM SYSTEM REPORT".center(68) + "█\n"
        report += "█"*70 + "\n"
        
        report += self.generate_resource_graph()
        report += self.generate_process_table()
        report += self.generate_safety_report()
        
        return report
    
    def generate_resource_graph(self) -> str:
        """Alias for generate_ascii_graph"""
        return self.generate_ascii_graph()


class StateTransitionAnalyzer:
    """Analyze state transitions and deadlock potential"""
    
    def __init__(self, banker: BankersAlgorithm):
        self.banker = banker
    
    def analyze_request(self, pid: int, request: Dict[str, int]) -> Dict:
        """Analyze impact of a resource request"""
        state = self.banker.get_system_state()
        
        if pid not in state['processes']:
            return {'valid': False, 'reason': f'Process {pid} not found'}
        
        proc = state['processes'][pid]
        analysis = {
            'valid': True,
            'pid': pid,
            'request': request,
            'checks': {}
        }
        
        # Check 1: Request doesn't exceed need
        exceeds_need = False
        for res, amount in request.items():
            if amount > proc['needed'].get(res, 0):
                exceeds_need = True
                break
        analysis['checks']['exceeds_need'] = exceeds_need
        
        # Check 2: Request doesn't exceed available
        exceeds_available = False
        for res, amount in request.items():
            if amount > state['available'].get(res, 0):
                exceeds_available = True
                break
        analysis['checks']['exceeds_available'] = exceeds_available
        
        # Check 3: Would allocation be safe?
        result = self.banker.explore_what_if(pid, request)
        analysis['checks']['would_be_safe'] = result['feasible']
        analysis['safe_sequence'] = result['safe_sequence']
        
        return analysis
    
    def get_deadlock_risk(self) -> float:
        """Estimate deadlock risk (0.0 to 1.0)"""
        state = self.banker.get_system_state()
        
        if not state['processes']:
            return 0.0
        
        total_needed = sum(
            sum(proc['needed'].values()) 
            for proc in state['processes'].values()
        )
        total_available = sum(state['available'].values())
        
        if total_needed == 0:
            return 0.0
        
        # Risk increases as needed resources approach available
        risk = min(1.0, total_needed / (total_needed + total_available))
        
        return risk
    
    def get_system_health(self) -> Dict:
        """Get overall system health metrics"""
        state = self.banker.get_system_state()
        
        health = {
            'is_safe': state['is_safe'],
            'deadlock_risk': self.get_deadlock_risk(),
            'num_processes': len(state['processes']),
            'resource_utilization': {}
        }
        
        for resource, total in state['total_resources'].items():
            used = total - state['available'].get(resource, 0)
            utilization = (used / total * 100) if total > 0 else 0
            health['resource_utilization'][resource] = utilization
        
        return health


def print_full_report(banker: BankersAlgorithm):
    """Print complete system report to console"""
    graph = ResourceAllocationGraph(banker)
    print(graph.generate_full_report())


def print_health_check(banker: BankersAlgorithm):
    """Print system health check"""
    analyzer = StateTransitionAnalyzer(banker)
    health = analyzer.get_system_health()
    
    print("\n" + "="*70)
    print("SYSTEM HEALTH CHECK")
    print("="*70)
    print(f"Safe: {'✓ Yes' if health['is_safe'] else '✗ No'}")
    print(f"Deadlock Risk: {health['deadlock_risk']*100:.1f}%")
    print(f"Active Processes: {health['num_processes']}")
    print("\nResource Utilization:")
    for resource, util in health['resource_utilization'].items():
        bar = "█" * int(util / 5) + "░" * (20 - int(util / 5))
        print(f"  {resource:<15} [{bar}] {util:>6.1f}%")
    print()
