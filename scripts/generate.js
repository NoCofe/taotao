const fs = require('fs');
const path = require('path');

const csvPath = path.join(process.cwd(), 'data', 'emoji.csv');
const outDir = path.join(process.cwd(), 'data', 'generated');

const lines = fs.readFileSync(csvPath, 'utf8').trim().split('\n');
const index = [];

for (const line of lines.slice(1)) {
  const [emoji, slug, name] = line.split(',');
  const record = { emoji, slug, name };
  index.push(record);
  const data = {
    ...record,
    meaning_cn: `${name} 的示例中文含义。`,
    usage_cn: `${name} 的示例中文使用场景。`,
    meaning_en: `Sample English meaning for ${name}.`,
    usage_en: `Sample English usage for ${name}.`
  };
  fs.writeFileSync(path.join(outDir, `${slug}.json`), JSON.stringify(data, null, 2));
}

fs.writeFileSync(
  path.join(process.cwd(), 'data', 'emojiIndex.json'),
  JSON.stringify(index, null, 2)
);

console.log('Generated', index.length, 'emoji files');
