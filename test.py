class Player:
  def __init__(self, name, point=0):    
    self.point = point
    self.name = name 

  def add(self):
    self.point = self.point + 1

  def update(self, nameImport, pointImport):
    self.point = pointImport
    self.name = nameImport

  def id(self):
    print(self.name, self.point)
  
  def giveName(self):
    return self.name

def searchName(objectList, targetName):
    for objectt in objectList:
        if objectt.name == targetName:
            return False
    return True

globalPlayers = [
    {"name" : "Sanetro", "points" : 0},
    {"name" : "Derulo", "points" : 1},
    {"name" : "A", "points" : 0},
    {"name" : "Markus", "points" : 0}]

objectOfPlayers = [
    {"name" : "Merlyn", "points" : 10},
    {"name" : "A", "points" : 40},
    {"name" : "B", "points" : 50},
    {"name" : "V", "points" : 20},
    {"name" : "C", "points" : 20},
    {"name" : "D", "points" : 220},
    {"name" : "E", "points" : 550}]

fileList = []


print("FILE:")
with open("Toplist_copy.txt", "r") as f:
    for data in f:        
        row = data.split()
        fileList.append({"name" : row[0], "points" : int(row[1])})       
    f.close()


print("\n\tobjects:")
for user in objectOfPlayers:
    print(user["name"], user["points"])

print("\n\tFile objects:")
for user in fileList:
    print(user["name"], user["points"])


print("\n\tSearching:")
for innerUser in globalPlayers:
    print("For: ", innerUser["name"])
    for user in objectOfPlayers:
        print("\t", user["name"], user["points"])
        if user["name"] == innerUser["name"]:
            user["points"] += 1
            break
    else:
        objectOfPlayers.append(innerUser)
        print("\t", user["name"], "added to the list.")
            
print("\n\t")

print("\n\tobjects:")
for user in objectOfPlayers:
    print(user["name"], user["points"])
    
print("\n\tobjects:")
for user in objectOfPlayers:
    print(user["name"], user["points"])