# 🚀 PagePilot Quick Start Guide

**Get up and running with PagePilot in 5 minutes!**

## 📋 Prerequisites

- Python 3.8 or higher
- pip package manager
- PDF documents to analyze

## ⚡ Quick Installation

### Option 1: Automated Installation (Recommended)

**Windows:**
```bash
# Run the installation script
install.bat
```

**Linux/Mac:**
```bash
# Make script executable and run
chmod +x install.sh
./install.sh
```

### Option 2: Manual Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir input output
```

## 🎯 Quick Usage

### Step 1: Add Your PDFs
Place your PDF files in the `input/` folder:
```
input/
├── document1.pdf
├── document2.pdf
└── document3.pdf
```

### Step 2: Configure Analysis
Copy and modify the sample configuration:
```bash
cp input/sample_analysis_request.json input/analysis_request.json
```

Edit `input/analysis_request.json`:
```json
{
    "documents": ["your_document.pdf"],
    "persona": {
        "role": "Your Role Here"
    },
    "job_to_be_done": {
        "task": "Your specific task here"
    }
}
```

### Step 3: Run Analysis
```bash
python main.py
```

### Step 4: View Results
Check `output/analysis_result.json` for your results!

## 🔧 Common Persona Examples

### HR Professional
```json
{
    "persona": {"role": "HR professional"},
    "job_to_be_done": {"task": "Create fillable forms for onboarding"}
}
```

### Training Manager
```json
{
    "persona": {"role": "Training Manager"},
    "job_to_be_done": {"task": "Develop training curriculum"}
}
```

### Legal Professional
```json
{
    "persona": {"role": "Legal Professional"},
    "job_to_be_done": {"task": "Review contracts for compliance"}
}
```

## 🐛 Troubleshooting

**Problem: "No module named 'fitz'"**
```bash
pip install PyMuPDF==1.24.0
```

**Problem: Empty results**
- Ensure PDFs contain readable text (not scanned images)
- Check that your persona and job are specific
- Verify PDF files are in the input folder

**Problem: Permission errors**
- Run as administrator (Windows) or use sudo (Linux/Mac)
- Check file permissions on input/output folders

## 📞 Need Help?

- Check the main README.md for detailed documentation
- Run `python main.py --help` for command options
- Use debug mode: `python main.py --verbose`

---

**Happy analyzing! 🎉**
