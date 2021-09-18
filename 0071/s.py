def abbreviate(word):
	return word[0] + str(len(word)-2) + word[-1]

n_words = int(input())
for _ in range(n_words):
	word = input()
	if len(word) <= 10:
		print(word)
	else:
		print(abbreviate(word))