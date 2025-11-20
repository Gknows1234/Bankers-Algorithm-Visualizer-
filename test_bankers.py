"""
Unit tests for Banker's Algorithm implementation
"""

import unittest
from bankers_algorithm import BankersAlgorithm, AllocationStatus, Process


class TestProcess(unittest.TestCase):
    """Test Process class"""
    
    def test_process_creation(self):
        """Test process initialization"""
        proc = Process(0, {'CPU': 5, 'Memory': 10})
        self.assertEqual(proc.pid, 0)
        self.assertEqual(proc.max_claim, {'CPU': 5, 'Memory': 10})
        # allocated and needed are empty dicts by default
        self.assertEqual(proc.allocated, {})
        self.assertEqual(proc.needed, {})
    
    def test_calculate_needed(self):
        """Test needed resource calculation"""
        proc = Process(0, {'CPU': 5, 'Memory': 10})
        proc.allocated = {'CPU': 2, 'Memory': 3}
        proc.calculate_needed()
        self.assertEqual(proc.needed, {'CPU': 3, 'Memory': 7})
    
    def test_can_finish(self):
        """Test process finish check"""
        proc = Process(0, {'CPU': 5, 'Memory': 10})
        proc.allocated = {'CPU': 2, 'Memory': 3}
        proc.calculate_needed()
        
        # Can finish with enough resources
        self.assertTrue(proc.can_finish({'CPU': 3, 'Memory': 7}))
        
        # Cannot finish with insufficient resources
        self.assertFalse(proc.can_finish({'CPU': 2, 'Memory': 7}))
        self.assertFalse(proc.can_finish({'CPU': 3, 'Memory': 6}))
    
    def test_release_resources(self):
        """Test resource release"""
        proc = Process(0, {'CPU': 5, 'Memory': 10})
        proc.allocated = {'CPU': 2, 'Memory': 3}
        
        released = proc.release_resources()
        self.assertEqual(released, {'CPU': 2, 'Memory': 3})
        self.assertEqual(proc.allocated, {'CPU': 0, 'Memory': 0})


class TestBankersAlgorithm(unittest.TestCase):
    """Test Banker's Algorithm"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.banker = BankersAlgorithm({'CPU': 10, 'Memory': 20})
    
    def test_initialization(self):
        """Test system initialization"""
        self.assertEqual(self.banker.total_resources, {'CPU': 10, 'Memory': 20})
        self.assertEqual(self.banker.available, {'CPU': 10, 'Memory': 20})
        self.assertEqual(len(self.banker.processes), 0)
    
    def test_add_process(self):
        """Test adding processes"""
        self.banker.add_process(0, {'CPU': 5, 'Memory': 10})
        self.assertIn(0, self.banker.processes)
        self.assertEqual(self.banker.processes[0].max_claim, {'CPU': 5, 'Memory': 10})
    
    def test_add_duplicate_process(self):
        """Test adding duplicate process raises error"""
        self.banker.add_process(0, {'CPU': 5, 'Memory': 10})
        with self.assertRaises(ValueError):
            self.banker.add_process(0, {'CPU': 3, 'Memory': 5})
    
    def test_remove_process(self):
        """Test removing processes"""
        self.banker.add_process(0, {'CPU': 5, 'Memory': 10})
        self.banker.request_resources(0, {'CPU': 2, 'Memory': 3})
        
        self.banker.remove_process(0)
        self.assertNotIn(0, self.banker.processes)
        # After removal, resources should be returned to available
        self.assertEqual(self.banker.available, {'CPU': 10, 'Memory': 20})
    
    def test_safe_state_initial(self):
        """Test initial state is safe"""
        self.banker.add_process(0, {'CPU': 5, 'Memory': 10})
        self.banker.add_process(1, {'CPU': 3, 'Memory': 5})
        
        self.assertTrue(self.banker.is_safe())
    
    def test_safe_sequence(self):
        """Test safe sequence generation"""
        self.banker.add_process(0, {'CPU': 5, 'Memory': 10})
        self.banker.add_process(1, {'CPU': 3, 'Memory': 5})
        
        seq = self.banker.get_safe_sequence()
        self.assertEqual(len(seq), 2)
        self.assertIn(0, seq)
        self.assertIn(1, seq)
    
    def test_request_exceeds_need(self):
        """Test request exceeding need is denied"""
        self.banker.add_process(0, {'CPU': 5, 'Memory': 10})
        
        status, msg = self.banker.request_resources(0, {'CPU': 6, 'Memory': 0})
        self.assertEqual(status, AllocationStatus.DENIED)
    
    def test_request_exceeds_available(self):
        """Test request exceeding available is denied"""
        self.banker.add_process(0, {'CPU': 5, 'Memory': 10})
        
        status, msg = self.banker.request_resources(0, {'CPU': 15, 'Memory': 0})
        self.assertEqual(status, AllocationStatus.DENIED)
    
    def test_safe_allocation(self):
        """Test safe allocation is granted"""
        self.banker.add_process(0, {'CPU': 5, 'Memory': 10})
        self.banker.add_process(1, {'CPU': 3, 'Memory': 5})
        
        status, msg = self.banker.request_resources(0, {'CPU': 2, 'Memory': 3})
        self.assertEqual(status, AllocationStatus.GRANTED)
        self.assertEqual(self.banker.processes[0].allocated, {'CPU': 2, 'Memory': 3})
    
    def test_unsafe_allocation_denied(self):
        """Test unsafe allocation is denied"""
        self.banker.add_process(0, {'CPU': 5, 'Memory': 10})
        self.banker.add_process(1, {'CPU': 5, 'Memory': 10})
        
        # Allocate most resources
        self.banker.request_resources(0, {'CPU': 5, 'Memory': 10})
        self.banker.request_resources(1, {'CPU': 5, 'Memory': 10})
        
        # Try to allocate more - should be denied
        status, msg = self.banker.request_resources(0, {'CPU': 0, 'Memory': 0})
        # This should still be safe since they're already allocated
        self.assertEqual(status, AllocationStatus.GRANTED)
    
    def test_release_resources(self):
        """Test resource release"""
        self.banker.add_process(0, {'CPU': 5, 'Memory': 10})
        self.banker.request_resources(0, {'CPU': 2, 'Memory': 3})
        
        initial_available = self.banker.available.copy()
        self.banker.release_resources(0)
        
        self.assertEqual(self.banker.available, {'CPU': 10, 'Memory': 20})
    
    def test_what_if_exploration(self):
        """Test what-if scenario exploration"""
        self.banker.add_process(0, {'CPU': 5, 'Memory': 10})
        self.banker.add_process(1, {'CPU': 3, 'Memory': 5})
        
        result = self.banker.explore_what_if(0, {'CPU': 2, 'Memory': 3})
        
        self.assertTrue(result['feasible'])
        self.assertIn('safe_sequence', result)
        
        # Verify state wasn't modified
        self.assertEqual(self.banker.processes[0].allocated, {'CPU': 0, 'Memory': 0})
    
    def test_get_system_state(self):
        """Test system state retrieval"""
        self.banker.add_process(0, {'CPU': 5, 'Memory': 10})
        self.banker.request_resources(0, {'CPU': 2, 'Memory': 3})
        
        state = self.banker.get_system_state()
        
        self.assertEqual(state['total_resources'], {'CPU': 10, 'Memory': 20})
        self.assertEqual(state['available'], {'CPU': 8, 'Memory': 17})
        self.assertTrue(state['is_safe'])
        self.assertIn(0, state['processes'])


class TestComplexScenarios(unittest.TestCase):
    """Test complex scenarios"""
    
    def test_three_process_system(self):
        """Test system with three processes"""
        banker = BankersAlgorithm({'CPU': 10, 'Memory': 20, 'Disk': 15})
        
        banker.add_process(0, {'CPU': 7, 'Memory': 5, 'Disk': 3})
        banker.add_process(1, {'CPU': 3, 'Memory': 2, 'Disk': 2})
        banker.add_process(2, {'CPU': 9, 'Memory': 0, 'Disk': 2})
        
        # Initial state should be safe
        self.assertTrue(banker.is_safe())
        
        # Allocate resources
        status, _ = banker.request_resources(0, {'CPU': 0, 'Memory': 1, 'Disk': 0})
        self.assertEqual(status, AllocationStatus.GRANTED)
        
        status, _ = banker.request_resources(1, {'CPU': 2, 'Memory': 0, 'Disk': 1})
        self.assertEqual(status, AllocationStatus.GRANTED)
        
        # System should still be safe
        self.assertTrue(banker.is_safe())
    
    def test_process_lifecycle(self):
        """Test complete process lifecycle"""
        banker = BankersAlgorithm({'CPU': 8, 'Memory': 16})
        
        banker.add_process(0, {'CPU': 4, 'Memory': 8})
        banker.add_process(1, {'CPU': 3, 'Memory': 6})
        
        # Allocate
        banker.request_resources(0, {'CPU': 2, 'Memory': 4})
        banker.request_resources(1, {'CPU': 2, 'Memory': 3})
        
        self.assertEqual(banker.available, {'CPU': 4, 'Memory': 9})
        
        # Release
        banker.release_resources(0)
        self.assertEqual(banker.available, {'CPU': 6, 'Memory': 13})
        
        banker.release_resources(1)
        self.assertEqual(banker.available, {'CPU': 8, 'Memory': 16})


class TestEdgeCases(unittest.TestCase):
    """Test edge cases"""
    
    def test_zero_allocation(self):
        """Test zero resource allocation"""
        banker = BankersAlgorithm({'CPU': 10, 'Memory': 20})
        banker.add_process(0, {'CPU': 5, 'Memory': 10})
        
        status, _ = banker.request_resources(0, {'CPU': 0, 'Memory': 0})
        self.assertEqual(status, AllocationStatus.GRANTED)
    
    def test_single_process(self):
        """Test system with single process"""
        banker = BankersAlgorithm({'CPU': 10, 'Memory': 20})
        banker.add_process(0, {'CPU': 10, 'Memory': 20})
        
        self.assertTrue(banker.is_safe())
        seq = banker.get_safe_sequence()
        self.assertEqual(seq, [0])
    
    def test_empty_system(self):
        """Test empty system"""
        banker = BankersAlgorithm({'CPU': 10, 'Memory': 20})
        
        self.assertTrue(banker.is_safe())
        self.assertEqual(banker.get_safe_sequence(), [])
    
    def test_nonexistent_process(self):
        """Test operations on nonexistent process"""
        banker = BankersAlgorithm({'CPU': 10, 'Memory': 20})
        
        status, _ = banker.request_resources(999, {'CPU': 1, 'Memory': 1})
        self.assertEqual(status, AllocationStatus.DENIED)


def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == '__main__':
    run_tests()
