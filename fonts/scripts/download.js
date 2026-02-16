import { access, writeFile, mkdir, rm, copyFile } from 'fs/promises'
import { execSync } from 'child_process'
import { dirname, join } from 'path'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const SRC_DIR = join(__dirname, '..', 'src')
const TMP_DIR = join(__dirname, '..', '.tmp-download')

const FONTS = [
  {
    name: 'Cormorant Garamond Variable',
    url: 'https://github.com/google/fonts/raw/main/ofl/cormorantgaramond/CormorantGaramond%5Bwght%5D.ttf',
    filename: 'cormorant-garamond-variable.ttf',
  },
  {
    name: 'Cormorant Garamond Italic Variable',
    url: 'https://github.com/google/fonts/raw/main/ofl/cormorantgaramond/CormorantGaramond-Italic%5Bwght%5D.ttf',
    filename: 'cormorant-garamond-italic-variable.ttf',
  },
  {
    name: 'Charter Regular',
    url: 'https://github.com/davidseegert/Bitstream-Charter/raw/master/CharterBT-Roman.otf',
    filename: 'charter-regular.otf',
  },
  {
    name: 'Charter Bold',
    url: 'https://github.com/davidseegert/Bitstream-Charter/raw/master/CharterBT-Bold.otf',
    filename: 'charter-bold.otf',
  },
  {
    name: 'Charter Italic',
    url: 'https://github.com/davidseegert/Bitstream-Charter/raw/master/CharterBT-Italic.otf',
    filename: 'charter-italic.otf',
  },
  {
    name: 'Charter Bold Italic',
    url: 'https://github.com/davidseegert/Bitstream-Charter/raw/master/CharterBT-BoldItalic.otf',
    filename: 'charter-bold-italic.otf',
  },
  {
    name: 'Inter Variable',
    url: 'https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf',
    filename: 'inter-variable.ttf',
  },
  {
    name: 'Inter Italic Variable',
    url: 'https://github.com/google/fonts/raw/main/ofl/inter/Inter-Italic%5Bopsz%2Cwght%5D.ttf',
    filename: 'inter-italic-variable.ttf',
  },
  {
    name: 'Commit Mono Variable',
    url: 'https://raw.githubusercontent.com/eigilnikolajsen/commit-mono/main/src/fonts/fontlab/CommitMonoV143-VF.ttf',
    filename: 'commit-mono-variable.ttf',
  },
  {
    name: 'LXGW WenKai Regular',
    url: 'https://github.com/lxgw/LxgwWenKai/releases/download/v1.521/LXGWWenKai-Regular.ttf',
    filename: 'lxgw-wenkai-regular.ttf',
  },
  {
    name: 'Noto Sans SC Variable',
    url: 'https://github.com/google/fonts/raw/main/ofl/notosanssc/NotoSansSC%5Bwght%5D.ttf',
    filename: 'noto-sans-sc-variable.ttf',
  },
  {
    name: 'Tiro Devanagari Hindi Regular',
    url: 'https://github.com/google/fonts/raw/main/ofl/tirodevanagarihindi/TiroDevanagariHindi-Regular.ttf',
    filename: 'tiro-devanagari-regular.ttf',
  },
  {
    name: 'Noto Sans Devanagari Variable',
    url: 'https://github.com/google/fonts/raw/main/ofl/notosansdevanagari/NotoSansDevanagari%5Bwdth%2Cwght%5D.ttf',
    filename: 'noto-sans-devanagari-variable.ttf',
  },
  {
    name: 'Noto Sans Mono Variable',
    url: 'https://github.com/google/fonts/raw/main/ofl/notosansmono/NotoSansMono%5Bwdth%2Cwght%5D.ttf',
    filename: 'noto-sans-mono-variable.ttf',
  },
]

const ARCHIVES = [
  {
    name: 'Sarasa Mono SC Regular',
    url: 'https://github.com/be5invis/Sarasa-Gothic/releases/download/v1.0.36/SarasaMonoSC-TTF-1.0.36.7z',
    archiveFile: 'SarasaMonoSC-TTF-1.0.36.7z',
    extract: 'SarasaMonoSC-Regular.ttf',
    filename: 'sarasa-mono-sc-regular.ttf',
  },
]

async function fileExists(path) {
  try {
    await access(path)
    return true
  } catch {
    return false
  }
}

async function downloadFont({ name, url, filename }) {
  const dest = join(SRC_DIR, filename)

  if (await fileExists(dest)) {
    console.log(`  [skip] ${name}`)
    return
  }

  console.log(`  [download] ${name}`)
  const res = await fetch(url, { redirect: 'follow' })

  if (!res.ok) {
    throw new Error(`Failed: ${name} (${res.status})`)
  }

  const buffer = Buffer.from(await res.arrayBuffer())
  await writeFile(dest, buffer)
  console.log(`  [done] ${name} (${(buffer.length / 1024).toFixed(1)} KB)`)
}

async function downloadArchive({ name, url, archiveFile, extract, filename }) {
  const dest = join(SRC_DIR, filename)

  if (await fileExists(dest)) {
    console.log(`  [skip] ${name}`)
    return
  }

  await mkdir(TMP_DIR, { recursive: true })
  const archivePath = join(TMP_DIR, archiveFile)

  console.log(`  [download] ${name} (archive)`)
  const res = await fetch(url, { redirect: 'follow' })

  if (!res.ok) {
    throw new Error(`Failed: ${name} (${res.status})`)
  }

  const buffer = Buffer.from(await res.arrayBuffer())
  await writeFile(archivePath, buffer)
  console.log(`  [extract] ${extract}`)

  execSync(`7z e -y -o"${TMP_DIR}" "${archivePath}" "${extract}"`, { stdio: 'pipe' })

  const extracted = join(TMP_DIR, extract)
  if (!(await fileExists(extracted))) {
    throw new Error(`${extract} not found in archive`)
  }

  await copyFile(extracted, dest)
  await rm(TMP_DIR, { recursive: true })
  console.log(`  [done] ${name}`)
}

console.log('Downloading font sources...\n')

for (const font of FONTS) {
  await downloadFont(font)
}

for (const archive of ARCHIVES) {
  await downloadArchive(archive)
}

console.log('\nAll fonts downloaded.')
