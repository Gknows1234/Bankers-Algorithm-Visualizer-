# Quick Start Guide - Banker's Algorithm Visualizer

## Installation

1. **Install Python 3.7+** (if not already installed)

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Running the Application

### Option 1: GUI Application (Recommended)
```bash
python gui.py
```

This launches the interactive GUI where you can:
- Configure system resources
- Add/remove processes
- Request resources interactively
- Explore what-if scenarios
- View real-time visualizations

### Option 2: Console Demo
```bash
python demo.py
```

This runs 4 comprehensive demonstrations showing:
1. Basic resource allocation
2. What-if scenario exploration
3. Process lifecycle management
4. Unsafe state detection

### Option 3: Run Tests
```bash
python test_bankers.py
```

Runs 23 unit tests covering all functionality.

## GUI Workflow

### Step 1: Initialize System
1. Set resource quantities (CPU, Memory, Disk, Network)
2. Click **"Initialize System"**

### Step 2: Add Processes
1. Enter a Process ID (e.g., 0, 1, 2)
2. Click **"Add Process"**
3. Specify max resource claims for each type
4. Click **OK**

### Step 3: Request Resources
1. Select a Process ID
2. Click **"Request Resources"**
3. Enter quantities needed
4. System automatically checks safety
5. Request is granted or denied

### Step 4: Explore Scenarios
1. Select a Process ID
2. Click **"Explore Request"**
3. Test hypothetical allocations
4. View safe sequences without modifying state

### Step 5: Release Resources
1. Select a Process ID
2. Click **"Release All Resources"**
3. Resources returned to available pool

## Example Scenario

**Setup:**
- CPU: 10 instances
- Memory: 20 instances
- Disk: 15 instances

**Add Processes:**
- Process 0: Max (7, 5, 3)
- Process 1: Max (3, 2, 2)
- Process 2: Max (9, 0, 2)

**Operations:**
1. P0 requests (0, 1, 0) → ✓ Granted
2. P1 requests (2, 0, 1) → ✓ Granted
3. P2 requests (3, 0, 2) → ✗ Denied (unsafe)

## Understanding the Output

### System State Tab
Shows all processes with:
- **Max Claim**: Maximum resources process may need
- **Allocated**: Currently held resources
- **Needed**: Remaining resources needed
- **Status**: Safe or Unsafe

### Resource Graph Tab
Visual bar chart showing:
- **Green bars**: Available resources
- **Red bars**: Allocated resources

### Safe Sequence Tab
Shows the order in which processes can safely complete:
- Example: "Safe Sequence: 0 → 1 → 2"

### History Tab
Complete log of all operations performed

## Key Concepts

### Safe State
A state where there exists a safe sequence - an order in which all processes can complete without deadlock.

### Safe Sequence
An order of process execution where each process can acquire its needed resources and complete.

### Deadlock Avoidance
The algorithm prevents deadlock by only granting requests that keep the system in a safe state.

### Resource Allocation
Resources are allocated only if the system remains safe after allocation.

## Troubleshooting

### GUI won't start
- Ensure PyQt5 is installed: `pip install PyQt5==5.15.9`
- Check Python version: `python --version` (should be 3.7+)

### Request always denied
- Check if resources are available
- Verify process max claims aren't exceeded
- Try releasing resources from other processes

### What-if explorer shows unsafe
- The hypothetical request would create a deadlock risk
- Try requesting fewer resources
- Release resources from other processes first

## Advanced Usage

### Using the Algorithm Directly
```python
from bankers_algorithm import BankersAlgorithm

# Create system
banker = BankersAlgorithm({'CPU': 10, 'Memory': 20})

# Add process
banker.add_process(0, {'CPU': 5, 'Memory': 10})

# Request resources
status, message = banker.request_resources(0, {'CPU': 2, 'Memory': 3})

# Check safety
if banker.is_safe():
    print("System is safe!")
    print(f"Safe sequence: {banker.get_safe_sequence()}")
```

### Visualization Analysis
```python
from visualization import ResourceAllocationGraph, StateTransitionAnalyzer

graph = ResourceAllocationGraph(banker)
print(graph.generate_full_report())

analyzer = StateTransitionAnalyzer(banker)
print(analyzer.get_system_health())
```

## Performance Notes

- Handles up to 100 processes efficiently
- Safe state check: O(n² × m) where n=processes, m=resources
- Suitable for educational and small production systems
- Real-time systems may need optimizations

## Files Overview

- **bankers_algorithm.py** - Core algorithm implementation
- **gui.py** - PyQt5 GUI application
- **demo.py** - Console demonstrations
- **test_bankers.py** - Unit tests (23 tests)
- **visualization.py** - Advanced visualization utilities
- **requirements.txt** - Python dependencies
- **README.md** - Full documentation

## Next Steps

1. Run the demo to understand the algorithm
2. Launch the GUI and experiment with scenarios
3. Read the full README.md for detailed documentation
4. Explore the source code to understand implementation
5. Modify and extend for your use cases

## Support

For issues or questions:
1. Check the README.md for detailed documentation
2. Review the demo.py for usage examples
3. Check test_bankers.py for edge cases
4. Examine the source code comments

Enjoy exploring the Banker's Algorithm! 🎓
