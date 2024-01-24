import os


def find_files(filename, search_path):
   result = ""

# Wlaking top-down from the root
   for root, dir, files in os.walk(search_path):
      if filename in files:
         result += os.path.join(root, filename)
   return result


path = find_files("Users\Mayur\OneDrive\Documents\Electrical","C:/")           #to search in diffrent dirs just change E with (C or D or E or F )
# path = str(path)
print(path)
os.startfile(path)