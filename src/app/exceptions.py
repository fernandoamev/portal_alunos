class StudentAlreadyExistsError(Exception):
    """
    Exception raised when attempting to create a student with an email or enrollment number
    that already exists in the system.
    """
    def __init__(self, message: str = "Student with this email or enrollment number already exists."):
        self.message = message
        super().__init__(self.message)

class StudentNotFoundError(Exception):
    """
    Exception raised when a student cannot be found by their ID or other unique identifiers.
    """
    def __init__(self, message: str = "Student not found."):
        self.message = message
        super().__init__(self.message)
