#!/usr/bin/env python3
"""
Complete thesis conversion script from LaTeX to Markdown using Pandoc
"""

import os
import subprocess
import sys
from pathlib import Path

def preprocess_latex(content):
    """Apply preprocessing fixes for better Pandoc Markdown conversion"""
    import re
    
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

def convert_with_pandoc(input_file, output_file, bib_file=None):
    """Convert LaTeX file to Markdown using Pandoc"""
    cmd = [
        'pandoc',
        '-f', 'latex',
        '-t', 'markdown',
        '--mathjax',
        '--wrap=none',
        '--markdown-headings=atx',
        '-o', output_file,
        input_file
    ]
    
    if bib_file and os.path.exists(bib_file):
        cmd.extend(['--citeproc', '--bibliography', bib_file])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✓ Converted {input_file} -> {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error converting {input_file}: {e.stderr}")
        return False

def main():
    # Setup paths
    base_dir = Path('.')
    output_dir = base_dir / 'markdown_output'
    output_dir.mkdir(exist_ok=True)
    
    # Bibliography file
    bib_file = base_dir / 'refs.bib'
    
    # Chapter files in order
    chapter_files = [
        '0_abstract.tex',
        '1_introduction.tex', 
        '2_theoretical_framework.tex',
        '3_methods.tex',
        '4_results.tex',
        '5_conclusion.tex',
        '8_appendix.tex',
        '9_miscellaneous.tex'
    ]
    
    converted_files = []
    
    print("Converting individual chapters...")
    for chapter_file in chapter_files:
        if not os.path.exists(chapter_file):
            print(f"⚠ Skipping {chapter_file} - file not found")
            continue
            
        # Read and preprocess
        with open(chapter_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        processed_content = preprocess_latex(content)
        
        # Write preprocessed file
        preprocessed_file = f"temp_{chapter_file}"
        with open(preprocessed_file, 'w', encoding='utf-8') as f:
            f.write(processed_content)
        
        # Convert with Pandoc
        output_file = output_dir / f"{chapter_file.replace('.tex', '.md')}"
        if convert_with_pandoc(preprocessed_file, str(output_file), str(bib_file)):
            converted_files.append(output_file)
        
        # Clean up temp file
        os.remove(preprocessed_file)
    
    # Create combined thesis
    if converted_files:
        print("\\nCreating combined thesis...")
        combined_path = output_dir / 'thesis_complete.md'
        
        with open(combined_path, 'w', encoding='utf-8') as combined_file:
            combined_file.write("# Weak Lensing Map Inference: A Physics-Informed Gaussian Processes Approach\\n\\n")
            
            for md_file in converted_files:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    combined_file.write(content)
                    combined_file.write("\\n\\n---\\n\\n")
        
        print(f"✓ Combined thesis created: {combined_path}")
    
    print("\\nConversion complete!")
    print(f"Individual chapters: {len(converted_files)} files in {output_dir}")
    if converted_files:
        print(f"Combined thesis: {output_dir / 'thesis_complete.md'}")

if __name__ == "__main__":
    main()