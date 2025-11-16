import ast

def solve_qr_large(p, candidates):
    """Finds quadratic residue and calculates its largest square root modulo p."""
    if p % 4 != 3:
        print(f"Error: p={p} does not satisfy p % 4 == 3")
        return
    
    print(f"Prime p = {p} (p % 4 = {p % 4})\n")
    
    # Find quadratic residue using Euler's Criterion
    exponent_test = (p - 1) // 2
    found_residue = None
    
    for a in candidates:
        result = pow(a, exponent_test, p)
        if result == 1:
            print(f"[+] Found QR: {a}")
            found_residue = a
            break
        print(f"[-] Not QR: {a}")
    
    if not found_residue:
        print("No quadratic residue found")
        return
    
    # Calculate square roots: a^((p+1)/4) % p
    root1 = pow(found_residue, (p + 1) // 4, p)
    root2 = p - root1
    flag = max(root1, root2)
    
    print(f"\nRoots: {root1}, {root2}")
    print(f"Flag (larger root): {flag}")
    return flag

def parse_input_file(filename="output.txt"):
    """Reads and parses p and list of integers from file."""
    try:
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        
        if len(lines) < 2:
            print(f"Error: File must contain at least 2 lines")
            return None, None
        
        p_line = next((line for line in lines if line.startswith(('p =', 'p='))), None)
        ints_line = next((line for line in lines if line.startswith(('ints =', 'ints='))), None)
        
        if not p_line or not ints_line:
            print("Error: Could not find 'p =' or 'ints =' in file")
            return None, None
        
        p = int(p_line.split('=', 1)[1].strip())
        candidates = ast.literal_eval(ints_line.split('=', 1)[1].strip())
        
        print(f"Successfully parsed '{filename}'")
        return p, candidates
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return None, None
    except Exception as e:
        print(f"Error parsing file: {e}")
        return None, None

if __name__ == "__main__":
    p, candidates = parse_input_file("output.txt")
    if p and candidates:
        solve_qr_large(p, candidates)