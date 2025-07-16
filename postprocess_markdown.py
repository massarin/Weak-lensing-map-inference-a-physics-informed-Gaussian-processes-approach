#!/usr/bin/env python3
"""
Post-processing script to clean up Markdown output from Pandoc conversion
"""

import re
import sys
import os

def clean_cross_references(content):
    """Clean up LaTeX cross-references to standard Markdown links"""
    # Fix section references like [sec:weak lensing](#sec:weak lensing){reference-type="ref" reference="sec:weak lensing"}
    content = re.sub(
        r'\[([^\]]+)\]\(#([^)]+)\)\{reference-type="ref" reference="[^"]+"\}',
        r'[\1](#\2)',
        content
    )
    
    # Fix equation references like [\[eq:fullsky\]](#eq:fullsky){reference-type="eqref" reference="eq:fullsky"}
    content = re.sub(
        r'\[\\\[([^\]]+)\\\]\]\(#([^)]+)\)\{reference-type="eqref" reference="[^"]+"\}',
        r'Eq. [\1](#\2)',
        content
    )
    
    return content

def clean_figures(content):
    """Clean up figure formatting"""
    # Remove empty figure captions and improve figure structure
    content = re.sub(r'<figure id="([^"]+)">\s*</figure>', '', content)
    
    # Fix figure captions to be more readable
    content = re.sub(
        r'<figure id="([^"]+)">\s*<figcaption>([^<]+)</figcaption>\s*</figure>',
        r'**Figure \1:** \2\n',
        content
    )
    
    return content

def clean_citations(content):
    """Clean up citation formatting"""
    # The citations are already well-formatted by Pandoc with --citeproc
    # Just clean up any remaining spacing issues
    content = re.sub(r'\s+\n', '\n', content)
    return content

def fix_math_formatting(content):
    """Fix any remaining math formatting issues"""
    # Ensure proper spacing around math
    content = re.sub(r'([a-zA-Z])\$([^$]+)\$([a-zA-Z])', r'\1 $\2$ \3', content)
    return content

def clean_line_breaks(content):
    """Clean up line breaks and formatting"""
    # Fix escaped newlines that shouldn't be there
    content = content.replace('\\n\\n', '\n\n')
    content = content.replace('\\n', '\n')
    
    # Remove excessive blank lines
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    return content

def postprocess_markdown(content):
    """Apply all post-processing steps"""
    content = clean_cross_references(content)
    content = clean_figures(content)
    content = clean_citations(content)
    content = fix_math_formatting(content)
    content = clean_line_breaks(content)
    
    return content

def process_file(input_file, output_file):
    """Process a single Markdown file"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    processed_content = postprocess_markdown(content)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(processed_content)
    
    print(f"Post-processed {input_file} -> {output_file}")

def main():
    markdown_dir = "markdown_output"
    
    if not os.path.exists(markdown_dir):
        print(f"Error: Directory {markdown_dir} does not exist")
        sys.exit(1)
    
    # Process all markdown files
    for filename in os.listdir(markdown_dir):
        if filename.endswith('.md'):
            input_path = os.path.join(markdown_dir, filename)
            output_path = os.path.join(markdown_dir, f"clean_{filename}")
            process_file(input_path, output_path)
    
    print("Post-processing complete!")

if __name__ == "__main__":
    main()