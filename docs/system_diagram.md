# Pun Generator System Architecture

This diagram shows how the pun generation system works, including the main components and their interactions.

```mermaid
graph TD
    %% Main Input and Output
    Input[User Input Theme Word]
    Output[Generated Pun]

    %% Level 1: Core System
    subgraph Core["Core System"]
        direction TB
        Lotus[Lotus Class]
    end

    %% Level 2: Processing Systems
    subgraph Processing["Processing Systems"]
        direction TB
        subgraph Semantic["Semantic Processing"]
            direction TB
            WordNet[WordNet Path Similarity]
            InfoContent[Information Content]
            Relations[WordNet Relationships]
        end

        subgraph Grammar["Grammar Processing"]
            direction TB
            VerbForm[Verb Form Detection]
            POSTag[POS Tagging]
            Conjugation[Verb Conjugation]
        end
    end

    %% Level 3: Template System
    subgraph Template["Template System"]
        direction TB
        TemplateClass[GrammaticalTemplate Class]
        Patterns[Template Patterns]
    end

    %% Level 4: Features
    subgraph Features["System Features"]
        direction TB
        subgraph Theme["Theme Relevance"]
            direction TB
            Scoring[Relevance Scoring]
            Expansion[Word Expansion]
            Corpus[Corpus Analysis]
        end

        subgraph Correction["Grammar Correction"]
            direction TB
            Morphology[Morphological Analysis]
            PatternMatch[Pattern Matching]
            Rules[Conjugation Rules]
        end
    end

    %% Main Flow
    Input --> Lotus
    Lotus --> Semantic
    Lotus --> Grammar
    Semantic --> TemplateClass
    Grammar --> TemplateClass
    TemplateClass --> Patterns
    Patterns --> Output

    %% Feature Connections
    Semantic --> Theme
    Grammar --> Correction

    %% Styling
    classDef input fill:#f9f,stroke:#333,stroke-width:2px
    classDef output fill:#9f9,stroke:#333,stroke-width:2px
    classDef core fill:#bbf,stroke:#333,stroke-width:2px
    classDef semantic fill:#fbb,stroke:#333,stroke-width:2px
    classDef grammar fill:#bfb,stroke:#333,stroke-width:2px
    classDef template fill:#fbf,stroke:#333,stroke-width:2px
    classDef feature fill:#ddd,stroke:#333,stroke-width:2px

    class Input input
    class Output output
    class Lotus core
    class WordNet,InfoContent,Relations semantic
    class VerbForm,POSTag,Conjugation grammar
    class TemplateClass,Patterns template
    class Scoring,Expansion,Corpus,Morphology,PatternMatch,Rules feature
```

## System Architecture

### 1. Input Layer
- **User Input**: Theme word processing and validation
- **Input Normalization**: Standardization of input format

### 2. Core System
- **Lotus Class**: Main orchestrator for pun generation
  - Coordinates between processing systems
  - Manages theme word processing
  - Handles compound word generation

### 3. Processing Systems
#### Semantic Processing
- **WordNet Integration**: Path similarity calculations
- **Information Content**: Corpus-based frequency analysis
- **WordNet Relationships**: Hypernyms, hyponyms, and meronyms

#### Grammar Processing
- **Verb Form Detection**: Automatic verb identification
- **POS Tagging**: Part-of-speech analysis
- **Verb Conjugation**: Morphological rules application

### 4. Template System
- **GrammaticalTemplate Class**: Core template management
- **Template Patterns**: Pun structure and formatting
- **Grammar Integration**: Applies corrections to templates

### 5. System Features
#### Theme Relevance
- **Relevance Scoring**: Semantic similarity metrics
- **Word Expansion**: Related word discovery
- **Corpus Analysis**: Frequency and usage patterns

#### Grammar Correction
- **Morphological Analysis**: Word form processing
- **Pattern Matching**: Template-based corrections
- **Conjugation Rules**: Verb form generation

## Data Flow

1. **Input Processing**
   - User provides theme word
   - System validates and normalizes input

2. **Core Processing**
   - Lotus class coordinates generation
   - Semantic and grammar systems process input

3. **Template Processing**
   - Template system applies corrections
   - Patterns are selected and formatted

4. **Feature Application**
   - Theme relevance ensures context
   - Grammar correction ensures correctness

5. **Output Generation**
   - Final pun is formatted
   - Output is grammatically correct and theme-relevant

## Key Features

### Theme Relevance
- Multi-method semantic similarity
- WordNet relationship expansion
- Corpus-based frequency analysis

### Grammar Correction
- Automatic verb form detection
- Morphological analysis
- Pattern-based corrections

### Performance
- Caching system
- Early termination
- Batch processing 