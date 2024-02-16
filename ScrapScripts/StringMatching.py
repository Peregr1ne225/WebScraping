from fuzzywuzzy import fuzz
from fuzzywuzzy import process

print(fuzz.token_set_ratio("Samsung Galaxy Z Fold5 (5G)".upper(), "SAMSUNG Galaxy Z Fold5 (5G) (12+1TB,F946BZEH) Cream".upper()))

choices = ["Apple MacBook Air M2/8GB/256GB SSD/15.3/STARLIGHT", "Apple MacBook Air M2/8GB/512GB SSD/15.3/STARLIGHT", "Apple MacBook Air 2020 M1/8GB/256GB SSD/13.3/SILVER (MGN93TH/A)"]
query_string = "Apple MacBook Air 15 M2 chip 256GB"

best_match, similarity = process.extractOne(query_string, choices, scorer=fuzz.token_set_ratio)
print(best_match, similarity)