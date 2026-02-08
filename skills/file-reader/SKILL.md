---
name: file-reader
description: Read files with proper encoding support for Chinese characters and special paths. Use when reading files in Chinese Windows paths, handling encoding issues, or processing documents with non-ASCII characters.
---

# File Reader Skill

## Usage

### Read Chinese Path Files

Use `read` tool with the full Windows path. The tool automatically handles:
- Chinese characters in paths
- UTF-8 encoding
- Special folder names
- Long paths (>260 characters)

Example:
```
Path: D:\wendy\26.2.4复旦003\关于AI内核探索.txt
```

### Common Issues & Solutions

**Problem**: File not found with Chinese path
**Solution**: Use PowerShell to verify path exists first

**Problem**: Garbled text (encoding issue)
**Solution**: The system automatically uses UTF-8 encoding

### Path Verification Command

```powershell
powershell -Command "Get-Item '完整路径' -ErrorAction SilentlyContinue"
```

## File Types Supported

- `.txt` - Plain text files
- `.md` - Markdown files  
- `.json` - JSON files
- `.docx` - Word documents (basic text extraction)
- `.pptx` - PowerPoint (slides as images/text)
- `.pdf` - PDF documents
- `.png/.jpg/.jpeg` - Images (analyzed via vision model)
- `.mp4/.wav` - Media files (audio transcription via Whisper)
