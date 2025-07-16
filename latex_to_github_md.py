#!/usr/bin/env python3
"""
General LaTeX to GitHub Flavored Markdown converter
Handles common LaTeX constructs that Pandoc doesn't convert well for GitHub
"""

import re
import os
import subprocess
import sys
from pathlib import Path
import tempfile
import shutil

class LaTeXToGitHubMarkdown:
    def __init__(self, input_file, output_dir="github_md", bib_file=None):
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        self.bib_file = Path(bib_file) if bib_file else None
        self.output_dir.mkdir(exist_ok=True)
        
        # Counters for unique labels
        self.equation_counter = 1
        self.figure_counter = 1
        self.table_counter = 1
        
    def extract_title_metadata(self, content):
        """Extract title, author, and other metadata from LaTeX"""
        metadata = {}
        
        # Extract title
        title_match = re.search(r'\\title\{([^}]+)\}', content)
        if title_match:
            metadata['title'] = title_match.group(1)
        
        # Extract author
        author_match = re.search(r'\\author\{([^}]+)\}', content)
        if author_match:
            metadata['author'] = author_match.group(1)
            
        # Extract date
        date_match = re.search(r'\\date\{([^}]+)\}', content)
        if date_match:
            metadata['date'] = date_match.group(1)
            
        # Extract thesis type
        thesis_match = re.search(r'\\thesistype\{([^}]+)\}', content)
        if thesis_match:
            metadata['thesis_type'] = thesis_match.group(1)
            
        return metadata
    
    def preprocess_latex(self, content):
        """Preprocess LaTeX content for better Pandoc conversion"""
        
        # Remove problematic environments and commands
        content = self._remove_title_pages(content)
        content = self._fix_figures(content)
        content = self._fix_math_environments(content)
        content = self._fix_custom_commands(content)
        content = self._fix_cross_references(content)
        content = self._remove_tikz_diagrams(content)
        content = self._clean_formatting(content)
        
        return content
    
    def _remove_title_pages(self, content):
        """Remove title page environments that don't convert well"""
        # Remove titlingpage environment
        content = re.sub(r'\\begin\{titlingpage\}.*?\\end\{titlingpage\}', '', content, flags=re.DOTALL)
        
        # Remove frontmatter/mainmatter commands
        content = re.sub(r'\\frontmatter|\\mainmatter|\\backmatter', '', content)
        
        # Remove abstract input if it's empty or problematic
        content = re.sub(r'\\input\{0_abstract\}', '', content)
        
        return content
    
    def _fix_figures(self, content):
        """Convert LaTeX figures to markdown-compatible format"""
        
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
        
        # Fix includegraphics to use relative paths
        def fix_includegraphics(match):
            filename = match.group(1)
            # Convert PDF to more web-friendly reference
            if filename.endswith('.pdf'):
                # Keep the PDF reference for now, but note it for conversion
                return f'![Figure](images/{filename})'
            return f'![Figure]({filename})'
        
        content = re.sub(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', fix_includegraphics, content)
        
        return content
    
    def _fix_math_environments(self, content):
        """Fix math environments and equations"""
        
        # Remove equation labels to avoid duplicates
        content = re.sub(r'\\label\{eq:[^}]+\}', '', content)
        
        # Convert align* and aligned environments to align for better compatibility
        content = re.sub(r'\\begin\{align\*\}', r'\\begin{aligned}', content)
        content = re.sub(r'\\end\{align\*\}', r'\\end{aligned}', content)
        
        # Ensure math environments are properly spaced
        content = re.sub(r'(\$\$[^$]+\$\$)', r'\n\1\n', content)
        
        return content
    
    def _fix_custom_commands(self, content):
        """Handle custom LaTeX commands"""
        
        # Common custom commands that might cause issues
        custom_commands = {
            r'\\code\{([^}]+)\}': r'`\1`',
            r'\\texttt\{([^}]+)\}': r'`\1`',
            r'\\emph\{([^}]+)\}': r'*\1*',
            r'\\textbf\{([^}]+)\}': r'**\1**',
            r'\\textit\{([^}]+)\}': r'*\1*',
        }
        
        for pattern, replacement in custom_commands.items():
            content = re.sub(pattern, replacement, content)
        
        return content
    
    def _fix_cross_references(self, content):
        """Simplify cross-references for better conversion"""
        
        # Simplify section references
        content = re.sub(r'\\textit\{Sec\.\s*\}\\ref\{([^}]+)\}', r'Section \\ref{\1}', content)
        content = re.sub(r'\\textit\{Fig\.\s*\}\\ref\{([^}]+)\}', r'Figure \\ref{\1}', content)
        content = re.sub(r'\\textit\{Tab\.\s*\}\\ref\{([^}]+)\}', r'Table \\ref{\1}', content)
        content = re.sub(r'\\textit\{Eq\.\s*\}\\ref\{([^}]+)\}', r'Equation \\ref{\1}', content)
        
        return content
    
    def _remove_tikz_diagrams(self, content):
        """Replace TikZ diagrams with placeholders"""
        
        def replace_tikz(match):
            # Try to extract caption or label for better placeholder
            tikz_content = match.group(0)
            caption_match = re.search(r'\\caption\{([^}]+)\}', tikz_content)
            label_match = re.search(r'\\label\{([^}]+)\}', tikz_content)
            
            placeholder = "[Diagram"
            if caption_match:
                placeholder += f": {caption_match.group(1)}"
            if label_match:
                placeholder += f" ({label_match.group(1)})"
            placeholder += "]"
            
            return placeholder
        
        # Remove TikZ pictures
        content = re.sub(
            r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}',
            replace_tikz,
            content,
            flags=re.DOTALL
        )
        
        # Remove standalone figures
        content = re.sub(
            r'\\begin\{standalone\}.*?\\end\{standalone\}',
            '[Standalone figure - see LaTeX source]',
            content,
            flags=re.DOTALL
        )
        
        return content
    
    def _clean_formatting(self, content):
        """Clean up formatting issues"""
        
        # Remove adjustwidth environments
        content = re.sub(r'\\begin\{adjustwidth\*?\}.*?\\end\{adjustwidth\*?\}', '', content, flags=re.DOTALL)
        
        # Clean up multiple blank lines
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        
        # Remove comments
        content = re.sub(r'(?<!\\)%.*$', '', content, flags=re.MULTILINE)
        
        return content
    
    def convert_with_pandoc(self, preprocessed_file, output_file):
        """Convert preprocessed LaTeX to GitHub Flavored Markdown"""
        
        cmd = [
            'pandoc',
            '-f', 'latex',
            '-t', 'gfm',
            '--wrap=none',
            '--standalone',
            '-o', str(output_file),
            str(preprocessed_file)
        ]
        
        # Add bibliography if available
        if self.bib_file and self.bib_file.exists():
            cmd.extend(['--citeproc', '--bibliography', str(self.bib_file)])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Pandoc conversion failed: {e.stderr}")
            return False
    
    def postprocess_markdown(self, content):
        """Post-process markdown for GitHub compatibility"""
        
        # Fix embed tags to use markdown image syntax
        content = re.sub(r'<embed src="([^"]+)"[^>]*/?>', r'![Figure](\1)', content)
        
        # Convert HTML figures to markdown
        content = re.sub(
            r'<figure[^>]*>\s*<embed src="([^"]+)"[^>]*/?>\s*<figcaption>(.*?)</figcaption>\s*</figure>',
            r'![Figure](\1)\n\n*\2*',
            content,
            flags=re.DOTALL
        )
        
        # Fix math blocks - ensure they use $$ delimiters
        content = re.sub(r'``` math\n(.*?)\n```', r'$$\1$$', content, flags=re.DOTALL)
        
        # Clean up reference links
        content = re.sub(
            r'<a href="[^"]*" data-reference-type="[^"]*" data-reference="[^"]*">\[([^\]]+)\]</a>',
            r'(\1)',
            content
        )
        
        # Remove div classes that don't work on GitHub
        content = re.sub(r'<div class="[^"]*">\s*</div>', '', content)
        content = re.sub(r'<div class="[^"]*">\s*([^<]*)\s*</div>', r'\1', content)
        
        # Convert PDF image references to PNG for GitHub compatibility
        content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\.pdf\)', r'![\1](\2.png)', content)
        
        return content
    
    def add_metadata_header(self, content, metadata):
        """Add title and metadata to the beginning of the document"""
        
        header_lines = []
        
        if 'title' in metadata:
            header_lines.append(f"# {metadata['title']}")
            header_lines.append("")
        
        if 'thesis_type' in metadata:
            header_lines.append(f"*{metadata['thesis_type']}*")
        
        if 'author' in metadata:
            header_lines.append(f"*{metadata['author']}*")
        
        if 'date' in metadata:
            header_lines.append(f"*{metadata['date']}*")
        
        if header_lines:
            header_lines.extend(["", "---", ""])
        
        return '\n'.join(header_lines) + '\n' + content
    
    def create_figure_conversion_script(self):
        """Create a script to convert PDF figures to web-compatible formats"""
        
        script_content = '''#!/bin/bash
# Convert PDF figures to PNG for web compatibility
# Run this script after LaTeX conversion

if command -v gs &> /dev/null; then
    echo "Converting PDF figures to PNG using Ghostscript..."
    for pdf_file in images/*.pdf; do
        if [ -f "$pdf_file" ]; then
            base_name=$(basename "$pdf_file" .pdf)
            echo "Converting $pdf_file to $base_name.png"
            gs -dNOPAUSE -dBATCH -sDEVICE=png16m -r300 -sOutputFile="images/$base_name.png" "$pdf_file"
        fi
    done
    echo "Figure conversion complete!"
else
    echo "Ghostscript (gs) not found. Install Ghostscript to convert PDF figures."
    echo "On Ubuntu/Debian: sudo apt-get install ghostscript"
    echo "On macOS: brew install ghostscript"
fi
'''
        
        script_path = self.output_dir / 'convert_figures.sh'
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Make script executable
        os.chmod(script_path, 0o755)
        
        return script_path
    
    def convert(self):
        """Main conversion function"""
        
        print(f"Converting {self.input_file} to GitHub Flavored Markdown...")
        
        # Read input file
        with open(self.input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract metadata
        metadata = self.extract_title_metadata(content)
        
        # Preprocess LaTeX
        preprocessed_content = self.preprocess_latex(content)
        
        # Write preprocessed file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as temp_file:
            temp_file.write(preprocessed_content)
            temp_file_path = temp_file.name
        
        try:
            # Convert with Pandoc
            output_file = self.output_dir / f"{self.input_file.stem}.md"
            if self.convert_with_pandoc(temp_file_path, output_file):
                
                # Read converted markdown
                with open(output_file, 'r', encoding='utf-8') as f:
                    markdown_content = f.read()
                
                # Post-process markdown
                markdown_content = self.postprocess_markdown(markdown_content)
                
                # Add metadata header
                markdown_content = self.add_metadata_header(markdown_content, metadata)
                
                # Write final markdown
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                
                print(f"✓ Conversion successful: {output_file}")
                
                # Create figure conversion script
                script_path = self.create_figure_conversion_script()
                print(f"✓ Figure conversion script created: {script_path}")
                
                return True
            else:
                print("✗ Pandoc conversion failed")
                return False
                
        finally:
            # Clean up temp file
            os.unlink(temp_file_path)

def main():
    if len(sys.argv) < 2:
        print("Usage: python latex_to_github_md.py <input.tex> [output_dir] [bibliography.bib]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "github_md"
    bib_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Auto-detect bib file if not provided
    if not bib_file:
        input_path = Path(input_file)
        potential_bib = input_path.parent / "refs.bib"
        if potential_bib.exists():
            bib_file = str(potential_bib)
    
    converter = LaTeXToGitHubMarkdown(input_file, output_dir, bib_file)
    
    if converter.convert():
        print("\nConversion complete!")
        print(f"Output directory: {output_dir}")
        print("\nNext steps:")
        print("1. Run ./convert_figures.sh to convert PDF figures to PNG")
        print("2. Review the markdown file and fix any remaining issues")
        print("3. Copy images directory to your GitHub repository")
    else:
        print("Conversion failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()