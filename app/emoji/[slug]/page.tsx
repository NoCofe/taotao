import fs from 'fs';
import path from 'path';
import emojiIndex from '@/data/emojiIndex.json';

interface EmojiData {
  emoji: string;
  name: string;
  meaning_cn: string;
  usage_cn: string;
  meaning_en: string;
  usage_en: string;
}

export async function generateStaticParams() {
  return (emojiIndex as { slug: string }[]).map((e) => ({ slug: e.slug }));
}

export default async function EmojiPage({ params }: { params: { slug: string } }) {
  const filePath = path.join(process.cwd(), 'data', 'generated', `${params.slug}.json`);
  const data = JSON.parse(await fs.promises.readFile(filePath, 'utf8')) as EmojiData;

  return (
    <main>
      <h1>
        {data.emoji} {data.name}
      </h1>
      <section>
        <h2>中文含义</h2>
        <p>{data.meaning_cn}</p>
        <h3>使用场景</h3>
        <p>{data.usage_cn}</p>
      </section>
      <section>
        <h2>English Meaning</h2>
        <p>{data.meaning_en}</p>
        <h3>Usage</h3>
        <p>{data.usage_en}</p>
      </section>
    </main>
  );
}
