class Item:

    def __init__(self, left_side, right_side):
        self.left = left_side
        self.right = right_side

    def dot_position(self):
        index = self.right.find('.')
        return index
