# Set the given values
p = 29
numbers_to_check = [14, 6, 11]

# memory
found_residue = None
root1 = None
root2 = None

# Loop through all possible roots 'a' from 1 to p-1
for a in range(1, p):
    # Calculate the square of 'a' modulo p
    square = (a * a) % p
    
    # Check if this square is one of the numbers we're looking for
    if square in numbers_to_check:
        found_residue = square
        root1 = a
        root2 = p - a
        break

# Print the results
if found_residue is not None:
    print(f"p = {p}")
    print(f"List of numbers = {numbers_to_check}")
    print("-----------------------------------")
    print(f"Found Quadratic Residue: {found_residue}")
    print(f"The square roots are: {root1} and {root2}")
    
    # Calculate the smaller root for the flag
    flag = min(root1, root2)
    print(f"The smaller square root (the flag) is: {flag}")
else:
    print("Could not find a quadratic residue in the list.")