from entity.pathology import PathologyABC, NullPathology
from entity.state import SubjectState


class Subject:

    def __init__(self, id: int, age: int):
        self.id = int(id)
        self.age = int(age)
        self.state = SubjectState.OK
        self.disease: PathologyABC = NullPathology(self)

    def contact(self, subjects: list['Subject']):
        for subject in subjects:
            if subject == self:  # cannot contact with it self
                continue
            self.disease.infect(subject)

    def __str__(self):
        return f'Subject({self.id}, {self.age}, {self.state}, {self.disease})'
