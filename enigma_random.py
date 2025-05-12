import string
import random

class Enigma:
    def __init__(self, rotors, reflector, plugs):
        self.A = string.ascii_uppercase
        self.rotors = rotors
        self.refl = reflector
        self.plug = plugs
        self.pos = [0, 0, 0]

    def set_pos(self, pos):
        self.pos = pos[:]

    def process(self, text): 
        out = ''
        for c in text.upper():
            if c not in self.A: # if a character is not in the alphabet, keep them separate
                out += c
                continue
            char = self.plug.get(c, c)
            for i in range(len(self.rotors)):
                idx = (self.A.index(char) + self.pos[i]) % 26
                char = self.rotors[i][idx] # forward rotor first
            char = self.refl[char] # reflector after the firward rotor
            for i in reversed(range(len(self.rotors))):
                idx = (self.rotors[i].index(char) - self.pos[i]) % 26 # reverse rotor 
                char = self.A[idx]
            char = self.plug.get(char, char) # plugboard after the rotor 
            out += char
            self._rotate()
        return out

    def _rotate(self): #rotor rotation
        self.pos[0] += 1
        for i in range(len(self.pos)):
            if self.pos[i] >= 26:
                self.pos[i] = 0
                if i+1 < len(self.pos):
                    self.pos[i+1] += 1
            else:
                break

def make_rotor(): # randomizing the rotors
    lst = list(string.ascii_uppercase)
    random.shuffle(lst)
    return lst

def make_reflector(): # randomizing the reflector 
    alpha = list(string.ascii_uppercase)
    random.shuffle(alpha)
    reflect = {}
    for i in range(0, 26, 2):
        a, b = alpha[i], alpha[i+1]
        reflect[a], reflect[b] = b, a
    return reflect

rotor_set = [make_rotor(), make_rotor(), make_rotor()] # 3 rotors 
reflector = make_reflector()
plug = {'A': 'Y', 'Y': 'A', 'D': 'J', 'J': 'D', 'U': 'V', 'V': 'U', 'S': 'H', 'H': 'S'}
start = [0, 0, 0] # startinh from 0

print("Rotor settings:")
for idx, r in enumerate(rotor_set):
    print(f"R{idx+1}: {''.join(r)}")
print("Reflector mapping:", reflector)
print("Plugboard:", plug)
print()

enigma = Enigma(rotor_set, reflector, plug)
enigma.set_pos(start)
og = "HELLO WORLD!"
# the long messahe
# og = "The Enigma machine is a cipher device developed and used in the early- to mid-20th century to protect commercial, diplomatic, and military communication. It was employed extensively by Nazi Germany during World War II, in all branches of the German military. The Enigma machine was considered so secure that it was used to encipher the most top-secret messages. The Enigma has an electromechanical rotor mechanism that scrambles the 26 letters of the alphabet. In typical use, one person enters text on the Enigma's keyboard and another person writes down which of the 26 lights above the keyboard illuminated at each key press. If plaintext is entered, the illuminated letters are the ciphertext. Entering ciphertext transforms it back into readable plaintext. The rotor mechanism changes the electrical connections between the keys and the lights with each keypress. The security of the system depends on machine settings that were generally changed daily, based on secret key lists distributed in advance, and on other settings that were changed for each message. The receiving station would have to know and use the exact settings employed by the transmitting station to decrypt a message. Although Nazi Germany introduced a series of improvements to the Enigma over the years that hampered decryption efforts, cryptanalysis of the Enigma enabled Poland to first crack the machine as early as December 1932 and to read messages prior to and into the war. Poland's sharing of their achievements enabled the Allies to exploit Enigma-enciphered messages as a major source of intelligence. Many commentators say the flow of Ultra communications intelligence from the decrypting of Enigma, Lorenz, and other ciphers shortened the war substantially and may even have altered its outcome."

cipher = enigma.process(og)

enigma.set_pos(start)
decoded = enigma.process(cipher) #decoded is the reverse 

print("Original:", og)
print("Encoded :", cipher)
print("Decoded :", decoded)
