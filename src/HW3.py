
print('Гра "Камінь, ножиці, папір", де:\n1 = камінь\n2 = ножиці\n3 = папір')

player1 = int(input("Гравець 1, введіть: "))
player2 = int(input("Гравець 2, введіть: "))

if player1 == 1 and player2 == 2 or player1 == 2 and player2 == 3 or player1 == 3 and player2 == 1:
    print("Гравець 1 переміг!")
elif player1 == 2 and player2 == 1 or player1 == 3 and player2 == 2 or player1 == 1 and player2 == 3:
    print("Гравець 2 переміг!")
elif player1 == player2:
    print("Нічия!")
else:
    print("Помилка, потрібно (1, 2, 3), де 1 = камінь, 2 = ножиці, 3 = папір: .")
