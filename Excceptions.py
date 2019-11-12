class UnknownLocation(Exception):

    def __init__(self, location):
        super().__init__(f"Sorry, {location} unknown...")
        self.location = location

    def __str__(self):
        return repr(self.value)


class Time_Format_Error(Exception):

    def __init__(self, time):
        super().__init__(f"Sorry, unvalid time : {time}  ...")
        self.time = time

    def __str__(self):
        return repr(self.value)