#!/usr/bin/env python3
"""
Wordsmith - Intelligent Password Mutation Engine
Generates realistic password patterns that humans actually use.
"""

import itertools
import random
import string
import os
from typing import List, Tuple, Set
import click
from tqdm import tqdm


class Wordsmith:
    """Realistic password wordlist generator."""
    
    LEET_MAP = {
        'a': ['@', '4'],
        'e': ['3'],
        'i': ['1', '!'],
        'l': ['1'],
        'o': ['0'],
        's': ['$', '5'],
        't': ['7']
    }
    
    YEARS = ['2024', '2025', '2023', '2022', '2021', '2020', 
             '2019', '2018', '2000', '1999', '1998', '1995',
             '123', '1234', '007', '01', '001']
    
    NUMBERS = ['1', '12', '123', '1234', '01', '001', '111', '000',
               '69', '77', '88', '99', '00', '007', '666']
    
    SPECIALS = ['!', '@', '#', '$', '!!', '@@', '##', '123!', '1!']
    
    def __init__(self, base_words: List[str]):
        self.base_words = [w.strip() for w in base_words if w.strip()]
        
    def entropy(self, password: str) -> float:
        if not password:
            return 0.0
            
        pool = 0
        if any(c in string.ascii_lowercase for c in password):
            pool += 26
        if any(c in string.ascii_uppercase for c in password):
            pool += 26
        if any(c in string.digits for c in password):
            pool += 10
        if any(c in string.punctuation for c in password):
            pool += len(string.punctuation)
            
        if pool == 0:
            return 0.0
            
        return round(len(password) * (pool.bit_length() - 1), 2)
    
    def _leet(self, word: str) -> List[str]:
        """Simple leet substitutions."""
        word_lower = word.lower()
        variations = {word, word_lower}
        
        # Single char substitution
        for i, char in enumerate(word_lower):
            if char in self.LEET_MAP:
                for sub in self.LEET_MAP[char]:
                    variations.add(word_lower[:i] + sub + word_lower[i+1:])
                    
        return list(variations)
    
    def _case(self, word: str) -> List[str]:
        """Case variations."""
        return list({
            word.lower(),
            word.capitalize(),
            word.upper()
        })
    
    def _mutate_word(self, word: str) -> Set[str]:
        """Generate mutations for a single word."""
        mutations = set()
        
        # Case variations
        for cased in self._case(word):
            mutations.add(cased)
            # Leet on each case
            for leeted in self._leet(cased):
                mutations.add(leeted)
                
        return mutations
    
    def _single_word_patterns(self, word: str) -> Set[str]:
        """Realistic patterns for ONE word (most common)."""
        patterns = set()
        base_mutations = self._mutate_word(word)
        
        for base in base_mutations:
            # Just the word
            patterns.add(base)
            
            # Word + number
            for num in self.NUMBERS:
                patterns.add(base + num)
                patterns.add(num + base)
                
            # Word + year
            for year in self.YEARS:
                patterns.add(base + year)
                patterns.add(year + base)
                
            # Word + special
            for special in self.SPECIALS:
                patterns.add(base + special)
                
            # Word + number + special
            for num in ['123', '1', '01', '007']:
                for special in ['!', '@', '#']:
                    patterns.add(base + num + special)
                    patterns.add(base + special + num)
                    
        return patterns
    
    def _two_word_patterns(self, word1: str, word2: str) -> Set[str]:
        """Realistic patterns for TWO words (less common)."""
        patterns = set()
        
        mut1 = self._mutate_word(word1)
        mut2 = self._mutate_word(word2)
        
        for m1 in mut1:
            for m2 in mut2:
                # Direct concat (shorter is better)
                if len(m1) + len(m2) <= 15:
                    patterns.add(m1 + m2)
                    patterns.add(m2 + m1)
                    
                # With separator
                patterns.add(m1 + '@' + m2)
                patterns.add(m1 + '_' + m2)
                patterns.add(m1 + '!' + m2)
                
                # One word + year from other (if word2 is numeric-like)
                if m2.isdigit() or len(m2) == 4:
                    patterns.add(m1 + m2)
                    
        return patterns
    
    def forge(self, max_variations: int = 10000) -> List[Tuple[str, float]]:
        """Generate realistic password wordlist."""
        print(f"Forging wordlist from: {self.base_words}")
        
        all_passwords = set()
        
        # PRIORITY 1: Single word patterns (most realistic, 70% of passwords)
        for word in self.base_words:
            single_patterns = self._single_word_patterns(word)
            all_passwords.update(single_patterns)
            
        # PRIORITY 2: Two-word combinations (moderate, 25% of passwords)
        if len(self.base_words) >= 2:
            for i in range(len(self.base_words)):
                for j in range(i + 1, len(self.base_words)):
                    two_patterns = self._two_word_patterns(
                        self.base_words[i], 
                        self.base_words[j]
                    )
                    all_passwords.update(two_patterns)
                    
                if len(all_passwords) >= max_variations * 2:
                    break
        
        # PRIORITY 3: Three-word (rare, only if space left)
        if len(self.base_words) >= 3 and len(all_passwords) < max_variations:
            # Only shortest combinations
            short_words = sorted(self.base_words, key=len)[:3]
            combo = ''.join(w[:4] for w in short_words)  # Truncate
            all_passwords.add(combo)
            all_passwords.add('_'.join(short_words))
        
        # Filter: realistic length (6-20 chars)
        realistic = {p for p in all_passwords if 6 <= len(p) <= 20}
        
        # Calculate entropy and sort
        result = [(pwd, self.entropy(pwd)) for pwd in realistic]
        result.sort(key=lambda x: x[1], reverse=True)
        
        return result[:max_variations]
    
    def export(self, variations: List[Tuple[str, float]], filename: str, 
               format_type: str = 'plain') -> bool:
        try:
            filepath = os.path.abspath(filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                if format_type == 'john':
                    f.write("# John the Ripper wordlist\n")
                elif format_type == 'hashcat':
                    f.write("# Hashcat wordlist\n")
                
                for pwd, _ in variations:
                    f.write(f"{pwd}\n")
                        
            if os.path.exists(filepath):
                print(f"✓ Exported {len(variations)} passwords to {filepath}")
                return True
            return False
                
        except Exception as e:
            print(f"✗ Export error: {e}")
            return False


@click.command()
@click.option('--words', '-w', required=True, 
              help='Comma-separated base words (e.g., "name,year,company")')
@click.option('--output', '-o', default='wordlist.txt',
              help='Output filename')
@click.option('--limit', '-l', default=10000,
              help='Maximum variations')
@click.option('--format', '-f', 'fmt', default='plain',
              type=click.Choice(['plain', 'john', 'hashcat']))
def main(words, output, limit, fmt):
    print("=" * 60)
    print("WORDSMITH")
    print("Realistic Password Mutation Engine")
    print("=" * 60)
    
    base_words = [w.strip() for w in words.split(',')]
    print(f"\nBase words: {base_words}")
    
    smith = Wordsmith(base_words)
    variations = smith.forge(max_variations=limit)
    
    print(f"\n{'=' * 60}")
    print("RESULTS")
    print(f"{'=' * 60}")
    print(f"Total variations: {len(variations)}")
    
    if variations:
        entropies = [e for _, e in variations]
        print(f"Average entropy: {sum(entropies)/len(entropies):.2f} bits")
        print(f"Highest: {max(entropies):.2f} bits ({variations[0][0]})")
        print(f"Lowest: {min(entropies):.2f} bits ({variations[-1][0]})")
        
        print(f"\nSample passwords:")
        for i, (pwd, ent) in enumerate(variations[:15], 1):
            print(f"  {i}. {pwd:<20} ({ent:.0f} bits)")
    
    success = smith.export(variations, output, fmt)
    
    print(f"\n{'=' * 60}")
    print("COMPLETE" if success else "FAILED")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    main()