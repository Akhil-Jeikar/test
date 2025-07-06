from packages.server import Server

print(Server.version)

s = Server()

@s.get('/')
def root():
    return "root"

@s.get("/json")
def return_json():
    return {"aj": 1}

@s.get("/try/{a}/{b}/{c}")
def fun(a, b, c):
    return {"Item id": (a, b, c)}

@s.post("/post")
def submit(p,q):
    return {"p": p,"q":q}

@s.post("/user/{id}")
def user(id):
    return (id)

@s.post('/{a}')
def g(a):
    return {"a":a}
s.run()
