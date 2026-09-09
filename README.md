# wordsmith
Intelligent password wordlist generator with linguistic mutations.  Transforms base words into thousands of variations using leet speak,  case mixing, and pattern appendages. Calculates entropy for each  password to rank by strength. Exports to John the Ripper and Hashcat formats.

## 🔨 What It Does

Transforms base words into thousands of password variations using:

| Technique | Example |
|-----------|---------|
| **Leet Speak** | `admin` → `adm\|n`, `@dm!n` |
| **Case Mixing** | `admin` → `ADMIN`, `Admin` |
| **Word Combinations** | `name+year+company` → `Premchand2001BikaJi` |
| **Separators** | `Premchand_BikaJi`, `2001@Premchand` |
| **Year/Number Append** | `admin2024`, `123Premchand` |
| **Special Chars** | `admin!`, `Premchand@123` |

## 🚀 Usage

```bash
# Basic - single word
python wordsmith.py -w "company" -o list.txt

# Multiple words (name, birth year, company)
python wordsmith.py -w "Premchand,2001,BikaJi" -o list.txt -l 1000

# John the Ripper format
python wordsmith.py -w "target" -o john.txt -f john -l 5000

## 📊 Example Output

Base words: ['Premchand', '2001', 'BikaJi'] Total variations: 1000 Average entropy: 71.13 bits
Top Sample passwords:
  1. premch@nd@bikaj1     (96 bits)
  2. pr3mchand_bik4ji     (96 bits)
  3. premch4nd@b1kaji     (96 bits)
  4. premch@nd!bikaj1     (96 bits)
  5. PREMCHAND_b!kaji     (96 bits)
  6. PREMCHAND!b!kaji     (96 bits)
  7. PREMCHAND_Bikaji     (96 bits)
  8. pr3mchand@bikaj!     (96 bits)
  9. premch@nd!b1kaji     (96 bits)
  10. premch@nd@BIKAJI    (96 bits)


## 🛠 Features

- **Multi-word combinations**: Cross-mutates all input words
- **Entropy calculation**: Ranks passwords by strength
- **No duplicates**: Smart deduplication
- **Export formats**: Plain, John the Ripper, Hashcat

## ⚠️ Legal

For authorized penetration testing only.

---
GitHub: mintbearsec