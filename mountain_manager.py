from mountain import Mountain


class MountainManager:

    def __init__(self) -> None:
        self.mountains = []

    def add_mountain(self, mountain: Mountain):
        if mountain in self.mountains:
            self.mountains.append(mountain)
        else:
            raise KeyError(Mountain)

    def remove_mountain(self, mountain: Mountain):
        self.mountains.remove(mountain)

    def edit_mountain(self, old: Mountain, new: Mountain):
        raise NotImplementedError()

    def mountains_with_difficulty(self, diff: int):
        raise NotImplementedError()

    def group_by_difficulty(self):
        raise NotImplementedError()
