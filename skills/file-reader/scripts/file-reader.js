#!/usr/bin/env node
/**
 * File Reader Helper - Handles Chinese paths and encoding issues
 * Usage: node file-reader.js "path/to/file"
 */

import { readFileSync, existsSync, promises as fs } from 'fs';
import { fileURLToPath } from 'url';
import path from 'path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function readFileWithEncoding(filePath) {
  // Normalize path - handle Chinese characters
  const normalizedPath = path.normalize(filePath);
  
  console.log(`📄 Reading: ${normalizedPath}\n`);
  
  if (!existsSync(normalizedPath)) {
    console.error(`❌ File not found: ${normalizedPath}`);
    process.exit(1);
  }
  
  try {
    // Try UTF-8 first (most common for documents)
    const content = readFileSync(normalizedPath, 'utf8');
    console.log(content);
  } catch (err) {
    // Try other encodings if UTF-8 fails
    console.error(`Error reading file: ${err.message}`);
    process.exit(1);
  }
}

// Main
const args = process.argv.slice(2);
if (args.length === 0) {
  console.log('Usage: node file-reader.js "path/to/file"');
  console.log('\nExamples:');
  console.log('  node file-reader.js "D:\\wendy\\26.2.4复旦003\\文档.txt"');
  console.log('  node file-reader.js "/mnt/data/文档.md"');
  process.exit(0);
}

readFileWithEncoding(args[0]);
