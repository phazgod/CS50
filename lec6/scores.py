from cs50 import get_int

scores = []
for i in range(3):
    number = get_int("Scores: ")
    scores.append(number)
average = sum(scores) / len(scores)
print(f"Average: {average}")