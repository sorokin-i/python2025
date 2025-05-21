class Worker:
    name: str
    events_count = 0

    def __init__(self, name: str):
        self.name = name


def get_workers():
    workers = [Worker("Аня"), Worker("Костя"), Worker("Влад"), Worker("Дмитрий Валерьевич"), ]
    return workers