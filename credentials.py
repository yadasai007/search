from main import main
class Credentials:
    def __init__(self,usertype,username,password) -> None:
        self.usertype=usertype
        self.username=username
        self.password=password
    

    def is_admin(self):
        return self.usertype=="admin"
    
    def elegible(self):
        if (self.is_admin() and self.usertype=="admin"):
            main(True)
        else:
            main(False)

