# PagePilot - Adobe India Hackathon 2025

## 🏆 "Connecting the Dots" Challenge - Complete Solution

PagePilot is a comprehensive document intelligence solution that extracts structured outlines from PDFs and powers them with on-device intelligence for semantic understanding and content linking.

## 📁 Project Structure

```
PagePilot/
├── Round1A/          # PDF Outline Extraction (COMPLETED ✅)
├── Round1B/          # Persona-Aware Document Analyst (COMPLETED ✅)
├── Round2/           # Advanced Features & Integration (TODO)
└── README.md         # This file
```

## 🎯 Challenge Overview

### Round 1: Building the Brains
Extract structured outlines from raw PDFs with blazing speed and pinpoint accuracy, then power it up with on-device intelligence that understands sections and links related ideas together.

#### Round 1A: Understand Your Document ✅ COMPLETED
**Challenge Theme**: Connecting the Dots Through Docs

**Mission**: Extract structured outline (Title, H1, H2, H3) from PDF documents in clean, hierarchical JSON format.

**Status**: ✅ **COMPLETED** - Full working solution with Docker support

**Key Features**:
- Multi-heuristic heading detection (not just font-size based)
- Intelligent title extraction with fallback strategies
- AMD64 Docker compatibility
- Offline operation (no network dependencies)
- Robust error handling

**Output Format**:
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

#### Round 1B: Persona-Aware Document Analyst ✅ COMPLETED
**Challenge Theme**: Semantic Understanding & Content Linking

**Mission**: Build AI document analyst that accepts 3-10 PDFs, a persona, and job-to-be-done, then extracts and ranks relevant sections.

**Status**: ✅ **COMPLETED** - Full working solution with NLP intelligence

**Key Features**:
- Multi-heuristic section ranking with explainable AI
- Lightweight transformer models (≤1GB) with TF-IDF fallback
- Persona-aware relevance scoring
- CPU-only operation with offline capability
- ≤60 second processing time

#### Round 2: Advanced Features (TODO)
**Challenge Theme**: Integration & Advanced Capabilities

**Mission**: Advanced document processing and integration features.

**Status**: 🔄 **PENDING** - Awaiting requirements

## 🚀 Quick Start

### Round 1A - PDF Outline Extraction

```bash
cd Round1A

# Local execution
pip install PyMuPDF==1.23.14
python main.py

# Docker execution
docker build --platform linux/amd64 -t pagepilot-round1a:latest .
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none pagepilot-round1a:latest
```

## 📊 Current Status

- ✅ **Round 1A**: Complete PDF outline extraction solution
- ✅ **Round 1B**: Complete persona-aware document analyst
- 🔄 **Round 2**: Awaiting requirements and implementation

## 🛠️ Technology Stack

### Round 1A
- **Python 3.11**: Core runtime
- **PyMuPDF (fitz)**: PDF processing and text extraction
- **Docker**: Containerization for AMD64 architecture
- **Multi-heuristic algorithms**: Advanced heading detection

### Round 1B
- **sentence-transformers**: Lightweight NLP models (~80MB)
- **scikit-learn**: TF-IDF fallback and similarity computation
- **Multi-factor scoring**: NLP + domain + job + position + level
- **Explainable AI**: Human-readable ranking explanations

### Future Rounds
- TBD based on requirements

## 📈 Performance

### Round 1A Metrics
- ✅ Processes PDFs up to 50 pages
- ✅ Accurate heading detection across various layouts
- ✅ Fast processing with minimal memory footprint
- ✅ 100% offline operation
- ✅ Robust error handling

## 🎯 Next Steps

1. **Round 1B**: Implement on-device intelligence for semantic understanding
2. **Round 2**: Add advanced features and integration capabilities
3. **Integration**: Connect all rounds into a unified solution

## 📝 Notes

Each round is self-contained with its own:
- Source code and dependencies
- Documentation and README
- Docker configuration
- Test files and examples

This modular approach ensures clean separation of concerns and easy development/testing of individual components.

---

**Project**: PagePilot
**Challenge**: Adobe India Hackathon 2025 - "Connecting the Dots"
**Status**: Round 1A Complete, Round 1B & 2 Pending
**Last Updated**: July 28, 2025
