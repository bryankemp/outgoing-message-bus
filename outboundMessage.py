
#superGeneric class with an init that rebuilds it into from a dictionary into the object
class OutboundMessage:
    def __init__(self, **entries):
        self.__dict__.update(entries)
    