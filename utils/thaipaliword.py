# Define Thai subtract vowels (ส่วนของสระ ที่ไม่มี อ) เพื่ออ่านง่าย เมื่ออยู่ใน code
_i = "\u0E34"    # อิ
_ii = "\u0E35"   # อี
_u = "\u0E38"    # อุ
_uu = "\u0E39"   # อู
pintu ='\u0E3A'       # จุด พินทุ
niccahit = '\u0E4D'    # นิคคหิต
yamaga = '\u0E4E' #  ยมกะ
akasa = '\u0E31' #  ไม้หันอากาศ
sara_a = "\u0E30" # สระ ะ

# สระ ะ ไม่จัดใน vowels เพราะตอนนำเข้าไม่มีรูป สระ ะ
front_vowels = ['เ', 'โ']
back_vowels = ['า',_i,_ii,_u,_uu]
symbol_vowels = front_vowels + back_vowels
limit_letters = 'อาเโกขคฆงจฉชฌญฏฐฑฒณตถทธนปผพภมยรลวสหฬ' + _i +_ii +_u +_uu +pintu + niccahit

symbol_consonants='กขคฆงจฉชฌญฏฐฑฒณตถทธนปผพภมยรลวสหฬ'
vowels = ['อ', 'อา', 'อิ', 'อี', 'อุ', 'อู', 'เอ', 'โอ']
consonants = [
    'กฺ', 'ขฺ', 'คฺ', 'ฆฺ', 'งฺ',
    'จฺ', 'ฉฺ', 'ชฺ', 'ฌฺ', 'ญฺ',
    'ฏฺ', 'ฐฺ', 'ฑฺ', 'ฒฺ', 'ณฺ',
    'ตฺ', 'ถฺ', 'ทฺ', 'ธฺ', 'นฺ',
    'ปฺ', 'ผฺ', 'พฺ', 'ภฺ', 'มฺ',
    'ยฺ', 'รฺ', 'ลฺ', 'วฺ', 'สฺ', 'หฺ', 'ฬฺ', 'อํ'
]
thai_letters = vowels + consonants

# Define roman consonants (อักขระโรมัน)
roman_letters = [
        'a','ā','i','ī','u','ū','e','o',
        'k','kh','g','gh','ṅ',
        'c','ch','j','jh','ñ',
        'ṭ','ṭh','ḍ','ḍh','ṇ',
        't','th','d','dh','n',
        'p','ph','b','bh','m',
        'y','r','l','v','s','h','ḷ','ṃ']

base_letters = [
    '0', '1', '2', '3', '4', '5', '6', '7',
    'ก', 'ข', 'ค', 'ฆ', 'ง',
    'จ', 'ฉ', 'ช', 'ฌ', 'ญ',
    'ฏ', 'ฐ', 'ฑ', 'ฒ', 'ณ',
    'ต', 'ถ', 'ท', 'ธ', 'น',
    'ป', 'ผ', 'พ', 'ภ', 'ม',
    'ย', 'ร', 'ล', 'ว', 'ส', 'ห', 'ฬ', 'ฮ'
]

two_voice = ['ยฺ','รฺ','ลฺ','วฺ']   # กล้ำสังโยค


def is_thai_letters(word):
    # limit_letters is unique thai_letters
    return all(char in limit_letters for char in word)

def is_base_letters(word):
     return all(char in base_letters for char in word)

def is_roman_letters(word):
     return all(letter in roman_letters for letter in word)

def expander(thai):
    if thai == 'Fail':
      return 'Fail'

    x = thai + '????'
    y = ''
    i = 0
    while i < len(x)-4:
        w = x[i:i+4]
        if (w[0] == 'เ' or w[0] == 'โ') and w[1] != 'อ':
            if w[2] != pintu:
                y += w[1] + pintu + w[0]+'อ'
                i += 2
            else:
                y += w[1] + pintu + w[3] + pintu + w[0] + 'อ'
                i += 4
        elif (w[0] in symbol_consonants) and w[1] != pintu:
            y += w[0] + pintu + 'อะ'
            i+=1
        elif w[0:2] == 'อํ':
            y += 'อะอํ'
            i += 2
        elif w[0:2] in vowels:  # อย่างไร ก็ไม่มี อะ
            y += w[0:2]
            i+=2
        elif w[0] == niccahit:
            y += 'อํ'
            i+=1
        elif w[0] in back_vowels:
            y = y[:-1] + w[0]
            i+=1
        elif w[0] == 'อ' and (w[1] not in back_vowels):
            y += 'อะ'
            i+=1
        else:
            y += w[0]
            i += 1
    expanded = []
    i = 0
    while i < len(y):
      x = y[i:i+2]
      if x=='อะ':
        expanded.append('อ')
      else:
        expanded.append(x)
      i+=2
    return expanded

def shrinker(expand):  # expand เป็น list
  if expand=='Fail':
    return 'Fail'
  y = 'อ'
  for x in expand:
    if y[-1] == pintu and (x == 'เอ' or x == 'โอ'):  # มฺ-หฺ-เอ
      y = y[:-2] + x[0] + y[-2]   # มฺ-เห
    else:
      y += x
  y = y[1:]
  y = y.replace('อิอํ','อิํ')
  y = y.replace('อุอํ','อุํ')
  y = y.replace('ออํ','อํ')
  y = y.replace(pintu + 'อ', '')
  return y

def encoder(expand):

    if expand=='Fail':
      return 'Fail'

    encoded = ''
    for exp in expand:
      if exp == 'อํ':
        encoded += 'ฮ'
      elif exp in vowels:
        encoded += str(vowels.index(exp))
      elif exp in consonants:
        encoded += exp[0]
    return encoded

def decoder(base):
  if base=='Fail':
      return 'Fail'
  expand = []
  for x in base:
    if x in base_letters:
      id = base_letters.index(x)
      expand.append(thai_letters[id])
    else:
      return 'Fail'
  return expand

def to_roman(base):

    if base=='Fail':
      return 'Fail'

    roman = ''
    for b in base:
      if b in base_letters:
        id = base_letters.index(b)
        roman += roman_letters[id]
      else:
        return 'Fail'

    return roman

def to_voice(expand):
  if expand=='Fail':
      return 'Fail'
  payanks = []
  e = expand + ["?","?","?","?"]
  i = 0
  while i < len(e)-4:
    payank = []
    e0 = e[i]
    e1 = e[i+1]
    e2 = e[i+2]
    e3 = e[i+3]
    e4 = e[i+4]
    payank.append(e0)

    if e0+e1+e2+e3 == "พฺรฺอหฺ" :
      payank.extend(e[i+1:i+5])
      i+=4
    elif e1 == "อํ":
      payank.append(e1)
      i+=2
    elif e2 == "อํ":
      payank.extend(e[i+1:i+3])
      i+=3
    elif is_vowels(e0) and is_cons(e1) and not is_cons(e2):
      i+=1
    elif is_vowels(e0) and is_vowels(e1):
      i+=1
    else:

      if is_sanyoko(e1, e2):
          payank.append(e1)
          i += 1 + plus_sanyoko(e1, e2)
      elif is_cons(e1) and is_vowels(e2) and is_sanyoko(e3,e4):
          payank.extend(e[i+1:i+4])
          i += 3 + plus_sanyoko(e3, e4)
      elif is_cons(e1) and is_vowels(e2) and e3=='อํ':
          payank.extend(e[i+1:i+4])
          i+=4
      elif is_cons(e1) and is_vowels(e2):
          payank.extend(e[i+1:i+3])
          i+=3
      elif is_sanyoko(e2, e3):
          payank.extend(e[i+1:i+3])
          i += 2 + plus_sanyoko(e2, e3)
      else:
          payank.append(e1)
          i += 2
      #ถ้าตัดพยางค์ได้ แล้วหาตัวอักขระเจอ ถือว่าถูกต้อง
      #ตัวสุดท้ายต้องเป็นสระ
      #ในอนาคตจะตรวจสอบ สัญโญคด้วย ต้องซ้อนถูก ตอนนี้ข้อมูลไม่มากพอ

      if isFail(payank):
        return 'Fail'
  # หากเป็นภาษาอื่นต้องมีอีกขั้นตอนหนึ่งแต่ตอนนี้รวมไปก่อน
    payanks.append(shrinker(payank))  # คือ เอา shrinker ออก
  return payanks

def to_thai_voice(payankas):

  def adjust_payanka(payanka):
    if len(payanka) >  2 and payanka[1] == pintu:  #ถ้าตัวที่ 2 เป็น พินทุ 
        payanka = payanka[0] + yamaga + payanka[2:]  #เปลี่ยนเป็น ยมกะ
    if payanka[-1] == pintu:  
      payanka = payanka[:-1] 
      if len(payanka)==2:
        payanka = payanka[0] + akasa + payanka[1] # เพิ่มไม้หันอากาศ
      elif len(payanka)>2 and payanka[-3] not in ['เอ', 'โ']:
        payanka = payanka[:-1] + akasa + payanka[-1] # เพิ่มไม้หันอากาศ
    if niccahit in payanka:
        payanka = payanka.replace(niccahit, akasa + 'ง')
    if  len(payanka)==1:
        payanka += sara_a
    return payanka

  if payankas=='Fail':
      return 'Fail'
  else:
     return [adjust_payanka(payanka) for payanka in payankas]
  


def plus_sanyoko(s1, s2):
    return 0 if s2 in two_voice and s1 != s2 else 1

def is_sanyoko(s1, s2):
  return True  if is_cons(s1) and is_cons(s2) else False

def is_vowels(v):
  return True  if v in vowels else False

def is_cons(cons):
  return True  if cons in consonants and cons != 'อํ' else False

def isFail(payank):
    return True if any(p not in thai_letters for p in payank) else False

def to_base(roman):
  base = ''
  i = 0
  while i < len(roman):
      # ตรวจสอบสำหรับอักษรที่มีความยาว 2 ตัวอักษร เช่น 'th', 'kh', 'gh' ฯลฯ
      if i < len(roman) - 1 and roman[i:i+2] in roman_letters:
          base += base_letters[roman_letters.index(roman[i:i+2])]
          i += 2
      elif roman[i] in roman_letters:
          base += base_letters[roman_letters.index(roman[i])]
          i += 1
      else:
          return 'Fail'  # ถ้าพบอักษรที่ไม่รู้จัก
  return base

class ThaiPaliWord:
  # create word 3 rule
  # from encode thai roman
  def __init__(self, word, source):

    if source == 'thai':
      self.thai = word if is_thai_letters(word) else 'Fail'
    elif source == 'base':
      self.thai = shrinker(decoder(word)) if is_base_letters(word) else 'Fail'
    elif source == 'roman':
      if is_roman_letters(word):
        self.base = to_base(word)
        self.thai = shrinker(decoder(self.base))
      else:
        self.thai = 'Fail'
    self.expand = expander(self.thai)
    self.voice = to_voice(self.expand)
    self.thai_voice = to_thai_voice(self.voice)

    if self.voice=='Fail':
      self.expand = 'Fail'
      self.base = word if source == 'base' else 'Fail'
      self.thai = word if source == 'thai' else 'Fail'
      self.roman = word if source == 'roman' else 'Fail'

    else:
      self.base = encoder(self.expand)
      self.roman = to_roman(self.base)

  def isPali(self):
      return self.base != 'Fail'
  def display(self):
    
    a = f"roman: (บาลีอักขระโรมัน) {self.roman}\n"
    b = f"base: (บาลี basecode): {self.base}\n"
    c = f"expand (บาลีอักขระไทย-ขยาย):  {'-'.join(self.expand)}\n"
    d = f"thai: (บาลีอักขระไทย-ลด)  {self.thai}\n"
    e = f"voice: (บาลีอักขระไทย-อ่าน): {'-'.join(self.voice)}\n"
    f = f"thai_write (บาลีเขียนไทย): {''.join(self.thai_voice)}\n"
    g = f"thai_voice (บาลีเขียนไทย-อ่าน){self.thai_voice}\n"
    print(a+b+c+d+e+f+g)
