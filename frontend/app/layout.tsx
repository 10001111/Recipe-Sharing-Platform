import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Recipe Sharing Platform',
  description: 'Share and discover amazing recipes',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}

