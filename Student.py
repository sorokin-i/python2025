class Student:
    name = ""
    age = 0
    cl = 0
    favorite_subject = ""
    health = 10

    def __init__(self, name, age=0, cl=0, favorite_subject=""):
        self.name = name
        self.age = age
        self.cl = cl
        self.favorite_subject = favorite_subject

    def __repr__(self):
        return f"name: {self.name}, age: {self.age}, class: {self.cl}, favorite subject: {self.favorite_subject}, health: {self.health}"

    def greet_teacher(self, teachers_name="учитель"):
        if teachers_name[-1] == 'а':
            print(f"Здравствуйте, уважаемая {teachers_name}!")
        else:
            print(f"Здравствуйте, уважаемый {teachers_name}!")


    def hit_student(self, other_student):
        other_student.health -= 1
        print(f"{self.name} побил {other_student.name}")
    def sleep(self):
        self.health = 10
        print(f"{self.name} поспал и теперь здоров, полон сил и энергии")


if __name__ == "__main__":
    st1 = Student("Гоша")
    st2 = Student("Паша", 17, 10, "Математика")
    print(st1)
    print(st2)

    st1.greet_teacher("Дмитрий Валерьевич")
    st2.greet_teacher("Елена Леонидовна")
    st1.greet_teacher()
    print(f"st1.health = {st1.health} st2.health = {st2.health}")
    st1.hit_student(st2)
    print(f"st1.health = {st1.health} st2.health = {st2.health}")
    st2.sleep()
    print(f"st1.health = {st1.health} st2.health = {st2.health}")
