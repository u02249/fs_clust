import unittest
from fs_cluster import ClusterManager

class ClusterManagerTest(unittest.TestCase):

    def test_state_candidate(self):
        c = ClusterManager()
        c.key_not_found()
        self.assertEqual(c.candidat, c.current_state)

    def test_state_master(self):
        c = ClusterManager()
        c.key_not_found()
        c.key_set()
        self.assertEqual(c.master, c.current_state)

    def test_state_master_update(self):
        c = ClusterManager()
        c.key_not_found()
        c.key_set()
        c.key_update()
        self.assertEqual(c.master, c.current_state)

    def test_state_master_not_update(self):
        c = ClusterManager()
        c.key_not_found()
        c.key_set()
        c.key_not_update()
        self.assertEqual(c.slave, c.current_state)

if __name__ == "__main__":
    unittest.main()
