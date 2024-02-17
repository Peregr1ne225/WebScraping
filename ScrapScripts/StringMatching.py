from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from thefuzz import fuzz as fuz

print(fuzz.token_sort_ratio('MSI VGA GeForce RTX 4090 VENTUS 3X OC 24GB GDDR6X 384-bit'.upper(), "VGA MSI GEFORCE RTX 4090 VENTUS 3X - 24GB GDDR6X".upper()))
print(fuz.token_sort_ratio('MSI VGA GeForce RTX 4090 VENTUS 3X OC 24GB GDDR6X 384-bit'.upper(), "VGA MSI GEFORCE RTX 4090 VENTUS 3X - 24GB GDDR6X".upper()))

choices = ["Apple MacBook Air M2/8GB/256GB SSD/15.3/STARLIGHT", "Apple MacBook Air M2/8GB/256GB SSD/15.3/MIDNIGHT", "Apple MacBook Air 2020 M1/8GB/256GB SSD/13.3/SILVER (MGN93TH/A)"]
query_string = "Apple MacBook Air 15 M2 chip 256GB"

best_match, similarity = process.extractOne(query_string, choices, scorer=fuzz.token_sort_ratio)
best_matc, similarit = process.extractOne(query_string, choices, scorer=fuz.token_sort_ratio)
print(best_match, similarity, best_matc, similarit)