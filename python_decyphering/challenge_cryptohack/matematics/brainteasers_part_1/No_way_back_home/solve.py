from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from hashlib import sha256
from Crypto.Util.number import long_to_bytes, inverse, bytes_to_long

# These are the values from your out.txt file
p = 10699940648196411028170713430726559470427113689721202803392638457920771439452897032229838317321639599506283870585924807089941510579727013041135771337631951
q = 11956676387836512151480744979869173960415735990945471431153245263360714040288733895951317727355037104240049869019766679351362643879028085294045007143623763
vka = 12464174196712130006824128097140830662505063626119265584527449469538248489497399089901898143882439888598400388066533533687284981998304579047816690938196894991071790613647584256820864020381176607982536497416854119898887903699748913002215135285877655517844457677074095521488219905950926757695656018450299948207
vkakb = 114778245184091677576134046724609868204771151111446457870524843414356897479473739627212552495413311985409829523700919603502616667323311977056345059189257932050632105761365449853358722065048852091755612586569454771946427631498462394616623706064561443106503673008210435922340001958432623802886222040403262923652
vkb = 6568897840127713147382345832798645667110237168011335640630440006583923102503659273104899584827637961921428677335180620421654712000512310008036693022785945317428066257236409339677041133038317088022368203160674699948914222030034711433252914821805540365972835274052062305301998463475108156010447054013166491083
c = 'fef29e5ff72f28160027959474fc462e2a9e0b2d84b1508f7bd0e270bc98fac942e1402aa12db6e6a36fb380e7b53323'
n = p * q

print("Starting solver script...")
print(f"p = {p}")
print(f"q = {q}")

# 1. Find v mod q
# From the original script, modulo q:
#   vka = v * k_A (mod q)
#   vkb = v * k_B (mod q)
#   vkakb = v * k_A * k_B (mod q)
#
# If we multiply vka and vkb:
#   (vka * vkb) = (v^2 * k_A * k_B) (mod q)
#
# Now, if we divide this by vkakb (i.e., multiply by its inverse):
#   (vka * vkb * inverse(vkakb, q)) = (v^2 * k_A * k_B * inverse(v * k_A * k_B, q)) (mod q)
#   This simplifies to v (mod q).
#
# So, v_q = (vka * vkb * inverse(vkakb, q)) % q

try:
    # Calculate v_q (v mod q)
    vka_mod_q = vka % q
    vkb_mod_q = vkb % q
    vkakb_mod_q = vkakb % q
    
    inv_vkakb_mod_q = inverse(vkakb_mod_q, q)
    
    v_q = (vka_mod_q * vkb_mod_q * inv_vkakb_mod_q) % q
    print(f"\nSuccessfully calculated v_q (v mod q): {v_q}")

    # 2. Use Chinese Remainder Theorem (CRT) to find v
    # We have the system:
    #   v = 0 (mod p)
    #   v = v_q (mod q)
    #
    # The solution v is given by:
    #   v = (0 * q * inverse(q, p) + v_q * p * inverse(p, q)) % n
    #   v = (v_q * p * inverse(p, q)) % n
    
    inv_p_mod_q = inverse(p, q)
    
    # We can use (p*q) or n as the final modulus
    v = (v_q * p * inv_p_mod_q) % n
    print(f"\nSuccessfully recovered v: {v}")

    # 3. Derive the AES key from v
    v_bytes = long_to_bytes(v)
    key = sha256(v_bytes).digest()
    print(f"\nDerived AES key (hex): {key.hex()}")

    # 4. Decrypt the ciphertext c
    c_bytes = bytes.fromhex(c)
    cipher = AES.new(key, AES.MODE_ECB)
    
    padded_flag = cipher.decrypt(c_bytes)
    
    # 5. Unpad and print the flag
    try:
        flag = unpad(padded_flag, 16)
        print("\nDecryption successful!")
        print("========================================")
        print(f"FLAG: {flag.decode()}")
        print("========================================")
    except ValueError as e:
        print(f"\nDecryption worked, but unpadding failed: {e}")
        print("This might mean the key is wrong, or the padding is corrupt.")
        print(f"Padded flag (hex): {padded_flag.hex()}")

except Exception as e:
    print(f"\nAn error occurred: {e}")
    print("This could be due to a modular inverse not existing (e.g., if vkakb_mod_q is 0).")

