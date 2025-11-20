"""
Demo script showcasing Banker's Algorithm functionality
Run this to see the algorithm in action without GUI
"""

from bankers_algorithm import BankersAlgorithm, AllocationStatus


def print_state(banker, title="System State"):
    """Pretty print system state"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    
    state = banker.get_system_state()
    
    print(f"\nTotal Resources: {state['total_resources']}")
    print(f"Available: {state['available']}")
    print(f"System Status: {'SAFE ✓' if state['is_safe'] else 'UNSAFE ✗'}")
    
    print(f"\n{'PID':<5} {'Max Claim':<20} {'Allocated':<20} {'Needed':<20}")
    print("-" * 65)
    
    for pid, proc in state['processes'].items():
        print(f"{pid:<5} {str(proc['max_claim']):<20} {str(proc['allocated']):<20} {str(proc['needed']):<20}")
    
    if state['safe_sequence']:
        print(f"\nSafe Sequence: {' → '.join(map(str, state['safe_sequence']))}")
    else:
        print("\nNo safe sequence found!")


def demo_basic():
    """Demo 1: Basic allocation and safety check"""
    print("\n" + "="*60)
    print("DEMO 1: Basic Resource Allocation")
    print("="*60)
    
    # Initialize system
    resources = {'CPU': 10, 'Memory': 20, 'Disk': 15}
    banker = BankersAlgorithm(resources)
    
    print("\nInitializing system with resources:")
    print(f"  CPU: 10, Memory: 20, Disk: 15")
    
    # Add processes
    banker.add_process(0, {'CPU': 7, 'Memory': 5, 'Disk': 3})
    banker.add_process(1, {'CPU': 3, 'Memory': 2, 'Disk': 2})
    banker.add_process(2, {'CPU': 9, 'Memory': 0, 'Disk': 2})
    
    print("\nAdded 3 processes with max claims:")
    print("  P0: (7, 5, 3)")
    print("  P1: (3, 2, 2)")
    print("  P2: (9, 0, 2)")
    
    print_state(banker, "Initial State")
    
    # Request resources
    print("\n" + "-"*60)
    print("P0 requests (0, 1, 0)...")
    status, msg = banker.request_resources(0, {'CPU': 0, 'Memory': 1, 'Disk': 0})
    print(f"Result: {status.value} - {msg}")
    print_state(banker)
    
    print("\n" + "-"*60)
    print("P1 requests (2, 0, 1)...")
    status, msg = banker.request_resources(1, {'CPU': 2, 'Memory': 0, 'Disk': 1})
    print(f"Result: {status.value} - {msg}")
    print_state(banker)
    
    print("\n" + "-"*60)
    print("P2 requests (3, 0, 2)...")
    status, msg = banker.request_resources(2, {'CPU': 3, 'Memory': 0, 'Disk': 2})
    print(f"Result: {status.value} - {msg}")
    if status == AllocationStatus.DENIED:
        print("(This would make the system unsafe)")
    print_state(banker)


def demo_what_if():
    """Demo 2: What-if exploration"""
    print("\n" + "="*60)
    print("DEMO 2: What-If Scenario Exploration")
    print("="*60)
    
    resources = {'CPU': 10, 'Memory': 20}
    banker = BankersAlgorithm(resources)
    
    banker.add_process(0, {'CPU': 5, 'Memory': 10})
    banker.add_process(1, {'CPU': 4, 'Memory': 7})
    
    print("\nSystem with 2 processes:")
    print("  P0: Max (5, 10)")
    print("  P1: Max (4, 7)")
    print_state(banker, "Initial State")
    
    # Allocate some resources
    banker.request_resources(0, {'CPU': 2, 'Memory': 3})
    banker.request_resources(1, {'CPU': 1, 'Memory': 2})
    
    print_state(banker, "After Initial Allocations")
    
    # What-if analysis
    print("\n" + "-"*60)
    print("What-if: P0 requests (2, 5)?")
    result = banker.explore_what_if(0, {'CPU': 2, 'Memory': 5})
    print(f"Feasible: {result['feasible']}")
    print(f"Message: {result['message']}")
    if result['safe_sequence']:
        print(f"Safe Sequence: {' → '.join(map(str, result['safe_sequence']))}")
    
    print("\n" + "-"*60)
    print("What-if: P1 requests (2, 4)?")
    result = banker.explore_what_if(1, {'CPU': 2, 'Memory': 4})
    print(f"Feasible: {result['feasible']}")
    print(f"Message: {result['message']}")
    if result['safe_sequence']:
        print(f"Safe Sequence: {' → '.join(map(str, result['safe_sequence']))}")


def demo_process_lifecycle():
    """Demo 3: Complete process lifecycle"""
    print("\n" + "="*60)
    print("DEMO 3: Process Lifecycle (Allocation → Release)")
    print("="*60)
    
    resources = {'CPU': 8, 'Memory': 16}
    banker = BankersAlgorithm(resources)
    
    banker.add_process(0, {'CPU': 4, 'Memory': 8})
    banker.add_process(1, {'CPU': 3, 'Memory': 6})
    
    print("\nInitial system:")
    print_state(banker)
    
    # Allocate
    print("\n" + "-"*60)
    print("P0 requests (2, 4)...")
    status, msg = banker.request_resources(0, {'CPU': 2, 'Memory': 4})
    print(f"Result: {status.value}")
    
    print("\nP1 requests (2, 3)...")
    status, msg = banker.request_resources(1, {'CPU': 2, 'Memory': 3})
    print(f"Result: {status.value}")
    
    print_state(banker, "After Allocations")
    
    # Release
    print("\n" + "-"*60)
    print("P0 completes and releases resources...")
    banker.release_resources(0)
    print_state(banker, "After P0 Release")
    
    print("\n" + "-"*60)
    print("P1 completes and releases resources...")
    banker.release_resources(1)
    print_state(banker, "After P1 Release")


def demo_unsafe_state():
    """Demo 4: Detecting unsafe states"""
    print("\n" + "="*60)
    print("DEMO 4: Unsafe State Detection")
    print("="*60)
    
    resources = {'CPU': 6, 'Memory': 9}
    banker = BankersAlgorithm(resources)
    
    banker.add_process(0, {'CPU': 3, 'Memory': 4})
    banker.add_process(1, {'CPU': 2, 'Memory': 5})
    banker.add_process(2, {'CPU': 3, 'Memory': 4})
    
    print("\nSystem with 3 processes:")
    print("  P0: Max (3, 4)")
    print("  P1: Max (2, 5)")
    print("  P2: Max (3, 4)")
    print_state(banker)
    
    # Allocate to create tight situation
    print("\n" + "-"*60)
    print("P0 requests (2, 2)...")
    banker.request_resources(0, {'CPU': 2, 'Memory': 2})
    
    print("P1 requests (1, 3)...")
    banker.request_resources(1, {'CPU': 1, 'Memory': 3})
    
    print("P2 requests (2, 2)...")
    banker.request_resources(2, {'CPU': 2, 'Memory': 2})
    
    print_state(banker, "After Allocations")
    
    # Try to allocate more
    print("\n" + "-"*60)
    print("P0 requests (1, 2) - would this be safe?")
    result = banker.explore_what_if(0, {'CPU': 1, 'Memory': 2})
    print(f"Feasible: {result['feasible']}")
    print(f"Message: {result['message']}")


def main():
    """Run all demos"""
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█" + "  BANKER'S ALGORITHM VISUALIZER - DEMO".center(58) + "█")
    print("█" + " "*58 + "█")
    print("█"*60)
    
    demo_basic()
    demo_what_if()
    demo_process_lifecycle()
    demo_unsafe_state()
    
    print("\n" + "="*60)
    print("All demos completed!")
    print("="*60)
    print("\nTo use the GUI version, run: python gui.py")


if __name__ == '__main__':
    main()
