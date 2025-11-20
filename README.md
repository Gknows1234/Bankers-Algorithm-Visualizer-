# Banker's Algorithm Visualizer + Safe State Explorer

A professional GUI-based implementation of the Banker's Algorithm for deadlock avoidance with interactive visualization and "what-if" scenario exploration.

## Features

### Core Algorithm
- **Banker's Algorithm Implementation**: Complete deadlock avoidance using resource allocation and safe state detection
- **Multi-Instance Resources**: Support for multiple resource types with configurable quantities
- **Safe State Detection**: Automatic verification of system safety after each allocation
- **State Management**: Save and restore system states for what-if analysis

### GUI Features
- **System Configuration**: Easy setup of resource types and quantities
- **Process Management**: Add/remove processes with max resource claims
- **Resource Requests**: Interactive dialog for requesting resources
- **What-If Explorer**: Test hypothetical scenarios without modifying system state
- **Real-Time Visualization**: 
  - System state table with process information
  - Resource allocation bar chart
  - Safe sequence display
  - Operation history log

### Advanced Features
- **Safe Sequence Display**: Shows the order in which processes can safely complete
- **Resource Allocation Graph**: Visual representation of resource usage
- **History Tracking**: Complete log of all operations
- **Request Validation**: Checks for need, availability, and safety before allocation

## Installation

1. Ensure Python 3.7+ is installed
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Application
```bash
python gui.py
```

### Workflow

1. **Initialize System**
   - Set resource quantities (CPU, Memory, Disk, Network)
   - Click "Initialize System"

2. **Add Processes**
   - Enter Process ID
   - Click "Add Process"
   - Specify max resource claims for each resource type

3. **Request Resources**
   - Select a process ID
   - Click "Request Resources"
   - Specify quantities needed
   - System automatically checks safety

4. **Explore What-If Scenarios**
   - Select a process ID
   - Click "Explore Request"
   - Test hypothetical allocations without modifying state
   - View resulting safe sequences

5. **Release Resources**
   - Select a process ID
   - Click "Release All Resources"
   - Resources returned to available pool

## Algorithm Details

### Banker's Algorithm
The algorithm maintains system safety by:
1. **Safety Check**: Before allocating resources, tentatively allocate and check if a safe sequence exists
2. **Safe Sequence**: Finds an order where all processes can complete with available resources
3. **Rollback**: If allocation would make system unsafe, request is denied and state is restored

### Data Structures
- **Max Claim Matrix**: Maximum resources each process may need
- **Allocated Matrix**: Currently allocated resources per process
- **Need Matrix**: Remaining resources needed (Max - Allocated)
- **Available Vector**: Resources currently available in system

## Key Components

### `bankers_algorithm.py`
- `BankersAlgorithm`: Main algorithm implementation
- `Process`: Represents a process with resource claims
- `AllocationStatus`: Enum for request outcomes

### `gui.py`
- `BankersVisualizerGUI`: Main application window
- `ResourceAllocationDialog`: Dialog for resource input
- Tabs for System State, Resource Graph, Safe Sequence, and History

## Example Scenario

**System Setup:**
- CPU: 10 instances
- Memory: 20 instances
- Disk: 15 instances
- Network: 8 instances

**Processes:**
- P0: Max (7, 5, 3)
- P1: Max (3, 2, 2)
- P2: Max (9, 0, 2)

**Operations:**
1. P0 requests (0, 1, 0) → Granted (safe sequence: P1 → P0 → P2)
2. P1 requests (2, 0, 1) → Granted
3. P2 requests (3, 0, 2) → Denied (would make system unsafe)

## Safety Guarantees

✓ No deadlock occurs if requests follow Banker's Algorithm
✓ System remains in safe state after each allocation
✓ All processes can eventually complete
✓ Resources are efficiently utilized

## Performance

- **Time Complexity**: O(n² × m) where n = processes, m = resource types
- **Space Complexity**: O(n × m) for state matrices
- Suitable for small to medium-sized systems (up to 100 processes)

## Limitations

- Designed for educational purposes
- Real-time systems may need optimizations
- Assumes static resource pool
- Processes must declare max claims upfront

## Future Enhancements

- Export/import system configurations
- Animated process execution
- Performance metrics and statistics
- Multi-threaded simulation
- Advanced graph visualization with D3.js
- REST API for remote access

## License

Educational use - Free to modify and distribute

## Author

Created as a comprehensive Banker's Algorithm visualization tool for OS education and demonstration.
