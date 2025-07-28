# PagePilot PDF Outline Extractor

## Overview

PagePilot is a sophisticated PDF outline extraction solution that intelligently identifies document structure including titles and hierarchical headings (H1, H2, H3) with pinpoint accuracy. Unlike simple font-size-based approaches, our solution uses multiple heuristics to understand document semantics and extract meaningful outlines.

## Approach

### Multi-Heuristic Heading Detection

Our solution doesn't rely solely on font sizes for heading detection. Instead, it employs a comprehensive approach using:

1. **Font Analysis**: Relative font size comparison within the document context
2. **Typography Heuristics**: Bold text, font family, and styling analysis
3. **Positional Analysis**: Text positioning, indentation, and spacing patterns
4. **Pattern Recognition**: Common heading patterns (numbered sections, chapter markers)
5. **Semantic Analysis**: Keyword recognition and context understanding
6. **Structural Analysis**: Standalone line detection and paragraph separation

### Title Extraction Strategy

The title extraction uses a multi-strategy approach:

1. **First Page Analysis**: Identifies the largest, most prominent text on the first page
2. **Pattern Matching**: Recognizes common title patterns and keywords
3. **Position-Based Detection**: Considers text positioning and layout
4. **Fallback Mechanisms**: Ensures a title is always extracted even from complex documents

### Architecture

```
src/
├── pdf_extractor.py      # Core PDF text extraction with font metadata
├── heading_detector.py   # Intelligent heading detection algorithms
├── title_extractor.py    # Multi-strategy title extraction
├── output_formatter.py   # JSON output formatting
└── outline_extractor.py  # Main processing pipeline
```

## Models and Libraries Used

- **PyMuPDF (fitz) v1.23.14**: Primary PDF processing library for text extraction with font metadata
- **Python 3.11**: Runtime environment
- **No ML Models**: Uses rule-based algorithms to stay under the 200MB limit and work offline

## Key Features

- **Robust Heading Detection**: Works with various PDF formats and layouts
- **Intelligent Title Extraction**: Multiple fallback strategies ensure reliable title detection
- **Hierarchical Structure**: Properly identifies H1, H2, H3 levels
- **Page Number Tracking**: Accurate page number association for each heading
- **Error Handling**: Graceful handling of malformed or complex PDFs
- **Offline Operation**: No network dependencies, works completely offline

## Build and Run Instructions

### Building the Docker Image

```bash
docker build --platform linux/amd64 -t pagepilot:latest .
```

### Running the Solution

```bash
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none pagepilot:latest
```

### Expected Behavior

- The container automatically processes all PDF files from `/app/input`
- For each `filename.pdf`, generates a corresponding `filename.json` in `/app/output`
- Output follows the required JSON format:

```json
{
  "title": "Document Title",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "Background", "page": 2 },
    { "level": "H3", "text": "Related Work", "page": 3 }
  ]
}
```

## Testing

For local development and testing:

1. Create `input/` and `output/` directories
2. Place PDF files in the `input/` directory
3. Run: `python main.py`

## Technical Specifications

- **Architecture**: AMD64 (x86_64) compatible
- **Memory**: Optimized for efficient processing
- **Dependencies**: Minimal, focused on PDF processing
- **Network**: Completely offline, no external API calls
- **Error Handling**: Robust error recovery and reporting

## Algorithm Details

### Heading Confidence Scoring

Each potential heading receives a confidence score based on:
- Font size relative to document average (30% weight)
- Bold formatting (25% weight)
- Text patterns and numbering (30% weight)
- Position and spacing (15% weight)

### Hierarchy Determination

Heading levels are determined by:
1. Font size ratios (primary factor)
2. Document structure analysis
3. Logical hierarchy validation
4. Context-aware adjustments

This approach ensures accurate heading detection across diverse document types and layouts.
