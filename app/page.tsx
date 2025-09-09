'use client';

import { useState } from 'react';
import EmojiCard, { EmojiIndexItem } from '@/components/EmojiCard';
import emojiIndex from '@/data/emojiIndex.json';

export default function Home() {
  const [query, setQuery] = useState('');

  const results = (emojiIndex as EmojiIndexItem[]).filter((e) =>
    e.name.toLowerCase().includes(query.toLowerCase()) || e.emoji.includes(query)
  );

  return (
    <main>
      <h1>Emoji 百科</h1>
      <input
        placeholder="Search emoji"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <div>
        {results.map((e) => (
          <EmojiCard key={e.slug} emoji={e} />
        ))}
      </div>
    </main>
  );
}
