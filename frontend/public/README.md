# Public Assets Directory

This directory contains static assets that are served directly by Next.js.

## Structure

```
public/
├── images/          # Image assets (logos, icons, placeholders)
├── icons/           # Favicon and app icons
└── fonts/           # Custom fonts (if any)
```

## Usage

Reference assets using absolute paths starting with `/`:

```tsx
<img src="/images/logo.png" alt="Logo" />
<link rel="icon" href="/icons/favicon.ico" />
```

## Best Practices

1. **Images**: Use Next.js Image component for optimization
2. **Icons**: Use SVG format when possible
3. **Favicon**: Place in root of public directory
4. **File Names**: Use lowercase with hyphens (e.g., `recipe-placeholder.png`)

