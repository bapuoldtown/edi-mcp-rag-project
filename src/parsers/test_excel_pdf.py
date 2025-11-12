#!/usr/bin/env python3
"""
Focused Parser Test - Excel and PDF Only

Tests Excel and PDF implementation guide parsing
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.parsers import UniversalParser, parse_document


def print_separator(title=""):
    """Print separator"""
    print("\n" + "=" * 70)
    if title:
        print(f"  {title}")
        print("=" * 70)
    print()


def test_universal_parser_init():
    """Test UniversalParser initialization"""
    print_separator("UniversalParser Initialization")
    
    parser = UniversalParser()
    
    print(f"Parser initialized!")
    print(f"Number of parsers: {len(parser.parsers)}")
    print(f"🔧 Parsers loaded:")
    for p in parser.parsers:
        print(f"   - {p.__class__.__name__}")
    
    print(f"\nSupported formats:")
    formats = parser.get_supported_formats()
    for fmt in formats:
        print(f"   - .{fmt}")
    
    return parser


def test_excel_parser():
    """Test Excel/CSV parsing"""
    print_separator("Excel/CSV Parser Test")
    
    data_dir = Path("data/input")
    
    # Look for Excel/CSV files
    excel_files = (
        list(data_dir.glob("*.xlsx")) + 
        list(data_dir.glob("*.xls")) + 
        list(data_dir.glob("*.csv"))
    )
    
    if not excel_files:
        print("No Excel/CSV files found in data/input/")
        print("\nTo test Excel parser:")
        print("   1. Add Excel implementation guide to data/input/")
        print("   2. Format: Seg, Elem, Name, Req, Type, Min, Max")
        print("   3. Run this test again")
        return
    
    print(f"Found {len(excel_files)} Excel/CSV file(s):\n")
    
    for file_path in excel_files:
        print(f"File: {file_path.name}")
        print(f"   Size: {file_path.stat().st_size / 1024:.2f} KB")
        
        try:
            # Parse with UniversalParser
            doc = parse_document(str(file_path))
            
            print(f"Parsed successfully!")
            print(f"Type: {doc.document_type}")
            print(f"Text length: {len(doc.text)} characters")
            print(f"Tables: {len(doc.tables)}")
            
            if doc.tables:
                table = doc.tables[0]
                print(f"\nTable Details:")
                print(f"      Rows: {table.num_rows}")
                print(f"      Columns: {table.num_columns}")
                print(f"      Headers: {', '.join(table.headers[:5])}")
                if len(table.headers) > 5:
                    print(f"               ... and {len(table.headers) - 5} more")
                
                # Show first few rows
                if table.rows:
                    print(f"\nFirst 3 Rows:")
                    for i, row in enumerate(table.rows[:3], 1):
                        seg = row[0] if len(row) > 0 else ''
                        name = row[2] if len(row) > 2 else ''
                        req = row[3] if len(row) > 3 else ''
                        print(f"      {i}. {seg:4} - {name[:30]:30} ({req})")
            
            print()
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            print()


def test_pdf_parser():
    """Test PDF parsing"""
    print_separator("PDF Parser Test")
    
    data_dir = Path("data/input")
    
    # Look for PDF files
    pdf_files = list(data_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in data/input/")
        print("\nTo test PDF parser:")
        print("   1. Add PDF implementation guide to data/input/")
        print("   2. Should contain tables with segment/element info")
        print("   3. Run this test again")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s):\n")
    
    for file_path in pdf_files:
        print(f"📄 File: {file_path.name}")
        print(f"   Size: {file_path.stat().st_size / 1024:.2f} KB")
        
        try:
            # Parse with UniversalParser
            doc = parse_document(str(file_path))
            
            print(f"Parsed successfully!")
            print(f"Type: {doc.document_type}")
            print(f" Text length: {len(doc.text)} characters")
            print(f"Tables found: {len(doc.tables)}")
            print(f"Pages: {doc.metadata.get('pages', 'unknown')}")
            
            if doc.tables:
                print(f"\nTable Details:")
                for i, table in enumerate(doc.tables[:3], 1):  # First 3 tables
                    print(f"\n      Table {i}:")
                    print(f"         Rows: {table.num_rows}")
                    print(f"         Columns: {table.num_columns}")
                    print(f"         Headers: {', '.join(table.headers[:4])}")
                    if len(table.headers) > 4:
                        print(f"                  ... and {len(table.headers) - 4} more")
                
                if len(doc.tables) > 3:
                    print(f"\n      ... and {len(doc.tables) - 3} more tables")
            
            # Show text preview
            preview = doc.text[:200].replace('\n', ' ')
            if len(doc.text) > 200:
                preview += "..."
            print(f"\n   📖 Text Preview:")
            print(f"      {preview}")
            
            print()
            
        except Exception as e:
            print(f" Error: {e}")
            import traceback
            traceback.print_exc()
            print()


def test_format_detection():
    """Test format detection"""
    print_separator("Format Detection Test")
    
    parser = UniversalParser()
    
    test_files = {
        "implementation_guide.pdf": "PDF",
        "mapping_spec.xlsx": "Excel",
        "segments.csv": "CSV"
    }
    
    print("Testing format detection:\n")
    
    for filename, expected in test_files.items():
        detected = parser.detect_format(filename)
        can_parse = parser.can_parse(filename) if Path("data/input").joinpath(filename).exists() else None
        
        print(f"📄 {filename}")
        print(f"   Expected: {expected}")
        print(f"   Detected: {detected}")
        if can_parse is not None:
            print(f"   Can Parse: {'Yes' if can_parse else ' No'}")
        print()


def test_extraction():
    """Test implementation guide extraction"""
    print_separator("Implementation Guide Extraction Test")
    
    from src.extractors import extract_from_excel, extract_from_pdf
    
    data_dir = Path("data/input")
    
    # Test Excel extraction
    excel_files = list(data_dir.glob("*.xlsx")) + list(data_dir.glob("*.csv"))
    
    if excel_files:
        print("Testing Excel Extraction:\n")
        
        for file_path in excel_files[:1]:  # Test first file
            print(f"File: {file_path.name}")
            
            try:
                impl_guide = extract_from_excel(str(file_path))
                
                print(f"    Extracted successfully!")
                print(impl_guide.summary())
                
                print(f"\n   First 5 Segments:")
                for i, segment in enumerate(impl_guide.segments[:5], 1):
                    print(f"      {i}. {segment.segment_id}: {segment.name}")
                    print(f"         Requirement: {segment.requirement}")
                    print(f"         Elements: {len(segment.elements)}")
                
                if len(impl_guide.segments) > 5:
                    print(f"\n      ... and {len(impl_guide.segments) - 5} more segments")
                
            except Exception as e:
                print(f"   Error: {e}")
            print()
    else:
        print(" No Excel files to extract\n")
    
    # Test PDF extraction
    pdf_files = list(data_dir.glob("*.pdf"))
    
    if pdf_files:
        print("📄 Testing PDF Extraction:\n")
        
        for file_path in pdf_files[:1]:  # Test first file
            print(f"📄 File: {file_path.name}")
            
            try:
                impl_guide = extract_from_pdf(str(file_path))
                
                print(f"  Extracted successfully!")
                print(impl_guide.summary())
                
                print(f"\n  First 5 Segments:")
                for i, segment in enumerate(impl_guide.segments[:5], 1):
                    print(f"      {i}. {segment.segment_id}: {segment.name}")
                    print(f"         Requirement: {segment.requirement}")
                    print(f"         Elements: {len(segment.elements)}")
                
                if len(impl_guide.segments) > 5:
                    print(f"\n      ... and {len(impl_guide.segments) - 5} more segments")
                
            except Exception as e:
                print(f"    Error: {e}")
                import traceback
                traceback.print_exc()
            print()
    else:
        print("📄 No PDF files to extract\n")


def show_usage():
    """Show usage examples"""
    print_separator("Usage Examples")
    
    print("Example 1: Parse with UniversalParser")
    print("""
    from src.parsers import UniversalParser
    
    parser = UniversalParser()  # Only PDF and Excel!
    
    # Parse any supported file
    doc = parser.parse("implementation_guide.pdf")  # PDF
    doc = parser.parse("mapping_spec.xlsx")         # Excel
    doc = parser.parse("segments.csv")              # CSV
    
    print(f"Type: {doc.document_type}")
    print(f"Tables: {len(doc.tables)}")
    """)
    
    print("\n Example 2: Quick Parse")
    print("""
    from src.parsers import parse_document
    
    # One-line parsing!
    doc = parse_document("guide.pdf")
    
    # Access data
    for table in doc.tables:
        print(f"Table: {table.num_rows} rows")
    """)
    
    print("\nExample 3: Extract Implementation Guide")
    print("""
    from src.extractors import extract_from_excel, extract_from_pdf
    
    # From Excel
    impl_guide = extract_from_excel("nike_850_guide.xlsx")
    
    # From PDF
    impl_guide = extract_from_pdf("nike_850_guide.pdf")
    
    # Access segments
    for segment in impl_guide.segments:
        print(f"{segment.segment_id}: {segment.name}")
    """)


def main():
    """Main test function"""
    print_separator("🚀 Focused Parser Test - Excel & PDF Only")
    
    print("Testing:")
    print(" UniversalParser (PDF + Excel only)")
    print(" ExcelParser (Polars-powered! ⚡)")
    print("   PDFParser (pdfplumber)")
    print("   Implementation Guide Extraction")
    
    try:
        # Test 1: Initialize parser
        parser = test_universal_parser_init()
        
        # Test 2: Format detection
        test_format_detection()
        
        # Test 3: Excel parsing
        test_excel_parser()
        
        # Test 4: PDF parsing
        test_pdf_parser()
        
        # Test 5: Extraction
        test_extraction()
        
        # Show usage
        show_usage()
        
        print_separator("✨ Test Complete!")
        
        print("Summary:")
        print("UniversalParser supports: PDF, Excel, CSV")
        print("Automatic format detection")
        print("Automatic parser selection")
        print("Implementation guide extraction")
        print()
        print(" Next Steps:")
        print("  1. Add your implementation guides to data/input/")
        print("     - PDF: nike_850_guide.pdf")
        print("     - Excel: mapping_spec.xlsx")
        print("  2. Run this test again")
        print("  3. See automatic parsing and extraction!")
        
    except Exception as e:
        print(f"\nTest failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())