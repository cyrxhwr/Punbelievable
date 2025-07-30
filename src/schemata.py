from nltk.corpus import cmudict
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
from nltk.corpus.reader.wordnet import information_content
import string
import templates as tmp
import random
import time
import sys

# Maximum number of related words to process for efficiency
MAX_RELATED_WORDS = 200
# Maximum number of puns to find before stopping
MAX_PUNS_TO_FIND = 10
# Minimum semantic similarity threshold
MIN_SIMILARITY_THRESHOLD = 0.3

class Lotus():
  # What kind of murderer has fiber? A cereal killer.
  def __init__(self, input_word=None):
    self.nplist = self.nounPhrase()
    self.input_word = input_word
    self.found_puns = []
    
    # Build frequency distribution for semantic similarity calculations
    self.freq_dist = self._build_frequency_distribution()
    
    if input_word:
      self.generate_themed_pun(input_word)
    else:
      self.generate_random_pun()
    
  def _build_frequency_distribution(self):
    """Build a frequency distribution from Brown corpus for semantic calculations."""
    try:
      from nltk.probability import FreqDist
      words = [word.lower() for word in brown.words() if word.isalpha()]
      return FreqDist(words)
    except:
      # Fallback if Brown corpus is not available
      return None
      
  def semantic_similarity(self, word1, word2):
    """Calculate semantic similarity between two words using multiple methods."""
    if not word1 or not word2:
      return 0.0
      
    # Method 1: WordNet-based path similarity
    wordnet_sim = self._wordnet_similarity(word1, word2)
    
    # Method 2: Information content similarity using corpus frequencies
    ic_sim = self._information_content_similarity(word1, word2)
    
    # Method 3: Relationship-based similarity
    rel_sim = self._relationship_similarity(word1, word2)
    
    # Combine similarities with weights
    combined_sim = (wordnet_sim * 0.4 + ic_sim * 0.3 + rel_sim * 0.3)
    
    return min(combined_sim, 1.0)
    
  def _wordnet_similarity(self, word1, word2):
    """Calculate WordNet path similarity."""
    try:
      synsets1 = wn.synsets(word1, pos=wn.NOUN)
      synsets2 = wn.synsets(word2, pos=wn.NOUN)
      
      if not synsets1 or not synsets2:
        return 0.0
        
      max_sim = 0.0
      for s1 in synsets1[:3]:  # Consider top 3 senses
        for s2 in synsets2[:3]:
          sim = s1.path_similarity(s2)
          if sim and sim > max_sim:
            max_sim = sim
            
      return max_sim
    except:
      return 0.0
      
  def _information_content_similarity(self, word1, word2):
    """Calculate similarity based on information content."""
    if not self.freq_dist:
      return 0.0
      
    try:
      import math
      # Get frequency counts
      freq1 = self.freq_dist.get(word1.lower(), 1)
      freq2 = self.freq_dist.get(word2.lower(), 1)
      
      # Calculate information content (negative log probability)
      total_words = self.freq_dist.N()
      ic1 = -math.log(freq1 / total_words)
      ic2 = -math.log(freq2 / total_words)
      
      # Similarity is inverse of distance between information contents
      ic_distance = abs(ic1 - ic2)
      return max(0.0, 1.0 - (ic_distance / 10.0))  # Normalize
    except:
      return 0.0
      
  def _relationship_similarity(self, word1, word2):
    """Calculate similarity based on semantic relationships."""
    try:
      # Check for shared hypernyms (common categories)
      synsets1 = wn.synsets(word1, pos=wn.NOUN)
      synsets2 = wn.synsets(word2, pos=wn.NOUN)
      
      for s1 in synsets1[:2]:
        for s2 in synsets2[:2]:
          # Check if they share hypernyms at different levels
          hyp1 = set(s1.hypernyms())
          hyp2 = set(s2.hypernyms())
          
          if hyp1.intersection(hyp2):
            return 0.6  # Share immediate hypernyms
            
          # Check second-level hypernyms
          hyp1_2 = set()
          hyp2_2 = set()
          for h in hyp1:
            hyp1_2.update(h.hypernyms())
          for h in hyp2:
            hyp2_2.update(h.hypernyms())
            
          if hyp1_2.intersection(hyp2_2):
            return 0.4  # Share second-level hypernyms
            
      return 0.0
    except:
      return 0.0

  def generate_random_pun(self):
    """Generate a random pun without theme constraints."""
    for npLex in self.nplist:
      # Lexical Preconditions
      self.homophone, npLex, self.np2 = self.lexical_preconds(npLex)
      if not self.homophone:
        continue
      # SAD description - generating the question
      self.qWords = self.sadGen(self.homophone, npLex)
      if not self.qWords[0] or not self.qWords[1]:
        continue
      # Relationships - generating the answer
      retval = self.relationships(self.qWords, self.np2)
      if not retval:
        continue
      break  # Stop after first successful pun
  
  def generate_themed_pun(self, theme_word):
    """Generate puns related to the theme word using semantic similarity."""
    # Find words related to the theme word (silently)
    related_words = self.find_related_words(theme_word)
    
    # Quick direct match search first (most efficient)
    direct_matches = self._find_direct_matches(theme_word, related_words)
    
    if direct_matches:
      # Try to generate puns from direct matches first
      if self._try_generate_puns(direct_matches[:50], "direct match", silent=True):
        return
    
    # If no direct matches worked, try semantic similarity approach
    scored_compounds = []
    compounds_processed = 0
    max_compounds_to_check = 10000  # Limit for efficiency
    
    for npLex in self.nplist[:max_compounds_to_check]:
      compounds_processed += 1
      
      comp_lex = self.splitLexemes(npLex)
      
      # Calculate relevance score for this compound
      relevance_score = self._calculate_compound_relevance(theme_word, comp_lex, related_words)
      
      if relevance_score >= MIN_SIMILARITY_THRESHOLD:
        scored_compounds.append((npLex, relevance_score))
    
    # Sort by relevance score (highest first)
    scored_compounds.sort(key=lambda x: x[1], reverse=True)
    
    if len(scored_compounds) > 0:
      # Try to generate puns from scored compounds
      if self._try_generate_puns([item[0] for item in scored_compounds], "semantic similarity", silent=True):
        return
    
    # If we get here, no pun was found
    print("Hmm, I couldn't come up with a good pun for that theme. Try another word!")

  def _find_direct_matches(self, theme_word, related_words):
    """Find compound words that directly contain theme-related words."""
    matches = []
    theme_set = set([theme_word.lower()] + [w.lower() for w in related_words[:30]])
    
    for npLex in self.nplist:
      comp_lex = self.splitLexemes(npLex)
      
      # Check for direct word matches
      for part in comp_lex:
        if part.lower() in theme_set:
          matches.append(npLex)
          break
    
    return matches

  def _try_generate_puns(self, compound_list, method_name, silent=False):
    """Try to generate puns from a list of compounds."""
    found_pun = False
    failed_attempts = 0
    attempts = 0
    max_attempts = min(100, len(compound_list))  # Limit attempts
    
    for npLex in compound_list[:max_attempts]:
      attempts += 1
      
      # Try to create a pun from this compound
      homophone, temp_npLex, np2 = self.lexical_preconds(npLex)
      if not homophone:
        failed_attempts += 1
        continue
      
      # SAD description - generating the question
      qWords = self.sadGen(homophone, npLex)
      if not qWords[0] or not qWords[1]:
        failed_attempts += 1
        continue
      
      # Successfully generated a pun!
      self._display_pun_with_countdown(qWords, np2)
      found_pun = True
      break
    
    return found_pun

  def _display_pun_with_countdown(self, qWords, np2):
    """Display the pun with a countdown reveal."""
    # Display the question
    question = f"What do you call a {qWords[0]} that {tmp.grammar_processor._create_verb_phrase(qWords[1])}?"
    print(f"\n{question}")
    
    # Countdown
    print("\n", end="")
    for i in range(3, 0, -1):
      print(f"{i}...", end="", flush=True)
      time.sleep(1)
    
    # Reveal answer
    print(f"\nA {np2}!")

  def _calculate_compound_relevance(self, theme_word, compound_parts, related_words):
    """Calculate how relevant a compound noun is to the theme."""
    max_relevance = 0.0
    
    # Check relevance of each part of the compound
    for part in compound_parts:
      # Direct theme word match
      if part.lower() == theme_word.lower():
        max_relevance = max(max_relevance, 1.0)
        continue
        
      # Match with related words
      for related_word in related_words:
        if part.lower() == related_word.lower():
          max_relevance = max(max_relevance, 0.9)
          continue
          
      # Semantic similarity with theme word
      similarity = self.semantic_similarity(theme_word, part)
      max_relevance = max(max_relevance, similarity)
      
      # Semantic similarity with related words
      for related_word in related_words[:20]:  # Check top 20 related words
        similarity = self.semantic_similarity(related_word, part)
        max_relevance = max(max_relevance, similarity * 0.8)  # Discount indirect similarity
        
    return max_relevance

  def find_related_words(self, word):
    """Find words related to the input word using comprehensive semantic relationships."""
    related = set()
    
    # Add the original word
    related.add(word.lower())
    
    # Get all synsets for the word
    synsets = wn.synsets(word, pos=wn.NOUN)
    
    for synset in synsets[:3]:  # Focus on top 3 most common senses
      # Add synonyms
      for lemma in synset.lemmas():
        related.add(lemma.name().lower())
      
      # Add hypernyms (more general terms) - multiple levels
      hypernyms = synset.hypernyms()
      for hypernym in hypernyms:
        for lemma in hypernym.lemmas():
          related.add(lemma.name().lower())
          
        # Add second-level hypernyms for broader context
        for hyp2 in hypernym.hypernyms():
          for lemma in hyp2.lemmas():
            related.add(lemma.name().lower())
      
      # Add hyponyms (more specific terms)
      for hyponym in synset.hyponyms():
        for lemma in hyponym.lemmas():
          related.add(lemma.name().lower())
      
      # Add meronyms (parts)
      for meronym in synset.part_meronyms() + synset.member_meronyms() + synset.substance_meronyms():
        for lemma in meronym.lemmas():
          related.add(lemma.name().lower())
      
      # Add holonyms (wholes that this is part of)
      for holonym in synset.part_holonyms() + synset.member_holonyms() + synset.substance_holonyms():
        for lemma in holonym.lemmas():
          related.add(lemma.name().lower())
    
    # Remove multi-word terms and convert to list
    filtered_related = [w for w in related if '_' not in w and len(w) > 2]
    
    return filtered_related
  
  def is_related(self, word1, word2):
    """Check if word1 is related to word2 using semantic similarity."""
    return self.semantic_similarity(word1, word2) >= MIN_SIMILARITY_THRESHOLD

  def lexical_preconds(self, np):
    # Performs the Lexical Preconditions
    compLex = self.splitLexemes(np)
    homophone = self.getHomophone(compLex[0])
    if not homophone:
      return 0,0,0
    #print self.homophone[0]
    np2 = homophone + " " + compLex[1]
    #qWords = self.sadGen(homophone, np)
    return homophone, np, np2

  def relationships(self, qWords, np):
    # Passes the question keywords and the punny word into a template
    if not qWords or not np:
      #print 'qWords and/or np undefined'
      return 0
    tmp.cereal_killer(qWords[0],qWords[1],np)
    return 1
  
  def sadGen(self, homophone, np):
    # Get hypernym of np (murderer)
    # Get meronym of homophone (grains)
    # I now have my question keywords
    if not homophone or not np:
      #print 'homophone and/or np undefined'
      return [[],[]]
    hypernym = self.getHypernym(np)
    meronym = self.getMeronym(homophone)
    # Haven't tested this yet, but should eliminate
    # errant Synset notation in output
    if isinstance(meronym, list):
      meronym = meronym[0]
    if not hypernym or not meronym:
      #print 'Hypernym and/or meronym not found'
      return [[],[]]
    return [hypernym, meronym]

  def nounPhrase(self):
    # Finds a compound lexeme in WordNet, returns lemma/list of lemmas
    compNoms = []
    for synset in list(wn.all_synsets('n')):
      compNoms.extend([x.name() for x in synset.lemmas() if x.name().count('_')==1 and x.name() != []])
    return compNoms

  def splitLexemes(self, nounPhrase):
    # Splits nounPhrase into component lexemes
    return nounPhrase.split('_')

  def getHomophone(self, wordA):
    # Finds a homophone of wordA
    phones = cmudict.dict()
    phone1 = []
    if wordA not in phones.keys():
      return 0
    phone1.extend(phones[wordA])
    phoneLst = []
    for i in phones.keys():
      if [a for a in phone1 if a in phones[i] and i != wordA]:
        phoneLst.append(i)
    if not phoneLst:
      #print 'No homophone found for ' + wordA
      return False
    return phoneLst[0]

  def getHypernym(self,np):
    # Gets most frequent hypernym of np
    # If this fails, exit the current call to getHypernym
    try:
      synsets = wn.synsets(np)
      if not synsets:
        return False
      hypernyms = synsets[0].hypernyms()
      if not hypernyms:
        return False
      return hypernyms[0].lemmas()[0].name()
    except:
      return False

  def getMeronym(self, homophone):
    # Gets meronym of homophone
    syn = wn.synsets(homophone)
    if not syn:
      #print 'No synset found for homophone'
      return False
    lst = [i.member_meronyms() for i in syn if i.member_meronyms()]
    if not lst:
      lst = [i.substance_meronyms() for i in syn if i.substance_meronyms()]
      if not lst:
        lst = [i.part_meronyms() for i in syn if i.substance_meronyms()]
        if not lst:
          #print 'Can\'t find any meronyms directly'
          # Can't find any meronyms of syn, invoke last-resort: find a synonym
          # that is not the string homophone
          translator = str.maketrans('', '', string.punctuation)
          lst = syn[0].definition().translate(translator).split()
          if not lst:
            # No meronyms found
            return 0

          retLst = [i for i in lst if set(syn)&set(wn.synsets(i)) and (syn != wn.synsets(i))] 
          if not retLst:
            # retLst is empty
            return 0
          return retLst[0]
    return lst[0]

def main():
  # If running directly, get input from user
  theme_word = input("Enter a theme word for your pun: ").strip()
  lotus = Lotus(theme_word)

if __name__ == '__main__':
  main()