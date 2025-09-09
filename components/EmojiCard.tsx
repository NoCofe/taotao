import Link from 'next/link';

export interface EmojiIndexItem {
  slug: string;
  emoji: string;
  name: string;
}

export default function EmojiCard({ emoji }: { emoji: EmojiIndexItem }) {
  return (
    <Link href={`/emoji/${emoji.slug}`}>
      <div style={{ fontSize: '2rem', margin: '0.5rem 0' }}>
        <span style={{ marginRight: '0.5rem' }}>{emoji.emoji}</span>
        <span>{emoji.name}</span>
      </div>
    </Link>
  );
}
