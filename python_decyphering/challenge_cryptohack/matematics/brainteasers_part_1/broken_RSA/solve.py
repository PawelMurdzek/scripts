# Import the long_to_bytes function from the Crypto.Util.number module
from Crypto.Util.number import long_to_bytes

# p is a large prime number, which serves as the modulus in the RSA-like scheme
p = 27772857409875257529415990911214211975844307184430241451899407838750503024323367895540981606586709985980003435082116995888017731426634845808624796292507989171497629109450825818587383112280639037484593490692935998202437639626747133650990603333094513531505209954273004473567193235535061942991750932725808679249964667090723480397916715320876867803719301313440005075056481203859010490836599717523664197112053206745235908610484907715210436413015546671034478367679465233737115549451849810421017181842615880836253875862101545582922437858358265964489786463923280312860843031914516061327752183283528015684588796400861331354873
# c is the ciphertext, which is the result of encrypting the message m (c = m^e mod p)
c = 11303174761894431146735697569489134747234975144162172162401674567273034831391936916397234068346115459134602443963604063679379285919302225719050193590179240191429612072131629779948379821039610415099784351073443218911356328815458050694493726951231241096695626477586428880220528001269746547018741237131741255022371957489462380305100634600499204435763201371188769446054925748151987175656677342779043435047048130599123081581036362712208692748034620245590448762406543804069935873123161582756799517226666835316588896306926659321054276507714414876684738121421124177324568084533020088172040422767194971217814466953837590498718
# e is the public exponent
e = 16

# This function calculates the modular square root of a number 'a' modulo a prime 'p'.
# It implements the Tonelli-Shanks algorithm.
def modular_sqrt(a, p):
    # First, check if a has a square root modulo p using the Legendre symbol.
    # If legendre_symbol(a, p) is not 1, 'a' is a quadratic non-residue and has no square root.
    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return 0
    # A simpler case for primes p congruent to 3 modulo 4.
    elif p % 4 == 3:
        return pow(a, (p + 1) // 4, p)

    # Tonelli-Shanks algorithm for other primes.
    # 1. Decompose p-1 into s * 2^e where s is odd.
    s = p - 1
    e = 0
    while s % 2 == 0:
        s //= 2
        e += 1

    # 2. Find a quadratic non-residue 'n' modulo p.
    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1

    # 3. Initialize the variables for the main loop.
    x = pow(a, (s + 1) // 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e

    # 4. Main loop of the algorithm to find the square root.
    while True:
        t = b
        m = 0
        for m in range(r):
            if t == 1:
                break
            t = pow(t, 2, p)

        if m == 0:
            return x

        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m

def legendre_symbol(a, p):
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls


for i in range(e):
    f = c
    chk = i
    for j in range(4):
        f = modular_sqrt(f, p)
        if f == 0:
            break
        if chk%2 == 1:
            f = p - f
        chk //= 2
    if f > 0:
        print(long_to_bytes(f))