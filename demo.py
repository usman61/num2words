from num2words import num2words
no= 18
print(num2words(no))
print(f"Arabic: {num2words(no, lang='ar')}")
print("--------------------------------------")
print(f"Urdu: {num2words(no, lang='ur')}")