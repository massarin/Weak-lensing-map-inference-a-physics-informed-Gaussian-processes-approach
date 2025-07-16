#!/bin/bash
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
