"""Simple class."""

class Student:
    def __init__(self, name):
      self.name = name
      self.finished = False

student = Student("John")
print(student.name)      
print(student.finished)
