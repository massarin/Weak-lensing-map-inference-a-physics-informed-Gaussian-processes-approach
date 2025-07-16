#!/usr/bin/env python3
"""
Preprocessing script to fix LaTeX issues before Pandoc conversion to Markdown
"""

import re
import sys
import os

def preprocess_latex(content):
    """Apply preprocessing fixes for better Pandoc Markdown conversion"""
    
    # Fix the custom \code command - replace with \texttt
    content = content.replace(
        r'\newcommand*{\code}{\lstinline[keepspaces=true,breaklines]}',
        r'\newcommand*{\code}[1]{\texttt{#1}}'
    )
    
    # Fix math spacing issues
    content = content.replace(r'\sigma_\text{ noise}', r'\sigma_{\text{noise}}')
    
    # Remove problematic LaTeX environments that don't convert well
    # Remove titlingpage environment
    content = re.sub(r'\\begin\{titlingpage\}.*?\\end\{titlingpage\}', '', content, flags=re.DOTALL)
    
    # Convert adjustwidth to simple paragraph
    content = re.sub(r'\\begin\{adjustwidth\*?\}.*?\\end\{adjustwidth\*?\}', '', content, flags=re.DOTALL)
    
    # Convert wrapfigure to regular figure
    content = re.sub(
        r'\\begin\{wrapfigure\}(\[[^\]]*\])?\{[^}]*\}\{[^}]*\}',
        r'\\begin{figure}[h]',
        content
    )
    content = re.sub(r'\\end\{wrapfigure\}', r'\\end{figure}', content)
    
    # Convert wraptable to regular table
    content = re.sub(
        r'\\begin\{wraptable\}(\[[^\]]*\])?\{[^}]*\}\{[^}]*\}',
        r'\\begin{table}[h]',
        content
    )
    content = re.sub(r'\\end\{wraptable\}', r'\\end{table}', content)
    
    # Remove TikZ pictures that don't convert well - replace with placeholder
    content = re.sub(
        r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}',
        '[Interactive diagram - see LaTeX source]',
        content,
        flags=re.DOTALL
    )
    
    # Remove standalone TikZ figures
    content = re.sub(
        r'\\begin\{standalone\}.*?\\end\{standalone\}',
        '[Standalone figure - see LaTeX source]',
        content,
        flags=re.DOTALL
    )
    
    # Clean up multiple blank lines
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    return content

def process_file(input_file, output_file):
    """Process a single LaTeX file"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply preprocessing
    processed_content = preprocess_latex(content)
    
    # Write processed content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(processed_content)
    
    print(f"Preprocessed {input_file} -> {output_file}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python pandoc_preprocess.py <input.tex> <output.tex>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} does not exist")
        sys.exit(1)
    
    process_file(input_file, output_file)

if __name__ == "__main__":
    main()