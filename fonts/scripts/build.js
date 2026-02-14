import { fontSplit } from 'cn-font-split'
import { mkdir, rm, readdir, readFile, writeFile, copyFile } from 'fs/promises'
import { existsSync } from 'fs'
import { join, dirname } from 'path'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const ROOT = join(__dirname, '..')
const DIST = join(ROOT, 'dist')
const SRC = join(ROOT, 'src')
const TMP = join(ROOT, '.tmp-build')

for (const dir of [DIST, TMP]) {
  if (existsSync(dir)) await rm(dir, { recursive: true })
}
await mkdir(DIST, { recursive: true })

const configs = [
  {
    label: 'Cormorant Garamond Variable',
    input: join(SRC, 'cormorant-garamond-variable.ttf'),
    locale: 'en',
    css: { fontFamily: 'Cormorant Garamond', fontWeight: '300 700', fontDisplay: 'swap' },
  },
  {
    label: 'Cormorant Garamond Italic Variable',
    input: join(SRC, 'cormorant-garamond-italic-variable.ttf'),
    locale: 'en',
    css: { fontFamily: 'Cormorant Garamond', fontWeight: '300 700', fontStyle: 'italic', fontDisplay: 'swap' },
  },
  {
    label: 'Charter Regular',
    input: join(SRC, 'charter-regular.otf'),
    locale: 'en',
    css: { fontFamily: 'Charter', fontWeight: '400', fontDisplay: 'swap' },
  },
  {
    label: 'Charter Bold',
    input: join(SRC, 'charter-bold.otf'),
    locale: 'en',
    css: { fontFamily: 'Charter', fontWeight: '700', fontDisplay: 'swap' },
  },
  {
    label: 'Charter Italic',
    input: join(SRC, 'charter-italic.otf'),
    locale: 'en',
    css: { fontFamily: 'Charter', fontWeight: '400', fontStyle: 'italic', fontDisplay: 'swap' },
  },
  {
    label: 'Charter Bold Italic',
    input: join(SRC, 'charter-bold-italic.otf'),
    locale: 'en',
    css: { fontFamily: 'Charter', fontWeight: '700', fontStyle: 'italic', fontDisplay: 'swap' },
  },
  {
    label: 'Inter Variable',
    input: join(SRC, 'inter-variable.ttf'),
    locale: 'en',
    css: { fontFamily: 'Inter', fontWeight: '100 900', fontDisplay: 'swap' },
  },
  {
    label: 'Commit Mono Variable',
    input: join(SRC, 'commit-mono-variable.ttf'),
    locale: 'en',
    css: { fontFamily: 'Commit Mono', fontWeight: '300 700', fontDisplay: 'swap' },
  },
  {
    label: 'LXGW WenKai Regular',
    input: join(SRC, 'lxgw-wenkai-regular.ttf'),
    locale: 'zh',
    css: { fontFamily: 'LXGW WenKai', fontWeight: '400', fontDisplay: 'swap' },
  },
  {
    label: 'Noto Sans SC Variable',
    input: join(SRC, 'noto-sans-sc-variable.ttf'),
    locale: 'zh',
    css: { fontFamily: 'Noto Sans SC', fontWeight: '100 900', fontDisplay: 'swap' },
  },
  {
    label: 'Sarasa Mono SC Regular',
    input: join(SRC, 'sarasa-mono-sc-regular.ttf'),
    locale: 'zh',
    css: { fontFamily: 'Sarasa Mono SC', fontWeight: '400', fontDisplay: 'swap' },
  },
  {
    label: 'Tiro Devanagari Hindi Regular',
    input: join(SRC, 'tiro-devanagari-regular.ttf'),
    locale: 'hi',
    css: { fontFamily: 'Tiro Devanagari Hindi', fontWeight: '400', fontDisplay: 'swap' },
  },
  {
    label: 'Noto Sans Devanagari Variable',
    input: join(SRC, 'noto-sans-devanagari-variable.ttf'),
    locale: 'hi',
    css: { fontFamily: 'Noto Sans Devanagari', fontWeight: '100 900', fontDisplay: 'swap' },
  },
  {
    label: 'Noto Sans Mono Variable',
    input: join(SRC, 'noto-sans-mono-variable.ttf'),
    locale: 'hi',
    css: { fontFamily: 'Noto Sans Mono', fontWeight: '100 900', fontDisplay: 'swap' },
  },
]

const cssChunks = {}

for (const cfg of configs) {
  const tmpDir = join(TMP, `${cfg.locale}-${cfg.label.replace(/\s+/g, '-').toLowerCase()}`)
  await mkdir(tmpDir, { recursive: true })

  console.log(`\nProcessing ${cfg.label}...`)
  try {
    await fontSplit({
      input: cfg.input,
      outDir: tmpDir,
      targetType: 'woff2',
      css: cfg.css,
    })
    console.log(`  [done] ${cfg.label}`)
  } catch (err) {
    console.error(`  [error] ${cfg.label}: ${err.message}`)
    throw err
  }

  const localeDir = join(DIST, cfg.locale)
  await mkdir(localeDir, { recursive: true })

  const files = await readdir(tmpDir)
  for (const f of files.filter(f => f.endsWith('.woff2'))) {
    await copyFile(join(tmpDir, f), join(localeDir, f))
  }

  const cssPath = join(tmpDir, 'result.css')
  if (existsSync(cssPath)) {
    const css = await readFile(cssPath, 'utf8')
    if (!cssChunks[cfg.locale]) cssChunks[cfg.locale] = []
    cssChunks[cfg.locale].push(css)
  }
}

console.log('\nMerging CSS files...')
for (const [locale, chunks] of Object.entries(cssChunks)) {
  const merged = chunks.join('\n')
  const dest = join(DIST, locale, 'index.css')
  await writeFile(dest, merged)

  const localeDir = join(DIST, locale)
  const files = await readdir(localeDir)
  const woff2Count = files.filter(f => f.endsWith('.woff2')).length
  const faceCount = (merged.match(/@font-face/g) || []).length
  console.log(`  ${locale}/: ${faceCount} @font-face rules, ${woff2Count} WOFF2 files`)
}

await rm(TMP, { recursive: true })

console.log('\nDone!')
