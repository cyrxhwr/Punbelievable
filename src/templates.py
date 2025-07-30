from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

# Initialize lemmatizer for morphological processing
lemmatizer = WordNetLemmatizer()

class GrammaticalTemplate:
    """Enhanced template class with automatic grammatical correction capabilities."""
    
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        # Cache for performance
        self._verb_cache = {}
        self._pos_cache = {}
    
    def _get_wordnet_pos(self, treebank_tag):
        """Convert treebank POS tag to WordNet POS tag."""
        if treebank_tag.startswith('J'):
            return wn.ADJ
        elif treebank_tag.startswith('V'):
            return wn.VERB
        elif treebank_tag.startswith('N'):
            return wn.NOUN
        elif treebank_tag.startswith('R'):
            return wn.ADV
        else:
            return wn.NOUN  # Default to noun
    
    def _analyze_word_pos(self, word):
        """Analyze the part of speech of a word using NLTK POS tagging."""
        if word in self._pos_cache:
            return self._pos_cache[word]
        
        # Get POS tag
        tokens = word_tokenize(word.lower())
        if tokens:
            pos_tags = pos_tag(tokens)
            pos_tag_result = pos_tags[0][1] if pos_tags else 'NN'
            wordnet_pos = self._get_wordnet_pos(pos_tag_result)
            self._pos_cache[word] = (pos_tag_result, wordnet_pos)
            return pos_tag_result, wordnet_pos
        return 'NN', wn.NOUN
    
    def _find_verb_form_automatic(self, word):
        """Automatically find the verb form of a word using WordNet and morphological analysis."""
        if word in self._verb_cache:
            return self._verb_cache[word]
        
        word = word.strip().lower()
        
        # Strategy 1: Check if it's already a verb
        verb_synsets = wn.synsets(word, pos=wn.VERB)
        if verb_synsets:
            conjugated = self._conjugate_verb_automatic(word)
            self._verb_cache[word] = conjugated
            return conjugated
        
        # Strategy 2: Use WordNet derivational relationships
        verb_form = self._find_related_verb_wordnet(word)
        if verb_form:
            conjugated = self._conjugate_verb_automatic(verb_form)
            self._verb_cache[word] = conjugated
            return conjugated
        
        # Strategy 3: Morphological analysis for -ing forms
        if word.endswith('ing'):
            base_form = self._extract_base_from_ing(word)
            if base_form and wn.synsets(base_form, pos=wn.VERB):
                conjugated = self._conjugate_verb_automatic(base_form)
                self._verb_cache[word] = conjugated
                return conjugated
        
        # Strategy 4: Try lemmatization with different POS assumptions
        for pos in [wn.VERB, wn.NOUN]:
            lemma = self.lemmatizer.lemmatize(word, pos=pos)
            if lemma != word and wn.synsets(lemma, pos=wn.VERB):
                conjugated = self._conjugate_verb_automatic(lemma)
                self._verb_cache[word] = conjugated
                return conjugated
        
        # Strategy 5: Check for common morphological patterns
        verb_form = self._apply_morphological_patterns(word)
        if verb_form:
            self._verb_cache[word] = verb_form
            return verb_form
        
        # Fallback: Create descriptive phrase
        fallback = f"has {word}" if not word.endswith('ing') else f"does {word}"
        self._verb_cache[word] = fallback
        return fallback
    
    def _find_related_verb_wordnet(self, word):
        """Find related verb forms using WordNet derivational relationships."""
        # Get all synsets for the word
        synsets = wn.synsets(word)
        
        for synset in synsets:
            for lemma in synset.lemmas():
                # Check derivationally related forms
                for related_lemma in lemma.derivationally_related_forms():
                    if related_lemma.synset().pos() == 'v':
                        return related_lemma.name().replace('_', ' ')
                
                # Check pertainyms (for adjectives)
                for pertainym in lemma.pertainyms():
                    if pertainym.synset().pos() == 'v':
                        return pertainym.name().replace('_', ' ')
        
        return None
    
    def _extract_base_from_ing(self, word):
        """Extract base verb from -ing form using morphological rules."""
        if not word.endswith('ing') or len(word) <= 3:
            return None
        
        base = word[:-3]
        
        # Handle doubled consonants (running -> run, swimming -> swim)
        if (len(base) >= 2 and 
            base[-1] == base[-2] and 
            base[-1] not in 'aeiouwxy' and
            len(base) >= 3):
            # Check if the doubled form makes sense
            single_base = base[:-1]
            if wn.synsets(single_base, pos=wn.VERB):
                return single_base
        
        # Handle e-dropping (making -> make, writing -> write)
        e_base = base + 'e'
        if wn.synsets(e_base, pos=wn.VERB):
            return e_base
        
        # Try the base as-is
        if wn.synsets(base, pos=wn.VERB):
            return base
        
        return None
    
    def _apply_morphological_patterns(self, word):
        """Apply common morphological patterns to find verb forms."""
        # Pattern 1: -er/-or endings (often agent nouns)
        if word.endswith(('er', 'or')):
            base = word[:-2]
            if wn.synsets(base, pos=wn.VERB):
                return self._conjugate_verb_automatic(base)
        
        # Pattern 2: -tion/-sion endings (often action nouns)
        if word.endswith('tion'):
            # action -> act, creation -> create
            base = word[:-4]
            if base.endswith('a'):
                base = base[:-1]  # creation -> creat -> create
            base += 'e' if not base.endswith('e') else ''
            if wn.synsets(base, pos=wn.VERB):
                return self._conjugate_verb_automatic(base)
        
        if word.endswith('sion'):
            # decision -> decide, division -> divide
            base = word[:-4]
            # Try common patterns
            for suffix in ['de', 'd', '']:
                test_base = base + suffix
                if wn.synsets(test_base, pos=wn.VERB):
                    return self._conjugate_verb_automatic(test_base)
        
        # Pattern 3: -ment endings (often result nouns)
        if word.endswith('ment'):
            base = word[:-4]
            if wn.synsets(base, pos=wn.VERB):
                return self._conjugate_verb_automatic(base)
        
        # Pattern 4: -al endings (often adjectives that can be verbs)
        if word.endswith('al'):
            base = word[:-2]
            if wn.synsets(base, pos=wn.VERB):
                return self._conjugate_verb_automatic(base)
        
        return None
    
    def _conjugate_verb_automatic(self, verb):
        """Automatically conjugate verb to third person singular using morphological rules."""
        verb = verb.strip().lower()
        
        # Check if it's already conjugated
        if verb.endswith('s') and len(verb) > 1:
            # Try to see if the base form exists
            base = verb[:-1]
            if wn.synsets(base, pos=wn.VERB):
                return verb  # Already conjugated
        
        # Handle irregular verbs using WordNet and morphological analysis
        # Get the lemma form first
        lemma = self.lemmatizer.lemmatize(verb, pos=wn.VERB)
        
        # Apply conjugation rules
        if lemma.endswith('y') and len(lemma) > 1 and lemma[-2] not in 'aeiou':
            return lemma[:-1] + 'ies'  # try -> tries, fly -> flies
        elif lemma.endswith(('s', 'sh', 'ch', 'x', 'z')):
            return lemma + 'es'  # pass -> passes, wash -> washes
        elif lemma.endswith('o') and len(lemma) > 1 and lemma[-2] not in 'aeiou':
            return lemma + 'es'  # go -> goes, do -> does
        elif lemma in ['be']:
            return 'is'
        elif lemma in ['have']:
            return 'has'
        elif lemma in ['do']:
            return 'does'
        else:
            return lemma + 's'  # most regular verbs
    
    def _create_verb_phrase(self, word):
        """Convert a word to an appropriate verb phrase for the template."""
        if not word:
            return "does something"
        
        # Clean the word
        word = str(word).strip().lower()
        
        # Use automatic verb finding
        return self._find_verb_form_automatic(word)

# Initialize the grammatical template processor
grammar_processor = GrammaticalTemplate()

def cereal_killer(l1, l2, ans):
    """Enhanced cereal killer template with automatic grammatical correction."""
    # This function is kept for compatibility but not used in the new interface
    # Clean inputs
    l1 = str(l1).strip() if l1 else "thing"
    l2 = str(l2).strip() if l2 else "something"
    ans = str(ans).strip() if ans else "unknown"
    
    # Convert l2 to appropriate verb phrase automatically
    verb_phrase = grammar_processor._create_verb_phrase(l2)
    
    # Create grammatically correct question
    print(f"\nWhat do you call a {l1} that {verb_phrase}? A {ans}")

def main():
    # Test the automatic grammatical correction
    print("Testing automatic grammatical correction:")
    
    # Test various word types
    test_cases = [
        ("mill", "meeting", "meet grinder"),
        ("person", "call", "serial caller"),
        ("machine", "grind", "meat grinder"),
        ("animal", "hunt", "deer hunter"),
        ("device", "computing", "computer"),
        ("tool", "cutting", "cutter"),
        ("person", "teaching", "teacher"),
        ("machine", "washing", "washer"),
        ("animal", "flying", "flyer"),
        ("person", "running", "runner")
    ]
    
    for l1, l2, ans in test_cases:
        cereal_killer(l1, l2, ans)

if __name__ == "__main__":
    main()