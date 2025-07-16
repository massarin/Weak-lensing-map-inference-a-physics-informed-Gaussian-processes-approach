Pandoc is a **powerful, flexible tool** for converting LaTeX to Markdown, but it is **not lossless**—especially with advanced LaTeX features. If your main goal is to **preserve content and math** (as you indicated), Pandoc is an excellent choice. Here’s an **advanced guide** to getting the best results, including tips, limitations, and customization options.

## Core Conversion Command

To convert a LaTeX (`.tex`) file to Pandoc’s enhanced Markdown:

```sh
pandoc -f latex -t markdown --mathjax -o output.md input.tex
```
- **`-f latex`**: Specifies LaTeX input.
- **`-t markdown`**: Outputs Markdown.
- **`--mathjax`**: Preserves LaTeX math as `$...$` or `$$...$$` (for MathJax rendering).
- **`-o output.md`**: Sets the output filename.

Pandoc will **drop most LaTeX-specific formatting** (custom commands, environments, etc.) but **preserve text, headings, lists, tables, and math**[3][6].

## What Pandoc Preserves and Drops

### ✅ Preserved

- **Text content**: Paragraphs, sections, lists, blockquotes.
- **Math**: Inline (`$...$`) and display (`$$...$$`) equations.
- **Basic tables**: Simple LaTeX tables become Markdown tables.
- **Footnotes**: Converted to Markdown footnote syntax.
- **Code blocks**: Fenced code blocks are supported.
- **Citations**: Basic citation support (see below for advanced cases).

### ❌ Dropped or Limited

- **Custom LaTeX commands**: `\newcommand`, `\renewcommand`, `\def`, etc., are ignored.
- **Complex environments**: Custom environments (e.g., `\begin{myenv}`) may not convert.
- **Advanced formatting**: Margin adjustments, custom spacing, font changes, etc., are lost.
- **Cross-references**: `\label` and `\ref` may not translate to Markdown links.
- **BibTeX citations**: While Pandoc supports citations, complex LaTeX bibliography setups may not convert cleanly to Markdown[9].
- **Images and figures**: Image paths are preserved, but LaTeX figure environments may need manual adjustment.

## Advanced Customization

### Using Templates and Metadata

- **YAML metadata**: Add a YAML header to your LaTeX file (or create a separate file) for title, author, date, etc. Pandoc will carry this into Markdown.
- **Templates**: While templates are more relevant for PDF/HTML output, you can use Lua or Python filters to customize Markdown output (e.g., transform headers, modify lists)[2][10].

### Filters for Fine Control

- **Lua filters**: Modify Pandoc’s abstract syntax tree (AST) to handle custom conversions (e.g., transform specific LaTeX commands into Markdown equivalents)[2][10].
- **Preprocessing**: Use `sed`, `awk`, or a script to remove or replace unsupported LaTeX commands before conversion.

### Handling Citations

- **Basic support**: Pandoc recognizes `\cite{key}` and similar commands if you use `--citeproc` and provide a `.bib` file.
- **Limitations**: Complex LaTeX citation styles or custom bibliography commands may not convert cleanly[9]. Test with your specific bibliography setup.

### Multiple Files

- **Concatenate inputs**: Pandoc can process multiple `.tex` files at once; it concatenates them before conversion[5].
  ```sh
  pandoc -f latex -t markdown --mathjax -o combined.md chap1.tex chap2.tex
  ```

## Workflow Tips

- **Clean up LaTeX first**: Remove or simplify custom commands, environments, and advanced formatting for smoother conversion.
- **Verify math**: Check that all math expressions are correctly wrapped in `$...$` or `$$...$$`.
- **Manual review**: After conversion, review the Markdown for any dropped content or formatting quirks, especially in tables, figures, and citations.
- **Iterate**: If you have many files or complex documents, script the conversion and review process.

## Example: Before and After

**LaTeX input:**
```latex
\section{Introduction}
Here is a formula: \(E = mc^2\). See Figure~\ref{fig:demo}.

\begin{figure}
  \centering
  \includegraphics{demo.png}
  \caption{Example figure}
  \label{fig:demo}
\end{figure}
```

**Markdown output (simplified):**
```markdown
# Introduction

Here is a formula: $E = mc^2$. See Figure [fig:demo].

![Example figure](demo.png)
```
*Note: Cross-references (`\ref`) may not become clickable links in plain Markdown.*

## Further Reading

- **Pandoc User’s Guide**: Comprehensive documentation on input/output formats, options, and filters[6].
- **Pandoc’s Markdown**: Details on supported syntax (tables, footnotes, math, etc.)[3][8].
- **Community examples**: For edge cases, check Pandoc’s GitHub issues and forums[9].

## Summary Table

| Feature               | Pandoc Support           | Notes                                  |
|-----------------------|-------------------------|----------------------------------------|
| Text & Structure      | Full                    | Headings, lists, paragraphs preserved  |
| Math                  | Full (LaTeX/MathJax)    | Use `--mathjax`                        |
| Tables                | Basic                   | Complex LaTeX tables may need cleanup  |
| Images/Figures        | Partial                 | Paths preserved, environments dropped  |
| Citations             | Basic                   | Complex BibTeX may not convert cleanly |
| Custom LaTeX          | Limited                 | Commands/environments usually dropped  |
| Cross-references      | Limited                 | `\label`/`\ref` may not become links   |

**In short:**  
Use `pandoc -f latex -t markdown --mathjax` for **content and math preservation**. Expect to **lose advanced LaTeX features**—clean up your source or post-process the output as needed. For **maximum control**, consider **preprocessing** and **Lua filters**. Always **review the output** for fidelity to your original content.

[1] https://www.reddit.com/r/LaTeX/comments/hchwvs/latex_pandoc_markdown/
[2] https://www.linkedin.com/pulse/how-generate-professional-reports-using-markdown-pandoc-boukhetta-etpac
[3] https://mushiyo.github.io/pandoc-toc-sidebar/outWithTOC.html
[4] https://tex.stackexchange.com/questions/573431/how-do-i-adapt-a-standard-latex-template-for-pandoc-in-a-docker-container-not
[5] https://www.flutterbys.com.au/stats/tut/tut17.3.html
[6] https://pandoc.org/MANUAL.html
[7] https://forum.literatureandlatte.com/t/latex-pandoc-tutorials/135988
[8] https://github.com/jgm/pandoc/blob/main/README.md
[9] https://github.com/jgm/pandoc/issues/3124
[10] https://ulriklyngs.com/post/2019/02/20/how-to-use-pandoc-filters-for-advanced-customisation-of-your-r-markdown-documents/