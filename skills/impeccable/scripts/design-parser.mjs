// Parse a DESIGN.md document into a stable structured model for Impeccable.
//
// Compatibility goals:
// - preserve the legacy six-section DESIGN.md subset and its established parser shapes;
// - understand the current portable/Google-alpha eight-section model;
// - preserve unknown H2 sections instead of treating them as invalid;
// - parse the YAML subset used by DESIGN.md, including `omitted` arrays;
// - stay dependency-free for live-mode use.

const SECTION_ALIASES = new Map([
  ['overview', 'Overview'],
  ['brand & style', 'Overview'],
  ['brand and style', 'Overview'],
  ['colors', 'Colors'],
  ['typography', 'Typography'],
  ['layout', 'Layout'],
  ['layout & spacing', 'Layout'],
  ['layout and spacing', 'Layout'],
  ['elevation', 'Elevation & Depth'],
  ['elevation & depth', 'Elevation & Depth'],
  ['elevation and depth', 'Elevation & Depth'],
  ['shapes', 'Shapes'],
  ['components', 'Components'],
  ["do's and don'ts", "Do's and Don'ts"],
  ['dos and donts', "Do's and Don'ts"],
  ['do’s and don’ts', "Do's and Don'ts"],
]);

const CANONICAL_SECTIONS = [
  'Overview',
  'Colors',
  'Typography',
  'Layout',
  'Elevation & Depth',
  'Shapes',
  'Components',
  "Do's and Don'ts",
];

function normalizeApostrophes(value) {
  return String(value ?? '').replace(/[\u2018\u2019]/g, "'");
}

function stripInlineYamlComment(value) {
  let quote = null;
  for (let i = 0; i < value.length; i += 1) {
    const ch = value[i];
    if (quote) {
      if (ch === quote && value[i - 1] !== '\\') quote = null;
      continue;
    }
    if (ch === '"' || ch === "'") {
      quote = ch;
      continue;
    }
    if (ch === '#' && i > 0 && /\s/.test(value[i - 1])) {
      return value.slice(0, i).trimEnd();
    }
  }
  return value;
}

function findTopLevelColon(value) {
  let quote = null;
  for (let i = 0; i < value.length; i += 1) {
    const ch = value[i];
    if (quote) {
      if (ch === quote && value[i - 1] !== '\\') quote = null;
      continue;
    }
    if (ch === '"' || ch === "'") {
      quote = ch;
      continue;
    }
    if (ch === ':') return i;
  }
  return -1;
}

function parseScalar(raw) {
  const value = stripInlineYamlComment(String(raw).trim());
  if ((value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))) {
    return value.slice(1, -1);
  }
  if (value === 'true') return true;
  if (value === 'false') return false;
  if (value === 'null' || value === '~') return null;
  if (/^-?\d+$/.test(value)) return Number(value);
  if (/^-?(?:\d+\.\d*|\d*\.\d+)$/.test(value)) return Number(value);
  if (value.startsWith('[') && value.endsWith(']')) {
    return value.slice(1, -1).split(',').map((item) => parseScalar(item)).filter((item) => item !== '');
  }
  return value;
}

function preprocessYaml(yaml) {
  return yaml.split(/\r?\n/)
    .map((raw) => ({
      raw,
      indent: raw.match(/^\s*/)?.[0].length ?? 0,
      text: raw.trim(),
    }))
    .filter((line) => line.text && !line.text.startsWith('#'));
}

function parseYamlSubset(yaml) {
  const lines = preprocessYaml(yaml);
  if (lines.length === 0) return {};

  function parseBlock(start, indent) {
    const isArray = lines[start]?.indent === indent && lines[start].text.startsWith('- ');
    const container = isArray ? [] : {};
    let i = start;

    while (i < lines.length) {
      const line = lines[i];
      if (line.indent < indent) break;
      if (line.indent > indent) {
        i += 1;
        continue;
      }

      if (isArray) {
        if (!line.text.startsWith('- ')) break;
        const itemText = line.text.slice(2).trim();
        if (!itemText) {
          if (i + 1 < lines.length && lines[i + 1].indent > indent) {
            const parsed = parseBlock(i + 1, lines[i + 1].indent);
            container.push(parsed.value);
            i = parsed.next;
          } else {
            container.push(null);
            i += 1;
          }
          continue;
        }

        const colon = findTopLevelColon(itemText);
        if (colon === -1) {
          container.push(parseScalar(itemText));
          i += 1;
          continue;
        }

        const obj = {};
        const key = itemText.slice(0, colon).trim();
        const rest = itemText.slice(colon + 1).trim();
        obj[key] = rest ? parseScalar(rest) : null;
        i += 1;

        while (i < lines.length && lines[i].indent > indent) {
          const child = lines[i];
          const childColon = findTopLevelColon(child.text);
          if (childColon === -1) {
            i += 1;
            continue;
          }
          const childKey = child.text.slice(0, childColon).trim();
          const childRest = child.text.slice(childColon + 1).trim();
          if (childRest) {
            obj[childKey] = parseScalar(childRest);
            i += 1;
          } else if (i + 1 < lines.length && lines[i + 1].indent > child.indent) {
            const parsed = parseBlock(i + 1, lines[i + 1].indent);
            obj[childKey] = parsed.value;
            i = parsed.next;
          } else {
            obj[childKey] = {};
            i += 1;
          }
        }
        container.push(obj);
        continue;
      }

      if (line.text.startsWith('- ')) break;
      const colon = findTopLevelColon(line.text);
      if (colon === -1) {
        i += 1;
        continue;
      }
      const key = line.text.slice(0, colon).trim();
      const rest = line.text.slice(colon + 1).trim();
      if (rest) {
        container[key] = parseScalar(rest);
        i += 1;
      } else if (i + 1 < lines.length && lines[i + 1].indent > indent) {
        const parsed = parseBlock(i + 1, lines[i + 1].indent);
        container[key] = parsed.value;
        i = parsed.next;
      } else {
        container[key] = {};
        i += 1;
      }
    }

    return { value: container, next: i };
  }

  return parseBlock(0, lines[0].indent).value;
}

function parseFrontmatter(markdown) {
  const lines = String(markdown ?? '').split(/\r?\n/);
  if (lines[0]?.trim() !== '---') return { frontmatter: null, body: markdown };
  let end = -1;
  for (let i = 1; i < lines.length; i += 1) {
    if (lines[i].trim() === '---') {
      end = i;
      break;
    }
  }
  if (end === -1) return { frontmatter: null, body: markdown };
  const yaml = lines.slice(1, end).join('\n');
  const body = lines.slice(end + 1).join('\n');
  try {
    return { frontmatter: parseYamlSubset(yaml), body };
  } catch {
    return { frontmatter: null, body: markdown };
  }
}

function canonicalSectionName(rawName) {
  const normalized = normalizeApostrophes(rawName)
    .replace(/^\d+\.\s*/, '')
    .trim()
    .toLowerCase();
  if (SECTION_ALIASES.has(normalized)) return SECTION_ALIASES.get(normalized);
  for (const [alias, canonical] of SECTION_ALIASES.entries()) {
    if (normalized.startsWith(`${alias}:`)) return canonical;
  }
  return null;
}

function splitSections(markdown) {
  const lines = String(markdown ?? '').split(/\r?\n/);
  let title = null;
  const canonical = {};
  const custom = [];
  const diagnostics = [];
  let current = null;

  const flush = () => {
    if (!current) return;
    const body = current.lines.join('\n').trim();
    if (current.canonical) {
      if (canonical[current.canonical]) {
        diagnostics.push({
          severity: 'error',
          code: 'duplicate-section',
          section: current.canonical,
        });
      } else {
        canonical[current.canonical] = { ...current, body };
      }
    } else {
      custom.push({ name: current.name, subtitle: current.subtitle, body });
    }
    current = null;
  };

  for (const raw of lines) {
    const line = raw.trimEnd();
    if (!title && /^#\s+/.test(line) && !/^##\s+/.test(line)) {
      title = line.replace(/^#\s+/, '').trim();
      continue;
    }

    const h2 = line.match(/^##\s+(?:\d+\.\s*)?(.+?)\s*$/);
    if (h2) {
      flush();
      const fullName = normalizeApostrophes(h2[1].trim());
      const colon = fullName.indexOf(':');
      const baseName = colon >= 0 ? fullName.slice(0, colon).trim() : fullName;
      const subtitle = colon >= 0 ? fullName.slice(colon + 1).trim() || null : null;
      current = {
        name: baseName,
        subtitle,
        canonical: canonicalSectionName(baseName),
        lines: [],
      };
      continue;
    }

    if (current) current.lines.push(raw);
  }
  flush();
  return { title, sections: canonical, customSections: custom, diagnostics };
}

function splitSubsections(lines) {
  const result = [{ name: null, lines: [] }];
  let current = result[0];
  for (const raw of lines) {
    const match = raw.match(/^###\s+(.+?)\s*$/);
    if (match) {
      current = { name: match[1].trim(), lines: [] };
      result.push(current);
    } else {
      current.lines.push(raw);
    }
  }
  return result;
}

function collectParagraphs(lines) {
  const paragraphs = [];
  let buffer = [];
  const flush = () => {
    if (!buffer.length) return;
    paragraphs.push(buffer.join(' ').trim());
    buffer = [];
  };
  for (const raw of lines) {
    const trimmed = raw.trim();
    if (!trimmed || /^#{1,6}\s/.test(trimmed) || /^[-*]\s+/.test(trimmed)) {
      flush();
      continue;
    }
    buffer.push(trimmed);
  }
  flush();
  return paragraphs.filter(Boolean);
}

function collectBullets(lines) {
  const bullets = [];
  let current = null;
  for (const raw of lines) {
    const match = raw.match(/^\s*[-*]\s+(.+)$/);
    if (match) {
      if (current) bullets.push(current);
      current = match[1].trim();
      continue;
    }
    if (current && /^\s{2,}\S/.test(raw)) {
      current += ` ${raw.trim()}`;
      continue;
    }
    if (!raw.trim() && current) {
      bullets.push(current);
      current = null;
    }
  }
  if (current) bullets.push(current);
  return bullets;
}

function stripBold(value) {
  return String(value ?? '').replace(/\*\*(.+?)\*\*/g, '$1').trim();
}

function extractNamedRules(lines) {
  const rules = [];
  const seen = new Set();
  const add = (name, body) => {
    const cleanName = stripBold(name).replace(/["“”]/g, '').replace(/[.:]\s*$/, '').trim();
    const cleanBody = stripBold(body).replace(/\s+/g, ' ').trim();
    if (!cleanName || !cleanBody || seen.has(cleanName.toLowerCase())) return;
    seen.add(cleanName.toLowerCase());
    rules.push({ name: cleanName, body: cleanBody });
  };

  // Legacy/Impeccable inline form: **The X Rule.** body (possibly continuing).
  const joined = lines.join('\n');
  const inlineStart = /\*\*(The [^*]+?(?:Rule|Principle|Fallback))[.:]?\*\*/gi;
  const matches = [];
  let match;
  while ((match = inlineStart.exec(joined)) !== null) {
    matches.push({ name: match[1], start: match.index, end: inlineStart.lastIndex });
  }
  for (let i = 0; i < matches.length; i += 1) {
    const current = matches[i];
    const end = i + 1 < matches.length ? matches[i + 1].start : joined.length;
    const body = joined.slice(current.end, end).split(/\n#{2,3}\s/)[0];
    add(current.name, body);
  }

  // Heading form: ### The "X" Rule / Principle / Fallback
  for (let i = 0; i < lines.length; i += 1) {
    const heading = lines[i].match(/^###\s+(.+?)\s*$/);
    if (!heading) continue;
    const name = heading[1].replace(/["“”]/g, '').trim();
    if (!/^The\b.*\b(?:Rule|Principle|Fallback)\b/i.test(name)) continue;
    const body = [];
    for (let j = i + 1; j < lines.length; j += 1) {
      if (/^###{0,1}\s/.test(lines[j])) break;
      body.push(lines[j]);
    }
    add(name, body.join(' '));
  }

  // Bullet form: **The X Rule:** body
  for (const bullet of collectBullets(lines)) {
    const bulletMatch = bullet.match(/^\*\*([^*]+?)\*\*\s*(.+)$/);
    if (!bulletMatch) continue;
    const name = bulletMatch[1].replace(/["“”]/g, '').replace(/[.:]\s*$/, '').trim();
    if (/^The\b.*\b(?:Rule|Principle|Fallback)$/i.test(name)) add(name, bulletMatch[2]);
  }
  return rules;
}

function extractOverview(section) {
  if (!section) return null;
  const text = section.lines.join('\n');
  const northStar = text.match(/\*\*(?:Creative North Star|Specific reference):\s*["“]?([^"”\n*]+)["”]?\*\*/i);
  const keyCharacteristics = [];
  const marker = section.lines.findIndex((line) => /\*\*Key Characteristics:\*\*/i.test(line));
  if (marker >= 0) keyCharacteristics.push(...collectBullets(section.lines.slice(marker + 1)).map(stripBold));
  return {
    subtitle: section.subtitle,
    creativeNorthStar: northStar ? northStar[1].trim() : null,
    philosophy: collectParagraphs(section.lines).filter((p) => !/^(Creative North Star|Specific reference|Key Characteristics):/i.test(stripBold(p))),
    keyCharacteristics,
  };
}

const COLOR_PATTERNS = [
  /#[0-9a-fA-F]{3,8}\b/g,
  /(?:rgb|rgba|hsl|hsla|hwb|oklch|oklab|lch|lab|color-mix)\([^\n]+?\)/gi,
];

function collectColorValues(value) {
  const output = [];
  for (const pattern of COLOR_PATTERNS) {
    pattern.lastIndex = 0;
    let match;
    while ((match = pattern.exec(value)) !== null) output.push(match[0]);
  }
  return [...new Set(output)];
}

function detectFormat(value) {
  const v = String(value ?? '').toLowerCase();
  if (v.startsWith('#')) return 'hex';
  if (v.startsWith('oklch')) return 'oklch';
  if (v.startsWith('oklab')) return 'oklab';
  if (v.startsWith('rgb')) return 'rgb';
  if (v.startsWith('hsl')) return 'hsl';
  if (v.startsWith('hwb')) return 'hwb';
  if (v.startsWith('lch')) return 'lch';
  if (v.startsWith('lab')) return 'lab';
  if (v.startsWith('color-mix')) return 'color-mix';
  return 'unknown';
}

function parseColorBullet(bullet) {
  const plain = stripBold(bullet);
  const values = collectColorValues(plain);
  if (!values.length) return null;
  const boldName = bullet.match(/^\*\*(.+?)\*\*/)?.[1] ?? null;
  const name = boldName ? boldName.replace(/\s*\([^)]*\):?$/, '').trim() : null;
  const descriptionMatch = bullet.match(/\)\s*:\s*\*{0,2}\s*(.+)$/);
  const description = descriptionMatch ? stripBold(descriptionMatch[1]) || null : plain;
  return {
    name,
    value: values[0],
    valueRange: values.length > 1 ? values : null,
    format: detectFormat(values[0]),
    description,
  };
}

function extractColors(section) {
  if (!section) return null;
  const subs = splitSubsections(section.lines);
  const groups = [];
  const role = /^(primary|secondary|tertiary|neutral|accent)\b/i;

  for (const sub of subs) {
    const colors = collectBullets(sub.lines).map(parseColorBullet).filter(Boolean);
    if (!colors.length) continue;
    if (!sub.name && colors.every((color) => color.name && role.test(color.name))) {
      for (const color of colors) groups.push({ role: color.name, colors: [color] });
    } else {
      groups.push({ role: sub.name || 'Palette', colors });
    }
  }
  return {
    subtitle: section.subtitle,
    description: collectParagraphs(subs[0].lines).join(' ') || null,
    groups,
    rules: extractNamedRules(section.lines),
  };
}

function normalizeFontRole(raw) {
  const tokens = String(raw).toLowerCase().split(/[-/&\s]+/).filter(Boolean);
  const priority = ['display', 'headline', 'body', 'ui', 'label', 'mono'];
  const canonical = { headline: 'display', ui: 'body' };
  for (const item of priority) {
    if (tokens.includes(item)) return canonical[item] || item;
  }
  return null;
}

function extractTypography(section) {
  if (!section) return null;
  const text = section.lines.join('\n');
  const fonts = {};

  // Legacy explicit form: **Display Font:** Family (with fallback)
  const explicit = /\*\*([\w\s/]+?)Font:\*\*\s*([^\n(]+?)(?:\s*\(with\s+([^)]+)\))?\s*$/gmi;
  let match;
  while ((match = explicit.exec(text)) !== null) {
    const rawRole = match[1].trim().toLowerCase().replace(/\s+/g, '-');
    const role = normalizeFontRole(rawRole) || rawRole;
    fonts[role] = { family: match[2].trim(), fallback: match[3]?.trim() ?? null };
  }

  // Legacy Stitch prose form: **Display & Headlines (Noto Serif):** description
  if (Object.keys(fonts).length === 0) {
    const stitch = /\*\*([\w\s&/]+?)\s*\(([^)]+)\):\*\*\s*(.+)/g;
    while ((match = stitch.exec(text)) !== null) {
      const rawRole = match[1].trim().toLowerCase().replace(/\s*&\s*/g, '-').replace(/\s+/g, '-');
      const role = normalizeFontRole(rawRole) || rawRole;
      fonts[role] = { family: match[2].trim(), fallback: null, purpose: match[3].trim() };
    }
  }

  const hierarchySection = splitSubsections(section.lines).find((sub) => /hierarch/i.test(sub.name ?? ''));
  const hierarchy = hierarchySection
    ? collectBullets(hierarchySection.lines).map((bullet) => {
        const item = bullet.match(/^\*\*(.+?)\*\*\s*\((.+?)\):\s*(.*)$/);
        return item ? { name: item[1].trim(), specs: item[2].split(',').map((s) => s.trim()), purpose: stripBold(item[3]) } : null;
      }).filter(Boolean)
    : [];

  const characterMatch = text.match(/\*\*Character:\*\*\s*([^\n]+(?:\n[^\n]+)*?)(?=\n\n|\n###|\n##|$)/i);
  const paragraphs = collectParagraphs(section.lines).filter(
    (p) => !/^\*\*[\w\s/&]+Font:/i.test(p) && !/^\*\*[\w\s/&]+\([^)]+\):/i.test(p) && !/^\*\*Character:\*\*/i.test(p)
  );
  const character = characterMatch ? characterMatch[1].replace(/\n/g, ' ').trim() : paragraphs[0] ?? null;
  return {
    subtitle: section.subtitle,
    fonts,
    character,
    hierarchy,
    rules: extractNamedRules(section.lines),
  };
}

function extractNarrativeSection(section) {
  if (!section) return null;
  return {
    subtitle: section.subtitle,
    description: collectParagraphs(section.lines).join(' ') || null,
    details: collectBullets(section.lines).map(stripBold),
    rules: extractNamedRules(section.lines),
  };
}

function parseShadowBullet(bullet) {
  const match = bullet.match(/^\*\*(.+?)\*\*\s*\(`?([^`]+?)`?\):\s*(.*)$/);
  if (!match) return null;
  const rawValue = match[2].replace(/^box-shadow:\s*/i, '').trim();
  const looksLikeShadow = /rgba?\(|\b(?:px|rem|em)\b|^-?\d+\s/i.test(rawValue) && /\d/.test(rawValue);
  if (!looksLikeShadow) return null;
  return {
    name: stripBold(match[1]),
    value: rawValue,
    purpose: stripBold(match[3]) || null,
  };
}

function extractElevation(section) {
  if (!section) return null;
  const shadows = [];
  const seen = new Set();
  const addShadow = (entry) => {
    if (!entry) return;
    const key = `${entry.name ?? ''}::${entry.value}`;
    if (seen.has(key)) return;
    seen.add(key);
    shadows.push(entry);
  };

  for (const bullet of collectBullets(section.lines)) addShadow(parseShadowBullet(bullet));

  const shadowRe = /box-shadow\s*:\s*([^`;\n]+)/gi;
  for (const line of section.lines) {
    let match;
    while ((match = shadowRe.exec(line)) !== null) {
      const value = match[1].replace(/[`.)]+$/, '').trim();
      if (value) addShadow({ name: null, value, purpose: null });
    }
  }
  return {
    subtitle: section.subtitle,
    description: collectParagraphs(section.lines).join(' ') || null,
    shadows,
    rules: extractNamedRules(section.lines),
  };
}

function extractComponents(section) {
  if (!section) return null;
  const subs = splitSubsections(section.lines);
  const components = [];
  for (const sub of subs.slice(1)) {
    if (!sub.name) continue;
    const properties = {};
    const variants = [];
    for (const bullet of collectBullets(sub.lines)) {
      const match = bullet.match(/^\*\*(.+?):?\*\*:?\s*(.+)$/);
      if (!match) continue;
      const key = stripBold(match[1]);
      const value = stripBold(match[2]);
      if (/^(primary|secondary|tertiary|ghost|hover|focus|active|pressed|disabled|default|error|selected|unselected|state)\b/i.test(key)) {
        variants.push({ name: key, description: value });
      } else {
        properties[key.toLowerCase()] = value;
      }
    }
    components.push({
      name: sub.name,
      description: collectParagraphs(sub.lines).join(' ') || null,
      properties,
      variants,
    });
  }
  return { subtitle: section.subtitle, components };
}

function extractDosDonts(section) {
  if (!section) return null;
  const dos = [];
  const donts = [];
  for (const bullet of collectBullets(section.lines)) {
    const plain = normalizeApostrophes(stripBold(bullet));
    if (/^don't\b/i.test(plain)) donts.push(plain);
    else if (/^do\b/i.test(plain)) dos.push(plain);
  }
  const subs = splitSubsections(section.lines);
  for (const sub of subs.slice(1)) {
    const name = normalizeApostrophes(sub.name ?? '').toLowerCase().replace(/:$/, '');
    const target = name === 'do' ? dos : name === "don't" || name === 'dont' ? donts : null;
    if (target) {
      for (const bullet of collectBullets(sub.lines).map(stripBold)) {
        if (!target.includes(bullet)) target.push(bullet);
      }
    }
  }
  return { dos, donts };
}

function normalizeOmitted(value) {
  if (!Array.isArray(value)) return [];
  return value.map((item) => {
    if (typeof item === 'string') return { section: item, reason: null };
    if (item && typeof item === 'object' && typeof item.section === 'string') {
      return { section: item.section, reason: item.reason ?? null };
    }
    return null;
  }).filter(Boolean);
}

export function parseDesignMd(markdown) {
  const { frontmatter, body } = parseFrontmatter(markdown);
  const split = splitSections(body);
  const sections = split.sections;
  return {
    schemaVersion: 2,
    designMdFormatVersion: frontmatter?.version ?? null,
    title: split.title,
    frontmatter,
    omitted: normalizeOmitted(frontmatter?.omitted),
    overview: extractOverview(sections.Overview),
    colors: extractColors(sections.Colors),
    typography: extractTypography(sections.Typography),
    layout: extractNarrativeSection(sections.Layout),
    elevation: extractElevation(sections['Elevation & Depth']),
    shapes: extractNarrativeSection(sections.Shapes),
    components: extractComponents(sections.Components),
    dosDonts: extractDosDonts(sections["Do's and Don'ts"]),
    customSections: split.customSections,
    diagnostics: split.diagnostics,
    sectionOrder: CANONICAL_SECTIONS.filter((name) => Boolean(sections[name])),
  };
}

export function assessCoverage(model) {
  return {
    overview: model.overview ? {
      northStar: Boolean(model.overview.creativeNorthStar),
      philosophy: model.overview.philosophy.length > 0,
      keyCharacteristics: model.overview.keyCharacteristics.length,
    } : 'missing',
    colors: model.colors ? {
      groups: model.colors.groups.length,
      totalColors: model.colors.groups.reduce((sum, group) => sum + group.colors.length, 0),
      rules: model.colors.rules.length,
    } : 'missing',
    typography: model.typography ? {
      fonts: Object.keys(model.typography.fonts).length,
      hierarchyEntries: model.typography.hierarchy.length,
      character: Boolean(model.typography.character),
      rules: model.typography.rules.length,
    } : 'missing',
    layout: model.layout ? {
      description: Boolean(model.layout.description),
      details: model.layout.details.length,
      rules: model.layout.rules.length,
    } : 'missing',
    elevation: model.elevation ? {
      shadows: model.elevation.shadows.length,
      rules: model.elevation.rules.length,
      description: Boolean(model.elevation.description),
    } : 'missing',
    shapes: model.shapes ? {
      description: Boolean(model.shapes.description),
      details: model.shapes.details.length,
      rules: model.shapes.rules.length,
    } : 'missing',
    components: model.components ? {
      count: model.components.components.length,
      variantTotal: model.components.components.reduce((sum, component) => sum + component.variants.length, 0),
    } : 'missing',
    dosDonts: model.dosDonts ? {
      dos: model.dosDonts.dos.length,
      donts: model.dosDonts.donts.length,
    } : 'missing',
    omitted: model.omitted?.length ?? 0,
    customSections: model.customSections?.length ?? 0,
    diagnostics: model.diagnostics?.length ?? 0,
  };
}
