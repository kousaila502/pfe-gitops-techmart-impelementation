import re
import os
from collections import Counter

def extract_citations_from_file(file_path):
    """Extract all citations from a single .tex file"""
    citations = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Pattern to match \cite{...} with support for multiple refs
        cite_pattern = r'\\cite\{([^}]+)\}'
        matches = re.findall(cite_pattern, content)
        
        for match in matches:
            # Split multiple citations like \cite{ref1,ref2,ref3}
            refs = [ref.strip() for ref in match.split(',')]
            citations.extend(refs)
            
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return citations

def scan_chapters_directory():
    """Scan all .tex files in the chapters directory"""
    chapters_dir = "."  # Current directory (chapters)
    tex_files = [f for f in os.listdir(chapters_dir) if f.endswith('.tex')]
    
    all_citations = []
    file_citations = {}
    
    print("Scanning LaTeX files for citations...\n")
    print("=" * 60)
    
    for tex_file in sorted(tex_files):
        file_path = os.path.join(chapters_dir, tex_file)
        citations = extract_citations_from_file(file_path)
        
        if citations:
            file_citations[tex_file] = citations
            all_citations.extend(citations)
            print(f"\n📄 {tex_file}:")
            print(f"   Found {len(citations)} citation(s)")
            for citation in sorted(set(citations)):
                count = citations.count(citation)
                print(f"   - {citation} ({count} time{'s' if count > 1 else ''})")
        else:
            print(f"\n📄 {tex_file}: No citations found")
    
    return all_citations, file_citations

def generate_bibliography_template(citations):
    """Generate a template .bib file with all found citations"""
    unique_citations = sorted(set(citations))
    
    bib_content = """% Generated bibliography template
% Please fill in the actual publication details

"""
    
    for citation in unique_citations:
        # Try to guess the type based on citation name
        if any(word in citation.lower() for word in ['docs', 'documentation', 'manual']):
            entry_type = "misc"
            template = f"""@{entry_type}{{{citation},
    title = {{{citation.replace('_', ' ').title()}}},
    author = {{{{Organization Name}}}},
    year = {{2024}},
    url = {{https://example.com}},
    note = {{Accessed: 2024-08-20}}
}}

"""
        elif any(word in citation.lower() for word in ['analysis', 'methodology', 'framework']):
            entry_type = "article"
            template = f"""@{entry_type}{{{citation},
    title = {{{citation.replace('_', ' ').title()}}},
    author = {{Author Name}},
    journal = {{Journal Name}},
    year = {{2024}},
    volume = {{1}},
    number = {{1}},
    pages = {{1--10}}
}}

"""
        else:
            entry_type = "misc"
            template = f"""@{entry_type}{{{citation},
    title = {{{citation.replace('_', ' ').title()}}},
    author = {{Author Name}},
    year = {{2024}},
    note = {{Please add publication details}}
}}

"""
        
        bib_content += template
    
    return bib_content

def main():
    print("🔍 LaTeX Citation Detector")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not any(f.endswith('.tex') for f in os.listdir('.')):
        print("❌ No .tex files found in current directory!")
        print("Please run this script from the chapters directory.")
        return
    
    # Extract citations
    all_citations, file_citations = scan_chapters_directory()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    if all_citations:
        citation_counts = Counter(all_citations)
        unique_citations = len(citation_counts)
        total_citations = len(all_citations)
        
        print(f"Total citations found: {total_citations}")
        print(f"Unique citations: {unique_citations}")
        
        print(f"\n📈 Most frequently cited:")
        for citation, count in citation_counts.most_common(5):
            print(f"   {citation}: {count} time{'s' if count > 1 else ''}")
        
        print(f"\n📋 All unique citations:")
        for citation in sorted(citation_counts.keys()):
            print(f"   - {citation}")
        
        # Generate bibliography template
        bib_content = generate_bibliography_template(all_citations)
        
        # Write to file
        with open('references_template.bib', 'w', encoding='utf-8') as f:
            f.write(bib_content)
        
        print(f"\n✅ Generated 'references_template.bib' with {unique_citations} entries")
        print("   Please edit this file to add actual publication details.")
        
        # Generate LaTeX setup instructions
        print(f"\n📝 To use in your LaTeX document, add to preamble:")
        print("   \\usepackage[backend=biber,style=ieee,sorting=none]{biblatex}")
        print("   \\addbibresource{references_template.bib}")
        print("\n   And before \\end{document}:")
        print("   \\printbibliography[title=References]")
        
    else:
        print("❌ No citations found in any .tex files!")
        print("Make sure your citations use the format: \\cite{reference_key}")

if __name__ == "__main__":
    main()