import random
import unittest

import connect_4


class TestInitialState(unittest.TestCase):
    def setUp(self) -> None:
        self.state = connect_4.connect_4.State()

    def test_print(self):
        print(self.state)
        while not self.state.is_game_over():
            # print(self.state.get_valid_actions())
            random_action = random.randrange(7)
            while not self.state.get_valid_actions()[random_action]:
                random_action = random.randrange(7)
            self.state.take_action(random_action)
            print(self.state)


if __name__ == '__main__':
    unittest.main()
