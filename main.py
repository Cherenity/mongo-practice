from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId

#GLOBAL VARIABLES
MONGO_URI = MongoClient('mongodb://localhost:27017/')
MYDB = MONGO_URI['christmas_gifts_db']

FORBIDDEN_CHARS = '!@#$%^&*()_=+[]}{|\\:;\"<>,.?/'
FORBIDDEN_START_CHARS = "'_-"

GIFT_CATEGORIES = [
    "Toys",
    "Books",
    "Electronics",
    "Clothes",
    "Games",
    "Home",
    "Other"
]


"""CRUD = Create, Read, Update, Delete"""

# ✔️ Using an ObjectId object will work Esimerkki
# db.books.find_one({ "_id": ObjectId(book_id_to_find) })

#CREATE
#-------------------------------------------------
def get_valid_title()->str:
  while True:
    title = input("Gift title: ").strip()
    if len(title) < 2:
      print("Title is too short.")
      continue

    if len(title) > 50:
      print("Title is too long")
      continue

    if title.isdigit():
      print("Title cannot be numbers")
      continue

    if title:
      break
    print("Title cannot be empty.")
  return title

def get_valid_price() -> float:
  while True:
    try:
      price = float(input("Price: ").strip())
      if price < 0:
        print("Price must be 0 or higher.")
        continue

      if price > 10000:
        print("Price must be under 10000.")
        continue

      return round(price, 2)

    except ValueError:
      print("Please enter a valid number.")

def get_valid_category() -> str:
  while True:
    choice = confirm_choice("", "List all categories? (y/n): ")
    if choice:
      for category in sorted(GIFT_CATEGORIES):
        print(category)

    category = input("Category: ").strip().capitalize()

    if category in GIFT_CATEGORIES:
      return category
    else:
      print("Invalid category. Please try again.")

def get_valid_availability() -> bool:
  while True:
    value = input("Is available (true/false): ").strip().lower()
    if value in ("true", "t", "yes", "y", "1"):
      return True

    if value in ("false", "f", "no", "n", "0"):
      return False

    print("Please enter True or False.")

def get_valid_available():
  pass

def add_gift() -> None:
  title = get_valid_title()
  price = get_valid_price()
  category = get_valid_category()
  available = get_valid_availability()

  gift = {
    "title" : title, 
    "price" : price, 
    "category" : category, 
    "available": available
    }

  is_title = MYDB.gifts.find_one({"title": gift["title"]})
  is_price = MYDB.gifts.find_one({"price": gift["price"]})
  if is_title and is_price:
    print("There is a gift with same name and price")
  else:
    result = MYDB.gifts.insert_one(gift)
    print(f"Gift added with id: {result.inserted_id}")

#CAN BE MODIFIED LATER (add ❌ ?)
def name_check(name: str, is_first_name: bool | None = None) -> bool:
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
  if is_first_name is True:
    print("✅ First name is valid")
  elif is_first_name is False:
    print("✅ Last name is valid")
  else:
    print("✅ Name is valid")
  return True

def email_check(email: str) -> bool:
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

def get_valid_name(prompt1: str = "Enter first name: ",
                   prompt2: str = "Enter last name: "
                   ) -> str:
  while True:
    first_name = input(prompt1).strip().title()
    if name_check(first_name, True):
      break

  while True:
    last_name = input(prompt2).strip().title()
    if name_check(last_name, False):
      break

  full_name = first_name + " " + last_name
  print(f"Full name is: {full_name}")
  return full_name

def get_valid_email(prompt: str = "Enter email: ") -> str:
  while True:
      email = input(prompt).strip().lower()
      if email_check(email):
        break
  return email

def get_valid_age(prompt: str = "Enter age: ") -> int:
    while True:
      age = input(prompt)
      try:
        age = int(age)
        if 0 <= age <= 100:
          break
        else:
          print("Age needs to be a number between 0-100")
      except ValueError:
        print("Age needs to be a number between 0-100")
    return age

def confirm_choice(print_text:str = "", choice_text:str = "Are you satisfied with your choice? (y/n): ") -> bool:

  if print_text:
    print(print_text)

  while True:
    choice = input(choice_text).strip().lower()
    if choice == "y":
      return True
    elif choice == "n":
      return False
    else:
      print("Invalid choice")

def add_person() -> None:
  cancel_message = "Person was not added..."
  full_name = get_valid_name()
  email = get_valid_email()
  age = get_valid_age()

  person = {
    "name" : full_name,
    "email" : email,
    "age" : age
    }

  person_summary = (
    f"{'Name':<5}: {person['name']}\n"
    f"{'Email':<5}: {person['email']}\n"
    f"{'Age':<5}: {person['age']}"
    )

  confirmed = confirm_choice(f"\nAdd a new person:\n{person_summary}\n")

  if not confirmed:
    print(cancel_message)
    return

  is_existing = MYDB.people.find_one({"email": person["email"]})

  if is_existing:
    print("There is a person with this email already")
  else:
    result = MYDB.people.insert_one(person)
    print(result.inserted_id)

#BONUS
def assign_gifts():
  pass

#READ -------------------------------------------------

def gift_print(gift:dict) -> None:
    print(f"{'ID':>10}: {gift['_id']}")
    print(f"{'Title':>10}: {gift['title']}")
    print(f"{'Price':>10}: {gift['price']}")
    print(f"{'Cateory':>10}: {gift['category']}")
    print(f"{'Available':>10}: {gift['available']}")

def list_gifts()->None:
  gifts = list(MYDB.gifts.find())
  if not gifts:
    print("No gifts found")
  else:
    print("Gits\n")
    for gift in gifts:
      gift_print(gift)
      print()

def list_people_print()->None:
  print(
"""
List/search people commands:
        0) Quit listing
        1) List all
        2) Search by full name
        3) Search by partial name
"""
)

def person_print(person:dict) -> None:
  print(f"{'ID':>10}: {person['_id']}")
  print(f"{'Title':>10}: {person['name']}")
  print(f"{'Price':>10}: {person['email']}")
  print(f"{'Age':>10}: {person['age']}")

def list_people() -> None:
  people = list(MYDB.people.find())
  if not people:
    print("No persons found in the database.")
    return

  while True:
    list_people_print()
    choice = input("Choose an option: ").strip()

    match choice:
      case "0":
        break
      case "1":
        print(f"Person count {len(people)}\n")
        for person in people:
          person_print(person)
          print()
      case "2":
        print("First, complete the name check.")
        full_name = get_valid_name()
        filtered_people = [p for p in people if p["name"] == full_name]
        if not filtered_people:
          print("No people found with the name " + full_name)
        else:
          print(f"Person count {len(filtered_people)}\n")
          for person in filtered_people:
            person_print(person)
            print()
      case "3":
        partial_name = input("Please give a partial name: ").strip().lower()
        filtered_people = [p for p in people if partial_name in p["name"].lower()]
        if not filtered_people:
          print(f"No name contains'{partial_name}'.")
        else:
          print(f"Person count {len(filtered_people)}\n")
          for person in filtered_people:
              person_print(person)
              print()
      case _:
        print("Invalid choice")

def list_assigned_gifts():
  ## BONUS | needs aggregated function
  pass

#UPDATE -------------------------------------------------
def edit_person_menu_prints(person: dict)->None:
  print("\nCurrent person details: ")
  person_print(person)
  print(
"""
Edit person commands:
        0) Nothing
        1) Edit name
        2) Edit email
        3) Edit age
""")

def edit_person():
  choice = confirm_choice("Do you want to list/search people first?")
  if choice:
    list_people()

  db_person = None
  # TODO: search where you can choose wich person to edit instead of typing person ID

  person_id_to_find = input("Please give a person ID to find: ")

  try:
    db_person = MYDB.people.find_one({ "_id": ObjectId(person_id_to_find) })
  except InvalidId:
    print("Invalid ID format")
    return

  if db_person is None:
    print("No person with that ID found")
    return

  edit_person_menu_prints(db_person)
  edit_choice = input("What do you want to edit? ").strip()

  match edit_choice:
    case "0":
      print("No changes made.")
    case "1":
      # TODO: separate first and last name editing later
      new_name = get_valid_name()
      MYDB.people.update_one(
        { "_id": ObjectId(person_id_to_find) },
        { "$set": { "name": new_name } }
      )
    case "2":
      new_email = get_valid_email("Enter a new email adress: ")
      MYDB.people.update_one(
        { "_id": ObjectId(person_id_to_find) },
        { "$set": { "email": new_email } }
      )
    case "3":
      new_age = get_valid_age("Enter a new age: ")
      MYDB.people.update_one(
        { "_id": ObjectId(person_id_to_find) },
        { "$set": { "age": new_age } }
      )
    case _:
      print("Invalid choice")

def edit_gifts():
  pass

#DELETE-------------------------------------------------
def delete_gift():
  choice = confirm_choice("","Do you want to list all gifts first? (y/n):")
  if choice:
    list_gifts()
  gift_id_to_find = input("Please give a gift ID to dekelete: ")
  try:
    db_gift = MYDB.gifts.find_one({ "_id": ObjectId(gift_id_to_find) })
  except InvalidId:
    print("Invalid ID format")
    return
  if db_gift is None:
    print("No gift with that ID found")
    return

def delete_person():
  choice = confirm_choice("","Do you want to list/search people first? (y/n):")
  if choice:
    list_people()
  person_id_to_find = input("Please give a person ID to dekelete: ")
  try:
    db_person = MYDB.people.find_one({ "_id": ObjectId(person_id_to_find) })
  except InvalidId:
    print("Invalid ID format")
    return
  if db_person is None:
    print("No person with that ID found")
    return

  print("Person details: ")
  person_print(db_person)

  confirm = confirm_choice("","Delete this person? (y/n): ")

  if not confirm:
    print("Nothing deleted.")

  result = MYDB.people.delete_one({ "_id": ObjectId(person_id_to_find) })

  if result.deleted_count == 1:
    print("Person deleted.")
  else:
    print("Delete failed.")

def print_commands()->None:
  print(
"""
Commands:
        0) Exit program
        1) List/search people
        2) List gifts
        3) Add a person
        4) Add a gift
        5) Edit person details
        6) Edit gift details
        7) Delete a person
        8) Delete a gift
"""
)

def test():
  get_valid_availability()

def main():
  print("Welcome! 🎅🎁🎄 This is my practise project ~")

  while True:
    print_commands()
    choice = input("Choose an option: ")

    match choice:
      case "0":
        print("Exiting program...")
        break
      case "1":
        list_people()
      case "2":
        list_gifts()
      case "3":
        add_person()
      case "4":
        add_gift()
      case "5":
        edit_person()
      case "6":
        delete_gift()
      case "7":
        delete_person()
      case _:
        print("Invalid choice")

if __name__ == "__main__":
  # test()
  main()
