"""
Example scenarios demonstrating various Banker's Algorithm use cases
Run individual scenarios to see different behaviors
"""

from bankers_algorithm import BankersAlgorithm, AllocationStatus
from visualization import ResourceAllocationGraph, StateTransitionAnalyzer


def scenario_1_simple_allocation():
    """Scenario 1: Simple resource allocation with 2 processes"""
    print("\n" + "="*70)
    print("SCENARIO 1: Simple Resource Allocation")
    print("="*70)
    
    banker = BankersAlgorithm({'CPU': 10, 'Memory': 20})
    
    banker.add_process(0, {'CPU': 5, 'Memory': 10})
    banker.add_process(1, {'CPU': 3, 'Memory': 8})
    
    print("\nSystem initialized with:")
    print("  Resources: CPU=10, Memory=20")
    print("  Process 0: Max (5, 10)")
    print("  Process 1: Max (3, 8)")
    
    # Allocate resources
    status, msg = banker.request_resources(0, {'CPU': 2, 'Memory': 5})
    print(f"\nP0 requests (2, 5): {status.value}")
    
    status, msg = banker.request_resources(1, {'CPU': 1, 'Memory': 3})
    print(f"P1 requests (1, 3): {status.value}")
    
    state = banker.get_system_state()
    print(f"\nSystem is {'SAFE ✓' if state['is_safe'] else 'UNSAFE ✗'}")
    print(f"Safe sequence: {' → '.join(map(str, state['safe_sequence']))}")


def scenario_2_deadlock_prevention():
    """Scenario 2: Demonstrating deadlock prevention"""
    print("\n" + "="*70)
    print("SCENARIO 2: Deadlock Prevention")
    print("="*70)
    
    banker = BankersAlgorithm({'CPU': 6, 'Memory': 9})
    
    banker.add_process(0, {'CPU': 3, 'Memory': 4})
    banker.add_process(1, {'CPU': 2, 'Memory': 5})
    banker.add_process(2, {'CPU': 3, 'Memory': 4})
    
    print("\nSystem initialized with:")
    print("  Resources: CPU=6, Memory=9")
    print("  Process 0: Max (3, 4)")
    print("  Process 1: Max (2, 5)")
    print("  Process 2: Max (3, 4)")
    
    # Allocate to create tight situation
    banker.request_resources(0, {'CPU': 2, 'Memory': 2})
    banker.request_resources(1, {'CPU': 1, 'Memory': 3})
    banker.request_resources(2, {'CPU': 2, 'Memory': 2})
    
    print("\nAfter allocations:")
    print("  P0 allocated: (2, 2)")
    print("  P1 allocated: (1, 3)")
    print("  P2 allocated: (2, 2)")
    
    # Try to allocate more
    print("\nAttempting additional allocations:")
    
    status, msg = banker.request_resources(0, {'CPU': 1, 'Memory': 2})
    print(f"  P0 requests (1, 2): {status.value}")
    if status == AllocationStatus.DENIED:
        print(f"    Reason: {msg}")
    
    status, msg = banker.request_resources(1, {'CPU': 1, 'Memory': 2})
    print(f"  P1 requests (1, 2): {status.value}")
    if status == AllocationStatus.DENIED:
        print(f"    Reason: {msg}")
    
    state = banker.get_system_state()
    print(f"\nSystem is {'SAFE ✓' if state['is_safe'] else 'UNSAFE ✗'}")


def scenario_3_multi_resource():
    """Scenario 3: Multiple resource types (CPU, Memory, Disk, Network)"""
    print("\n" + "="*70)
    print("SCENARIO 3: Multi-Resource System")
    print("="*70)
    
    resources = {
        'CPU': 10,
        'Memory': 20,
        'Disk': 15,
        'Network': 8
    }
    
    banker = BankersAlgorithm(resources)
    
    banker.add_process(0, {'CPU': 7, 'Memory': 5, 'Disk': 3, 'Network': 2})
    banker.add_process(1, {'CPU': 3, 'Memory': 2, 'Disk': 2, 'Network': 1})
    banker.add_process(2, {'CPU': 9, 'Memory': 0, 'Disk': 2, 'Network': 3})
    
    print("\nSystem initialized with 4 resource types:")
    print(f"  Resources: {resources}")
    print("  Process 0: Max (7, 5, 3, 2)")
    print("  Process 1: Max (3, 2, 2, 1)")
    print("  Process 2: Max (9, 0, 2, 3)")
    
    # Allocate resources
    allocations = [
        (0, {'CPU': 0, 'Memory': 1, 'Disk': 0, 'Network': 1}),
        (1, {'CPU': 2, 'Memory': 0, 'Disk': 1, 'Network': 0}),
        (2, {'CPU': 3, 'Memory': 0, 'Disk': 2, 'Network': 1}),
    ]
    
    print("\nAllocating resources:")
    for pid, request in allocations:
        status, msg = banker.request_resources(pid, request)
        print(f"  P{pid} requests {request}: {status.value}")
    
    state = banker.get_system_state()
    print(f"\nSystem is {'SAFE ✓' if state['is_safe'] else 'UNSAFE ✗'}")
    print(f"Safe sequence: {' → '.join(map(str, state['safe_sequence']))}")
    
    # Show resource utilization
    print("\nResource Utilization:")
    for resource, total in state['total_resources'].items():
        available = state['available'].get(resource, 0)
        used = total - available
        pct = (used / total * 100) if total > 0 else 0
        print(f"  {resource}: {used}/{total} ({pct:.1f}%)")


def scenario_4_what_if_analysis():
    """Scenario 4: What-if scenario exploration"""
    print("\n" + "="*70)
    print("SCENARIO 4: What-If Analysis")
    print("="*70)
    
    banker = BankersAlgorithm({'CPU': 10, 'Memory': 20})
    
    banker.add_process(0, {'CPU': 5, 'Memory': 10})
    banker.add_process(1, {'CPU': 4, 'Memory': 7})
    
    print("\nSystem initialized with:")
    print("  Resources: CPU=10, Memory=20")
    print("  Process 0: Max (5, 10)")
    print("  Process 1: Max (4, 7)")
    
    # Initial allocations
    banker.request_resources(0, {'CPU': 2, 'Memory': 3})
    banker.request_resources(1, {'CPU': 1, 'Memory': 2})
    
    print("\nAfter initial allocations:")
    print("  P0 allocated: (2, 3)")
    print("  P1 allocated: (1, 2)")
    
    # What-if scenarios
    scenarios = [
        (0, {'CPU': 2, 'Memory': 5}),
        (0, {'CPU': 3, 'Memory': 7}),
        (1, {'CPU': 2, 'Memory': 4}),
        (1, {'CPU': 3, 'Memory': 5}),
    ]
    
    print("\nWhat-If Analysis:")
    for pid, request in scenarios:
        result = banker.explore_what_if(pid, request)
        feasible = "✓ FEASIBLE" if result['feasible'] else "✗ NOT FEASIBLE"
        print(f"\n  P{pid} requests {request}: {feasible}")
        print(f"    Message: {result['message']}")
        if result['safe_sequence']:
            print(f"    Safe sequence: {' → '.join(map(str, result['safe_sequence']))}")


def scenario_5_process_lifecycle():
    """Scenario 5: Complete process lifecycle"""
    print("\n" + "="*70)
    print("SCENARIO 5: Process Lifecycle Management")
    print("="*70)
    
    banker = BankersAlgorithm({'CPU': 8, 'Memory': 16})
    
    print("\nInitial system: CPU=8, Memory=16")
    
    # Add processes
    banker.add_process(0, {'CPU': 4, 'Memory': 8})
    banker.add_process(1, {'CPU': 3, 'Memory': 6})
    banker.add_process(2, {'CPU': 2, 'Memory': 4})
    
    print("Added 3 processes")
    
    # Phase 1: Allocation
    print("\n--- Phase 1: Resource Allocation ---")
    banker.request_resources(0, {'CPU': 2, 'Memory': 4})
    print("P0 allocated (2, 4)")
    
    banker.request_resources(1, {'CPU': 2, 'Memory': 3})
    print("P1 allocated (2, 3)")
    
    banker.request_resources(2, {'CPU': 1, 'Memory': 2})
    print("P2 allocated (1, 2)")
    
    state = banker.get_system_state()
    print(f"Available: {state['available']}")
    
    # Phase 2: Execution
    print("\n--- Phase 2: Process Execution ---")
    print("Processes executing...")
    
    # Phase 3: Release
    print("\n--- Phase 3: Resource Release ---")
    banker.release_resources(0)
    print("P0 completed and released resources")
    state = banker.get_system_state()
    print(f"Available: {state['available']}")
    
    banker.release_resources(1)
    print("P1 completed and released resources")
    state = banker.get_system_state()
    print(f"Available: {state['available']}")
    
    banker.release_resources(2)
    print("P2 completed and released resources")
    state = banker.get_system_state()
    print(f"Available: {state['available']}")
    
    print("\nAll processes completed successfully!")


def scenario_6_system_health():
    """Scenario 6: System health and risk analysis"""
    print("\n" + "="*70)
    print("SCENARIO 6: System Health Analysis")
    print("="*70)
    
    banker = BankersAlgorithm({'CPU': 10, 'Memory': 20, 'Disk': 15})
    
    banker.add_process(0, {'CPU': 5, 'Memory': 10, 'Disk': 8})
    banker.add_process(1, {'CPU': 4, 'Memory': 8, 'Disk': 5})
    banker.add_process(2, {'CPU': 3, 'Memory': 6, 'Disk': 4})
    
    print("\nSystem initialized with 3 processes")
    
    # Allocate resources to create different scenarios
    banker.request_resources(0, {'CPU': 3, 'Memory': 5, 'Disk': 4})
    banker.request_resources(1, {'CPU': 2, 'Memory': 4, 'Disk': 2})
    banker.request_resources(2, {'CPU': 1, 'Memory': 2, 'Disk': 1})
    
    print("\nResources allocated to all processes")
    
    # Analyze system health
    analyzer = StateTransitionAnalyzer(banker)
    health = analyzer.get_system_health()
    
    print("\n--- System Health Report ---")
    print(f"Safe: {'✓ Yes' if health['is_safe'] else '✗ No'}")
    print(f"Deadlock Risk: {health['deadlock_risk']*100:.1f}%")
    print(f"Active Processes: {health['num_processes']}")
    
    print("\nResource Utilization:")
    for resource, util in health['resource_utilization'].items():
        bar = "█" * int(util / 5) + "░" * (20 - int(util / 5))
        print(f"  {resource:<10} [{bar}] {util:>6.1f}%")
    
    # Generate visualization
    print("\n--- Resource Allocation Graph ---")
    graph = ResourceAllocationGraph(banker)
    print(graph.generate_ascii_graph())


def main():
    """Run all scenarios"""
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  BANKER'S ALGORITHM - EXAMPLE SCENARIOS".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    scenarios = [
        ("Simple Allocation", scenario_1_simple_allocation),
        ("Deadlock Prevention", scenario_2_deadlock_prevention),
        ("Multi-Resource System", scenario_3_multi_resource),
        ("What-If Analysis", scenario_4_what_if_analysis),
        ("Process Lifecycle", scenario_5_process_lifecycle),
        ("System Health Analysis", scenario_6_system_health),
    ]
    
    print("\nAvailable Scenarios:")
    for i, (name, _) in enumerate(scenarios, 1):
        print(f"  {i}. {name}")
    
    print("\nRunning all scenarios...\n")
    
    for name, scenario_func in scenarios:
        try:
            scenario_func()
        except Exception as e:
            print(f"\nError in {name}: {e}")
    
    print("\n" + "="*70)
    print("All scenarios completed!")
    print("="*70)
    print("\nTo run individual scenarios, modify main() or import and call directly")


if __name__ == '__main__':
    main()
