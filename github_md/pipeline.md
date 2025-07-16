# LaTeX to GitHub Markdown Conversion Guide

This repository contains a comprehensive LaTeX to GitHub Flavored Markdown converter that handles complex academic documents with figures, math, citations, and custom LaTeX commands.

## Overview

The conversion process transforms LaTeX documents into GitHub-compatible markdown while preserving:
- Document structure and formatting
- Mathematical equations and symbols
- Figure references with web-compatible images
- Citations and bibliography
- Cross-references and labels

## Prerequisites

### Required Software
- **Python 3.7+**
- **Pandoc** (universal document converter)
- **Ghostscript** (for PDF to PNG conversion)

### Installation

```bash
# Install Pandoc
# On macOS:
brew install pandoc

# On Ubuntu/Debian:
sudo apt-get install pandoc

# Install Ghostscript
# On macOS:
brew install ghostscript

# On Ubuntu/Debian:
sudo apt-get install ghostscript
```

## Step-by-Step Conversion Process

### Step 1: Analyze LaTeX Document Structure

First, examine your LaTeX document to understand its structure:

```bash
# Check main LaTeX file
ls -la *.tex

# Identify dependencies
grep -n "\\input\|\\include" thesis.tex

# Check for bibliography
ls -la *.bib
```

### Step 2: Run the Conversion Script

Execute the main conversion script:

```bash
# Basic conversion
python latex_to_github_md.py thesis.tex

# With custom output directory
python latex_to_github_md.py thesis.tex my_output_dir

# With bibliography
python latex_to_github_md.py thesis.tex github_md refs.bib
```

### Step 3: Figure Conversion

Convert PDF figures to PNG for web compatibility:

```bash
# Navigate to output directory
cd github_md

# Run figure conversion script
./convert_figures.sh
```

### Step 4: Clean Up HTML Elements

Remove HTML elements that don't render properly on GitHub:

```bash
# Remove figure tags
sed -i '' 's/<figure[^>]*>//' thesis.md
sed -i '' 's/<\/figure>//' thesis.md

# Remove paragraph tags
sed -i '' 's/<p>//g; s/<\/p>//g' thesis.md
```

### Step 5: Verify and Fix Image References

Check that all images are properly referenced:

```bash
# Check image references
grep -n "!\[.*\](" thesis.md

# Verify image files exist
ls -la images/*.png
```

## Detailed Conversion Pipeline

### 1. LaTeX Preprocessing

The converter performs several preprocessing steps:

```python
def preprocess_latex(self, content):
    # Extract metadata (title, author, date)
    metadata = self.extract_title_metadata(content)
    
    # Remove problematic LaTeX environments
    content = self._remove_title_pages(content)
    
    # Fix figure environments
    content = self._fix_figures(content)
    
    # Handle math environments
    content = self._fix_math_environments(content)
    
    # Convert custom commands
    content = self._fix_custom_commands(content)
    
    # Process cross-references
    content = self._fix_cross_references(content)
    
    # Handle TikZ diagrams
    content = self._remove_tikz_diagrams(content)
    
    # Clean formatting
    content = self._clean_formatting(content)
    
    return content
```

### 2. Pandoc Conversion

Convert preprocessed LaTeX to GitHub Flavored Markdown:

```bash
pandoc -f latex -t gfm --wrap=none --standalone --citeproc --bibliography=refs.bib -o thesis.md thesis_preprocessed.tex
```

### 3. Postprocessing

Fix GitHub-specific formatting issues:

```python
def postprocess_markdown(self, content):
    # Fix HTML embed tags
    content = re.sub(r'<embed src="([^"]+)"[^>]*/?>', r'![Figure](\1)', content)
    
    # Convert math blocks
    content = re.sub(r'``` math\n(.*?)\n```', r'$$\1$$', content, flags=re.DOTALL)
    
    # Fix reference links
    content = re.sub(r'<a href="[^"]*"[^>]*>\[([^\]]+)\]</a>', r'(\1)', content)
    
    # Convert PDF to PNG references
    content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\.pdf\)', r'![\1](\2.png)', content)
    
    return content
```

### 4. Figure Processing

Convert PDF figures to PNG with high quality:

```bash
# Using Ghostscript (300 DPI)
gs -dNOPAUSE -dBATCH -sDEVICE=png16m -r300 -sOutputFile="figure.png" "figure.pdf"
```

## Common Issues and Solutions

### Issue 1: Math Rendering

**Problem**: Math equations not displaying properly
**Solution**: Ensure proper GitHub math syntax:
```markdown
# Inline math
$\kappa(\theta)$

# Display math
$$\kappa(\theta) = \int_0^{\chi*}d\chi W(\chi)\delta_m(\chi \theta, \chi)$$
```

### Issue 2: Figure Display

**Problem**: Images not showing on GitHub
**Solution**: 
1. Convert PDF to PNG: `gs -dNOPAUSE -dBATCH -sDEVICE=png16m -r300 -sOutputFile="image.png" "image.pdf"`
2. Use relative paths: `![Figure](images/figure.png)`
3. Remove HTML figure tags

### Issue 3: Custom Commands

**Problem**: LaTeX commands not recognized
**Solution**: Add preprocessing rules:
```python
custom_commands = {
    r'\\code\{([^}]+)\}': r'`\1`',
    r'\\texttt\{([^}]+)\}': r'`\1`',
    r'\\textbf\{([^}]+)\}': r'**\1**',
    r'\\textit\{([^}]+)\}': r'*\1*',
}
```

### Issue 4: Cross-References

**Problem**: LaTeX references not working
**Solution**: Convert to simple text:
```python
content = re.sub(r'\\textit\{Fig\.\s*\}\\ref\{([^}]+)\}', r'Figure \1', content)
```

## Repository Structure

```
├── latex_to_github_md.py    # Main conversion script
├── thesis.tex               # Original LaTeX file
├── refs.bib                 # Bibliography file
├── images/                  # Original PDF figures
├── github_md/               # Output directory
│   ├── thesis.md           # Converted markdown
│   ├── images/             # PNG figures
│   └── convert_figures.sh  # Figure conversion script
└── README.md               # This guide
```

## Script Features

### Handles Complex LaTeX
- Multi-file documents (`\input`, `\include`)
- Custom document classes (memoir, article, etc.)
- TikZ diagrams and complex figures
- Bibliography and citations
- Custom commands and environments

### GitHub Optimization
- Proper math rendering with `$` delimiters
- PNG images for web compatibility
- Clean markdown structure
- Preserved document hierarchy

### Automated Processing
- One-command conversion
- Batch figure processing
- Error handling and logging
- Customizable output directories

## Testing the Conversion

After conversion, verify the output:

```bash
# Check markdown syntax
grep -n "^#" thesis.md  # Headers
grep -n "!\[" thesis.md  # Images
grep -n "\$\$" thesis.md  # Math blocks

# Validate image links
find images/ -name "*.png" | wc -l
grep -o "images/[^)]*\.png" thesis.md | wc -l
```

## Advanced Usage

### Custom Processing

Extend the converter for specific needs:

```python
# Add custom preprocessing
def custom_preprocess(content):
    # Handle specific LaTeX commands
    content = re.sub(r'\\mycommand\{([^}]+)\}', r'**\1**', content)
    return content

# Add to pipeline
converter.preprocess_latex = custom_preprocess
```

### Batch Processing

Process multiple documents:

```bash
# Process all .tex files
for tex_file in *.tex; do
    python latex_to_github_md.py "$tex_file" "output_${tex_file%.*}"
done
```

## Troubleshooting

### Common Errors

1. **Pandoc not found**: Install Pandoc
2. **Ghostscript not found**: Install Ghostscript
3. **Math rendering issues**: Check `$` delimiter syntax
4. **Images not displaying**: Verify PNG conversion and paths
5. **Bibliography not working**: Check `.bib` file path

### Debug Mode

Enable verbose output:

```python
# In latex_to_github_md.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

To improve the converter:

1. Fork the repository
2. Add preprocessing rules for new LaTeX commands
3. Improve figure handling
4. Add support for new document classes
5. Submit pull requests

## License

This conversion tool is provided for academic and research purposes. Please respect appropriate citation practices when using this work.