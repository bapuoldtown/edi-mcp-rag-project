"""
Plain text parser
"""

import logging
from .base_parser import BaseParser
from .models import ParsedDocument, DocumentType

logger = logging.getLogger(__name__)


class TextParser(BaseParser):
    """Parse plain text files"""
    
    SUPPORTED_EXTENSIONS = ['txt', 'text', 'md', 'markdown', 'log']
    
    def can_parse(self, file_path: str) -> bool:
        """Check if file is text"""
        return self.get_file_extension(file_path) in self.SUPPORTED_EXTENSIONS
    
    def parse(self, file_path: str) -> ParsedDocument:
        """Parse text file"""
        if not self.validate_file(file_path):
            raise ValueError(f"Invalid file: {file_path}")
        
        logger.info(f"Parsing text file: {file_path}")
        
        try:
            with open(file_path, 'r', encoding=self.config.encoding) as f:
                text = f.read()
            
            metadata = {
                'encoding': self.config.encoding,
                'lines': len(text.splitlines()),
                'characters': len(text)
            }
            
            return self.create_parsed_document(
                file_path=file_path,
                document_type=DocumentType.TEXT,
                text=text,
                metadata=metadata
            )
        except UnicodeDecodeError:
            # Try different encodings
            for encoding in ['latin-1', 'cp1252', 'iso-8859-1']:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        text = f.read()
                    
                    metadata = {
                        'encoding': encoding,
                        'lines': len(text.splitlines()),
                        'characters': len(text)
                    }
                    
                    return self.create_parsed_document(
                        file_path=file_path,
                        document_type=DocumentType.TEXT,
                        text=text,
                        metadata=metadata
                    )
                except:
                    continue
            
            raise ValueError(f"Could not decode text file: {file_path}")
