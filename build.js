import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const distDir = path.join(__dirname, 'dist');
if (!fs.existsSync(distDir)) {
    fs.mkdirSync(distDir, { recursive: true });
}

// 1. Copy index.html
const srcHtml = path.join(__dirname, 'index.html');
const destHtml = path.join(distDir, 'index.html');
if (fs.existsSync(srcHtml)) {
    fs.copyFileSync(srcHtml, destHtml);
    console.log('✓ Copied index.html -> dist/index.html');
}

// 2. Copy assets if present
const srcAssets = path.join(__dirname, 'assets');
const destAssets = path.join(distDir, 'assets');
if (fs.existsSync(srcAssets)) {
    fs.cpSync(srcAssets, destAssets, { recursive: true });
    console.log('✓ Copied assets/ -> dist/assets/');
}

console.log('✨ Build finished successfully! Ready for Vercel deployment.');
