class Worker:
    name: str

    def __init__(self, name: str):
        self.name = name

def get_workers():
    workers = [Worker("Аня"), Worker("Костя"), Worker("Влад"), Worker("Дмитрий Валерьевич"), ]
    return workers