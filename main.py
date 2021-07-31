from entity.subject import Subject
from entity.pathology import ConcretePathology
from entity.state import SubjectState, PathologyState

s1 = Subject(1, 20)
s2 = Subject(1, 30)
s3 = Subject(1, 40)
s4 = Subject(1, 50)
s5 = Subject(1, 60)
s6 = Subject(1, 80)

s1.disease = ConcretePathology(s1, 0.15, 0.03, 7, 14)
s1.disease.state = PathologyState.INFECTIOUS
s1.state = SubjectState.SICK

a = [s1, s2, s3, s4, s5, s6]
s1.contact(a)

print('inicio')
for s in a:
    print(s)

print('kill 1')
for ss in a:
    ss.disease.kill()
    print(ss)

print('kill 2')
for ss in a:
    ss.disease.kill()
    print(ss)

print('kill 3')
for ss in a:
    ss.disease.kill()
    print(ss)