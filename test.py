from dictionary import Dictionary

# Initialize the dictionary
#dictionary = Dictionary(data_dir="dictionary/data/en")
dictionary = Dictionary()

# Look up a word
word = "truth"
result = dictionary.lookup(word)

if result:
    print(f"Definition of '{word}': {result}")
else:
    print(f"Word '{word}' not found in the dictionary.")

print("Returning a random value:")
print(dictionary.randomWord())
