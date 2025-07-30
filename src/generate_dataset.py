#!/usr/bin/env python3
"""
Dataset Generator for Pun Generator
Generates a dataset of 100 theme words with their corresponding puns.
"""

import sys
import io
import csv
import json
from contextlib import redirect_stdout
from schemata import Lotus
import templates as tmp

class PunDatasetGenerator:
    def __init__(self):
        self.dataset = []
        self.successful_puns = 0
        self.failed_themes = []
        
    def capture_pun_output(self, theme_word):
        """Capture the pun output for a given theme word."""
        # Redirect stdout to capture the print output
        captured_output = io.StringIO()
        
        try:
            with redirect_stdout(captured_output):
                # Create Lotus instance with theme word
                lotus = Lotus(theme_word)
                
            # Get the captured output
            output = captured_output.getvalue().strip()
            
            if output and "What do you call" in output:
                # Parse the output to extract question and answer
                lines = [line.strip() for line in output.split('\n') if line.strip()]
                
                question = None
                answer = None
                
                for i, line in enumerate(lines):
                    # Find the question line
                    if "What do you call" in line and line.endswith("?"):
                        question = line
                        
                        # Look for the answer after the countdown
                        # The answer typically starts with "A " and ends with "!"
                        for j in range(i + 1, len(lines)):
                            if lines[j].startswith("A ") and lines[j].endswith("!"):
                                answer = lines[j][2:-1]  # Remove "A " and "!"
                                break
                        break
                
                if question and answer:
                    return question, answer
                        
            return None, None
            
        except Exception as e:
            print(f"Error generating pun for '{theme_word}': {str(e)}")
            return None, None
    
    def generate_dataset(self, theme_words):
        """Generate dataset for the given theme words."""
        print(f"Generating puns for {len(theme_words)} theme words...")
        print("=" * 60)
        
        for i, theme_word in enumerate(theme_words, 1):
            print(f"\n[{i}/{len(theme_words)}] Processing theme: '{theme_word}'")
            
            question, answer = self.capture_pun_output(theme_word)
            
            if question and answer:
                self.dataset.append({
                    'theme_word': theme_word,
                    'question': question,
                    'answer': answer
                })
                self.successful_puns += 1
                print(f"✓ Success: {question} → {answer}")
            else:
                self.failed_themes.append(theme_word)
                print(f"✗ Failed to generate pun for '{theme_word}'")
        
        print(f"\n" + "=" * 60)
        print(f"Dataset generation complete!")
        print(f"Successful puns: {self.successful_puns}")
        print(f"Failed themes: {len(self.failed_themes)}")
        
        if self.failed_themes:
            print(f"Failed themes: {', '.join(self.failed_themes)}")
    
    def save_dataset(self, filename_base="pun_dataset"):
        """Save the dataset in multiple formats."""
        if not self.dataset:
            print("No data to save!")
            return
        
        # Save as CSV
        csv_filename = f"{filename_base}.csv"
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['theme_word', 'question', 'answer']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.dataset)
        
        # Save as JSON
        json_filename = f"{filename_base}.json"
        with open(json_filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(self.dataset, jsonfile, indent=2, ensure_ascii=False)
        
        # Save as text file for easy reading
        txt_filename = f"{filename_base}.txt"
        with open(txt_filename, 'w', encoding='utf-8') as txtfile:
            txtfile.write("PUN GENERATOR DATASET\n")
            txtfile.write("=" * 50 + "\n\n")
            
            for i, entry in enumerate(self.dataset, 1):
                txtfile.write(f"{i}. Theme: {entry['theme_word']}\n")
                txtfile.write(f"   Q: {entry['question']}\n")
                txtfile.write(f"   A: {entry['answer']}\n\n")
        
        print(f"\nDataset saved in multiple formats:")
        print(f"  - CSV: {csv_filename}")
        print(f"  - JSON: {json_filename}")
        print(f"  - Text: {txt_filename}")

def get_expanded_theme_words():
    """Return a list of diverse theme words for pun generation."""
    return [
        # Food & Cooking (expanded)
        "food", "pizza", "bread", "cheese", "meat", "fish", "fruit", "vegetable", "cake", "soup",
        "cookie", "sandwich", "pasta", "rice", "egg", "milk", "butter", "sugar", "salt", "pepper",
        "coffee", "tea", "wine", "beer", "juice", "water", "ice", "cream", "chocolate", "candy",
        
        # Animals (expanded)
        "cat", "dog", "bird", "fish", "horse", "cow", "pig", "chicken", "duck", "rabbit",
        "mouse", "rat", "bear", "lion", "tiger", "elephant", "monkey", "snake", "frog", "bee",
        "ant", "spider", "butterfly", "eagle", "owl", "wolf", "fox", "deer", "sheep", "goat",
        
        # Nature (expanded)
        "tree", "flower", "grass", "mountain", "river", "ocean", "sun", "moon", "star", "cloud",
        "rock", "stone", "sand", "dirt", "leaf", "branch", "root", "seed", "plant", "forest",
        "lake", "pond", "stream", "hill", "valley", "field", "beach", "island", "desert", "cave",
        
        # Technology (expanded)
        "computer", "phone", "internet", "robot", "machine", "software", "hardware", "data", "code", "app",
        "screen", "keyboard", "mouse", "printer", "camera", "video", "audio", "file", "program", "system",
        "network", "server", "database", "website", "email", "message", "signal", "wire", "cable", "chip",
        
        # Transportation (expanded)
        "car", "bus", "train", "plane", "bike", "boat", "ship", "truck", "motorcycle", "subway",
        "taxi", "van", "wagon", "cart", "wheel", "tire", "engine", "fuel", "road", "bridge",
        "tunnel", "station", "airport", "port", "garage", "parking", "traffic", "speed", "brake", "horn",
        
        # Sports & Recreation (expanded)
        "football", "basketball", "tennis", "golf", "swimming", "running", "dancing", "music", "game", "toy",
        "ball", "bat", "racket", "club", "net", "goal", "score", "team", "player", "coach",
        "field", "court", "pool", "track", "gym", "exercise", "fitness", "sport", "race", "match",
        
        # Home & Living (expanded)
        "house", "room", "kitchen", "bedroom", "bathroom", "garden", "furniture", "door", "window", "roof",
        "wall", "floor", "ceiling", "stairs", "basement", "attic", "garage", "yard", "fence", "gate",
        "chair", "table", "bed", "sofa", "lamp", "mirror", "picture", "clock", "carpet", "curtain",
        
        # Work & Education (expanded)
        "school", "teacher", "student", "book", "pen", "paper", "desk", "office", "job", "work",
        "class", "lesson", "test", "exam", "grade", "homework", "project", "research", "study", "learn",
        "boss", "employee", "meeting", "report", "presentation", "interview", "salary", "career", "skill", "training",
        
        # Health & Body (expanded)
        "doctor", "medicine", "hospital", "health", "exercise", "sleep", "heart", "brain", "hand", "foot",
        "eye", "ear", "nose", "mouth", "tooth", "hair", "skin", "bone", "muscle", "blood",
        "nurse", "patient", "treatment", "cure", "pain", "injury", "disease", "fever", "cold", "flu",
        
        # Weather & Seasons (expanded)
        "rain", "snow", "wind", "storm", "summer", "winter", "spring", "autumn", "hot", "cold",
        "warm", "cool", "dry", "wet", "sunny", "cloudy", "foggy", "thunder", "lightning", "tornado",
        "hurricane", "flood", "drought", "ice", "frost", "hail", "mist", "breeze", "gale", "blizzard",
        
        # Colors & Art (expanded)
        "red", "blue", "green", "yellow", "black", "white", "painting", "drawing", "art", "color",
        "orange", "purple", "pink", "brown", "gray", "silver", "gold", "bronze", "bright", "dark",
        "brush", "paint", "canvas", "sketch", "portrait", "landscape", "sculpture", "gallery", "museum", "artist",
        
        # Time & Events (expanded)
        "time", "clock", "watch", "calendar", "birthday", "holiday", "party", "wedding", "meeting", "event",
        "day", "night", "morning", "evening", "hour", "minute", "second", "week", "month", "year",
        "celebration", "festival", "ceremony", "concert", "show", "performance", "dance", "theater", "movie", "film",
        
        # Tools & Objects (new category)
        "hammer", "nail", "screw", "drill", "saw", "knife", "fork", "spoon", "plate", "cup",
        "glass", "bottle", "jar", "box", "bag", "basket", "bucket", "rope", "chain", "lock",
        "key", "button", "zipper", "thread", "needle", "scissors", "ruler", "pencil", "eraser", "glue",
        
        # Clothing & Fashion (new category)
        "shirt", "pants", "dress", "skirt", "jacket", "coat", "hat", "cap", "shoe", "sock",
        "glove", "scarf", "belt", "tie", "suit", "jeans", "sweater", "hoodie", "shorts", "underwear",
        "jewelry", "ring", "necklace", "bracelet", "earring", "watch", "glasses", "sunglasses", "purse", "wallet",
        
        # Science & Math (new category)
        "science", "math", "physics", "chemistry", "biology", "atom", "molecule", "cell", "gene", "DNA",
        "number", "equation", "formula", "theory", "experiment", "lab", "test", "result", "proof", "logic",
        "energy", "force", "gravity", "light", "sound", "heat", "electricity", "magnet", "chemical", "element",
        
        # Business & Money (new category)
        "money", "dollar", "cent", "coin", "bill", "bank", "loan", "debt", "credit", "cash",
        "business", "company", "store", "shop", "market", "sale", "buy", "sell", "price", "cost",
        "profit", "loss", "investment", "stock", "bond", "insurance", "tax", "budget", "account", "finance"
    ]

def main():
    """Main function to generate the expanded pun dataset."""
    print("PUN GENERATOR EXPANDED DATASET CREATION")
    print("=" * 50)
    
    # Get expanded theme words
    theme_words = get_expanded_theme_words()
    print(f"Total theme words: {len(theme_words)}")
    
    # Create dataset generator
    generator = PunDatasetGenerator()
    
    # Generate the dataset
    generator.generate_dataset(theme_words)
    
    # Save the dataset
    generator.save_dataset("pun_dataset_expanded")
    
    print(f"\nExpanded dataset generation completed!")
    print(f"Total successful puns: {generator.successful_puns}/{len(theme_words)}")
    print(f"Success rate: {(generator.successful_puns/len(theme_words)*100):.1f}%")

if __name__ == "__main__":
    main() 