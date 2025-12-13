from pymongo import MongoClient

#GLOBAL VARIABLES
MONGO_URI = MongoClient('mongodb://localhost:27017/')
MYDB = MONGO_URI['christmas_gifts_db']

FORBIDDEN_CHARS = '!@#$%^&*()_=+[]}{|\\:;\"<>,.?/'
FORBIDDEN_START_CHARS = "'_-"

"""CRUD = Create, Read, Update, Delete"""

# ✔️ Using an ObjectId object will work Esimerkki
# db.books.find_one({ "_id": ObjectId(book_id_to_find) })

#Create
def add_gift():
  gift = {"title" : "", "price" : "", "category" : "", "available": ""}

  title = input("Gift title: ")
  price = float(input("Price: "))
  category = input("Category: ")
  available = input("Is available, please enter True or False; ")

  is_title = MYDB.people.find_one({"title": gift["title"]})
  is_price = MYDB.people.find_one({"price": gift["price"]})
  if is_title and is_price:
    print("There is a gift with same name and price")
  else:
    result = MYDB.people.insert_one(gift)

#CAN BE MODIFIED LATER (add ❌ ?)
def name_checks(name: str)->bool:
  if not name:
      print("First name cannot be empty")
      return False  
  if any(char.isdigit() for char in name):
      print("No numbers allowed in first name")
      return False
  if any(char in FORBIDDEN_CHARS for char in name):
      print("Name contains forbidden characters")
      return False
  if name[0] in FORBIDDEN_START_CHARS:
      print("Name cannot start with this character")
      return False
  print("✅ Name is valid")
  return True

def email_check(email: str)->bool:
  if not email:
    print("email address cannot be empty")
    return False
  if email.count("@") != 1:
    print("Email address must contain exactly one '@' symbol.")
    return False
  
  local, domain = email.split("@")

  if not local:
    print("Email is missing the username before the '@' symbol.")
    return False
  if not domain:
    print("Email is missing the domain after the '@' symbol.")
    return False
  if "." not in domain:
    print("Domain must contain a dot (e.g. .com, .fi).")
    return False
  
  domain_parts = domain.split(".")

  if any(part == "" for part in domain_parts):
    print("Domain parts cannot be empty (e.g. 'example.com').")
    return False

  print("✅ Email is valid")
  return True

def add_person()->None:

  while True:
    first_name = input("Enter first name: ").strip().title()
    if name_checks(first_name):
      break

  # check = input("Want to continue yes|no: ") 
  # if check == "no":#HARKITAAN JOTAIN myöhemmin oma funktio?
  #   return

  while True:
    last_name = input("Enter last name: ").strip().title()
    if name_checks(last_name):
      full_name = first_name + " " + last_name
      break

  while True:
    email = input("Enter email: ").strip().lower()
    if email_check(email):
      break

  while True:
    age = input("Enter age: ")
    try:
      age = int(age)
      if 0 <= age <= 100:
        break  
    except ValueError:
      print("Age needs to be a number between 0-100")
  
  person = {"name" : "", "email" : "", "age" : ""}
  person["name"] = full_name
  person["email"] = email
  person["age"] = age
  
  print(person.values())

  is_existing = MYDB.people.find_one({"email": person["email"]})

  if is_existing:
    print("There is a person with this email already")
  else:
    result = MYDB.people.insert_one(person)
    print(result.inserted_id)
 
#BONUS
def assign_gifts():
  pass

#Read
def list_gifts()->None:
  gifts = list(MYDB.gifts.find())
  if not gifts:
    print("No gifts found")
  else:
    print("Gits\n")
    for gift in gifts:
      print(f"Title: {gift['title']}")
      print(f"Price: {gift['price']}")
      print(f"Cateory: {gift['category']}")
      print(f"Available: {gift['available']}")
      print()

def list_people()->None:
  people = list(MYDB.people.find())
  print(len(people))

  if not people:
    print("Not a single person found")
  else:
    print(f"Person count {len(people)}\n")
    for person in people:
      print(f"Title: {person['name']}")
      print(f"Price: {person['email']}")
      print(f"Cateory: {person['age']}")
      print("--------------------------------------")

def list_assigned_gifts():
  ## BONUS | needs aggregated function
  pass

#Update
def edit_people():
  pass
  email = input("Anna henkilön sähköpostiosoite: ")

  db_person = MYDB.people.find_one({"email": email})
  
  if not db_person:
    print("No person with that email found")
    return
  
  # check haluuko vaihtaa puuttuu vielä ja tarkistusket
  name = input("New name: ").strip().title()
  email = input("New email: ").strip().title()
  age = input("New age: ").strip()

  name = db_person["name"]
  email = db_person["email"]
  age = db_person["age"]

def edit_gifts():
  pass

#Delete
def delete_gift():
  pass

def delete_person():
  pass

def print_commands()->None:
  print("\n" + "Commands: " + "\n" \
  "\t0) " + "Exit program " + "\n" \
  "\t1) " + "List people"  + "\n"\
  "\t2) " + "List gifts" + "\n" \
  "\t3) " + "Add a person" + "\n" \
  "\t4) " + "Add a gift" + "\n"
  
  )

def test():
  print("TEST PROGRAM")
  add_person()

def main():
  print("Welcome! 🎅🎁🎄 This is my practise project ~")


  while True:
    print_commands()
    choice = input("Choose an option: ")
    
    if choice == "0":
      print("Exiting program...")
      break

    match choice:
      case "1":
        list_people()
      case "2":
        list_gifts()
      case "3":
        add_person()
      case "4":
        add_gift() 
      case _:
        print("Invalid choice")



  # list_gifts()
  # list_people()

  # gifts = DB_NAME.gifts.find()

  # for gift in gifts:
  #   print(gift["title"])


if __name__ == "__main__":
  main()
  # test()