from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256
from Crypto.Util.number import getPrime, GCD, bytes_to_long, long_to_bytes, inverse
from random import randint

p, q = (11937828783676581034379858931125102585140324472721260815335317763292864909480166621128213052274890836368799667838583870053506369497321135261063326455411669, 10791832153378244806121343863826761633315500670294598707472026045570114652554351434109171763819518428955386796330132933611585226029987715932926386870921009) 
vka = 17861197607573836317470852743261577757836195776077597552432680683466797098136864268004416983263458709262676766001801705484121426900602917823661374128795973017338811064064830745888948129754563018445340280322240329783246149494111301043358680307248355608392861091158065734798516791241711297016115223342905290485 
vkakb = 67935530955731337697826403917041420912730876047752226130944665541354451478806426192802758283489368571324137958316413684677085586326968083790248393217164858300920181830907564661482352964432246177520467471971937484415360862013908962078426400245560016377461618782911959221279509532432392897363961467392202999833 
vkb = 84242221073306245965942489642958344687371787572330245825957133351424060209731036155408429906114720003856404784037914599459176211062709584691421368556348357522054915642013274919939857077147153448830954134844703998734435265539724551134463605898582917330735987902562878223751672519585453755433575071131971464633 
c = '6fff54a0bbe33fc017dc31fd94ec0c82298d30759403e728d70b6be6622c8508044790d4e8f570fe7dfac7d8b15bd326' 
key = '6bd39a9a6846f1acf573e5830dcd9eac29722311a0ef06392c8f3c4779bc664d' 


n = p * q

# Since v = (p * randint(1, n)) % n, some values should share a factor with n
# Let's check which one
g_vka = GCD(vka, n)
g_vkakb = GCD(vkakb, n)
g_vkb = GCD(vkb, n)

print(f"GCD(vka, n) = {g_vka}")
print(f"GCD(vkakb, n) = {g_vkakb}")
print(f"GCD(vkb, n) = {g_vkb}")

# Find which prime is the common factor
if g_vka > 1:
    found_p = g_vka
    found_q = n // g_vka
elif g_vkakb > 1:
    found_p = g_vkakb
    found_q = n // g_vkakb
elif g_vkb > 1:
    found_p = g_vkb
    found_q = n // g_vkb
else:
    print("No common factor found! This shouldn't happen.")
    exit(1)

print(f"Found p = {found_p}")
print(f"Found q = {found_q}")

# Work modulo q (the other prime where vka is invertible)
# vka ≡ v * k_A (mod n)
# vkakb ≡ vka * k_B ≡ v * k_A * k_B (mod n)
# vkb ≡ v * k_B (mod n)

# Since v ≡ 0 (mod p), all these values are ≡ 0 (mod p)
# But modulo q, they're not zero (assuming GCD(k_A, q) = GCD(k_B, q) = 1)

# Work modulo q:
vka_q = vka % found_q
vkakb_q = vkakb % found_q
vkb_q = vkb % found_q

# k_B ≡ vkakb / vka (mod q)
k_B_q = (vkakb_q * inverse(vka_q, found_q)) % found_q
print(f"k_B mod q = {k_B_q}")

# v ≡ vkb / k_B (mod q)
v_q = (vkb_q * inverse(k_B_q, found_q)) % found_q
print(f"v mod q = {v_q}")

# Now we know:
# v ≡ 0 (mod p)
# v ≡ v_q (mod q)
# Use CRT to find v mod n

# v = p * x for some x
# p * x ≡ v_q (mod q)
# x ≡ v_q / p (mod q)
x = (v_q * inverse(found_p % found_q, found_q)) % found_q
v = (found_p * x) % n
print(f"v = {v}")

key = sha256(long_to_bytes(v)).digest()
print(f"Computed key: {key.hex()}")
cipher = AES.new(key, AES.MODE_ECB)

flag = unpad(cipher.decrypt(bytes.fromhex(c)), 16)
print(flag.decode())