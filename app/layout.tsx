import './globals.css';
import type { ReactNode } from 'react';

export const metadata = {
  title: 'Emoji 百科',
  description: 'Explore emoji meanings and usage',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
