from pwn import *
import json
import math

# Constants from the server
N = 56135841374488684373258694423292882709478511628224823806418810596720294684253418942704418179091997825551647866062286502441190115027708222460662070779175994701788428003909010382045613207284532791741873673703066633119446610400693458529100429608337219231960657953091738271259191554117313396642763210860060639141073846574854063639566514714132858435468712515314075072939175199679898398182825994936320483610198366472677612791756619011108922142762239138617449089169337289850195216113264566855267751924532728815955224322883877527042705441652709430700299472818705784229370198468215837020914928178388248878021890768324401897370624585349884198333555859109919450686780542004499282760223378846810870449633398616669951505955844529109916358388422428604135236531474213891506793466625402941248015834590154103947822771207939622459156386080305634677080506350249632630514863938445888806223951124355094468682539815309458151531117637927820629042605402188751144912274644498695897277
phi = 56135841374488684373258694423292882709478511628224823806413974550086974518248002462797814062141189227167574137989180030483816863197632033192968896065500768938801786598807509315219962138010136188406833851300860971268861927441791178122071599752664078796430411769850033154303492519678490546174370674967628006608839214466433919286766123091889446305984360469651656535210598491300297553925477655348454404698555949086705347702081589881912691966015661120478477658546912972227759596328813124229023736041312940514530600515818452405627696302497023443025538858283667214796256764291946208723335591637425256171690058543567732003198060253836008672492455078544449442472712365127628629283773126365094146350156810594082935996208856669620333251443999075757034938614748482073575647862178964169142739719302502938881912008485968506720505975584527371889195388169228947911184166286132699532715673539451471005969465570624431658644322366653686517908000327238974943675848531974674382848
g = 986762276114520220801525811758560961667498483061127810099097

FLAG_LENGTH = 8 * 50  # Try up to 50 bytes

# Compute the order of g
# Since N is a product of safe primes p and q where p = 2*p' + 1, q = 2*q' + 1
# phi(N) = (p-1)*(q-1) = 4*p'*q'
# The order of g divides phi(N)
# For a cofactor attack, g likely has a small order

def find_order_of_g():
    """Find the order of g modulo N"""
    # Check small divisors of phi
    # phi = 4 * p' * q' where p' and q' are primes
    # Possible orders: 1, 2, 4, p', q', 2*p', 2*q', 4*p', 4*q', 2*p'*q', 4*p'*q', phi
    
    # Let's check if g^2 = 1, g^4 = 1, etc.
    log.info(f"Checking order of g = {g}")
    
    for power in [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]:
        result = pow(g, power, N)
        log.info(f"g^{power} mod N = {result}")
        if result == 1:
            log.success(f"Found order: g^{power} = 1")
            return power
    
    # Try phi//2
    g_phi_half = pow(g, phi // 2, N)
    log.info(f"g^(phi/2) mod N = {g_phi_half}")
    if g_phi_half == 1:
        log.success(f"Order divides phi/2")
        return phi // 2
    
    return None

def jacobi_symbol(a, n):
    """Compute the Jacobi symbol (a/n)"""
    if n <= 0 or n % 2 == 0:
        raise ValueError("n must be a positive odd integer")
    a = a % n
    result = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in [3, 5]:
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a = a % n
    return result if n == 1 else 0

def is_bit_one(value, n):
    """
    If g is a non-quadratic residue, all its powers are also non-quadratic residues.
    A random number has a 50% chance of being a quadratic residue.
    If jacobi_symbol(value, n) == 1, the value is a quadratic residue, so it can't be a power of g. The bit is 0.
    If jacobi_symbol(value, n) == -1, it's a non-quadratic residue, so it's a power of g. The bit is 1.
    """
    j = jacobi_symbol(value, n)
    if j == 1:
        return False  # Bit is 0
    elif j == -1:
        return True  # Bit is 1
    else:
        # This case (j=0) is very unlikely for large N
        log.warning("Jacobi symbol is 0, assuming bit 0")
        return False


def solve():
    # Connect to the challenge server
    conn = remote('socket.cryptohack.org', 13398)

    # Receive the banner
    banner = conn.recvline()
    log.info(f"Banner: {banner.decode().strip()}")

    # Check if g is a quadratic residue
    g_jacobi = jacobi_symbol(g, N)
    if g_jacobi == 1:
        log.info("g is a quadratic residue modulo N.")
    elif g_jacobi == -1:
        log.info("g is a non-quadratic residue modulo N.")
    else:
        log.info("g shares a factor with N.")

    flag_bits = []

    for i in range(FLAG_LENGTH):
        # Request bit i
        payload = json.dumps({"option": "get_bit", "i": i})
        conn.sendline(payload.encode())

        response = conn.recvline()
        try:
            data = json.loads(response.decode())
        except json.JSONDecodeError:
            log.error(f"Failed to decode JSON: {response}")
            continue

        if "bit" in data:
            value = int(data["bit"], 16)
            if is_bit_one(value, N):
                flag_bits.append(1)
                log.info(f"Bit {i}: 1")
            else:
                flag_bits.append(0)
                log.info(f"Bit {i}: 0")
        else:
            log.error(f"Error from server: {data}")
            break

    # Reconstruct the flag
    flag_bytes = bytearray()
    for i in range(0, len(flag_bits), 8):
        byte = 0
        for j in range(8):
            if i + j < len(flag_bits) and flag_bits[i + j] == 1:
                byte |= (1 << j)
        flag_bytes.append(byte)

    try:
        flag = flag_bytes.decode('ascii')
        log.success(f"Flag: {flag}")
    except UnicodeDecodeError:
        log.error(f"Could not decode flag: {flag_bytes.hex()}")

    conn.close()


if __name__ == "__main__":
    solve()
        
        if "error" in data:
            log.info(f"Reached end of flag at bit {i}")
            break
            
        bit_value_hex = data["bit"]
        bit_value = int(bit_value_hex, 16)
        
        # Check if it's in the subgroup generated by g
        is_in_subgroup = is_in_subgroup_generated_by_g(bit_value, N, g)
        flag_bits.append(1 if is_in_subgroup else 0)
        
        if i % 8 == 7:
            log.info(f"Byte {i // 8}: {flag_bits[i-7:i+1]}")
    
    # Convert bits to bytes
    flag_bytes = []
    for byte_idx in range(len(flag_bits) // 8):
        byte_val = 0
        for bit_idx in range(8):
            if flag_bits[byte_idx * 8 + bit_idx]:
                byte_val |= (1 << bit_idx)
        flag_bytes.append(byte_val)
    
    flag = bytes(flag_bytes)
    conn.close()
    log.success(f"Flag: {flag}")
    try:
        log.success(f"Flag decoded: {flag.decode()}")
    except:
        log.info(f"Flag (hex): {flag.hex()}")
    
    # Convert bits to bytes
    flag_bytes = []
    for byte_idx in range(len(flag_bits) // 8):
        byte_val = 0
        for bit_idx in range(8):
            if flag_bits[byte_idx * 8 + bit_idx]:
                byte_val |= (1 << bit_idx)
        flag_bytes.append(byte_val)
    
    flag = bytes(flag_bytes)
    conn.close()
    log.success(f"Flag: {flag}")
    try:
        log.success(f"Flag decoded: {flag.decode()}")
    except:
        log.info(f"Flag (hex): {flag.hex()}")

if __name__ == "__main__":
    solve()
