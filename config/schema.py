import strawberry

name:str ="nico"

@strawberry.type
class Query:
    
    def ping(self)