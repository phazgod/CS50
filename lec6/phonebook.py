people = {
    "Carter": "+7-991-879-66-15",
    "David": "+7-964-599-17-23",
}

name = input("Name: ")

if name in people:
    number = people[name]
    print(f"Number: {number}")
else:
    print("Not found")