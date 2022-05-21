class Disser():

    def __init__(self, name, target, number):
        self.disser = name  # wer
        self.dissed = target  # wen
        self.disses = number  # wie oft

    def get_disser(self) -> str:
        return self.disser

    def get_dissed(self) -> str:
        return self.dissed

    def get_disses(self) -> int:
        return self.get_disses
