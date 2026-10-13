#!/usr/bin/env node
/**
 * Auto-Catalog Synchronizer for Satyender Parihar's GitHub Profile README.
 * Automatically discovers all public repositories of Satyenderparihar,
 * categorizes them into structured domains, and updates the Profile README.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const USERNAME = 'Satyenderparihar';

const CATEGORIES = [
  {
    id: 'trading',
    title: '📈 1. Financial Markets & Trading Systems (ट्रेडिंग एवं फिनटेक)',
    default_badge: ['Trading', '00ff88'],
    keywords: ['trading', 'market', 'forex', 'stock', 'smc', 'nifty', 'pine', 'crypto', 'finance', 'fvg', 'order-block']
  },
  {
    id: 'free_tokens',
    title: '🎁 2. Free LLM Tokens & Zero-Cost AI Routing (फ्री टोकन्स एवं AI राउटर्स)',
    default_badge: ['AI Router', '00ff88'],
    keywords: ['freellmapi', 'gpt4free', 'free-for-dev', 'claude-code', 'tokens', 'router', 'free-tier']
  },
  {
    id: 'ai_agents',
    title: '🤖 3. AI Agents & Large Language Models (एआई एजेंट्स एवं एलएलएम)',
    default_badge: ['AI-Agent', '7928ca'],
    keywords: ['agent', 'ai-agent', 'agentic', 'llm', 'rag', 'appflowy', 'transformers', 'langchain', 'crewai', 'genai', 'generative', 'lora', 'handsonllm']
  },
  {
    id: 'automation',
    title: '⚡ 4. Workflow Automation & Low-Code Pipelines (वर्कफ़्लो ऑटोमेशन)',
    default_badge: ['Automation', '00ff88'],
    keywords: ['workflow', 'automation', 'n8n', 'pipeline', 'notifier', 'reels', 'bot', 'crawler', 'extractor', 'cron', 'webhook']
  },
  {
    id: 'office',
    title: '📝 5. Free Office Suites & Desktop Productivity (फ्री ऑफिस एवं प्रोडक्टिविटी टूल्स)',
    default_badge: ['Productivity', '00ff88'],
    keywords: ['office', 'word', 'excel', 'powerpoint', 'wordcraft', 'gridcraft', 'deckcraft', 'photocraft', 'pdf', 'docx', 'xlsx', 'sheet', 'document', 'editor', 'productivity', 'writer']
  },
  {
    id: 'resources',
    title: '📚 6. Developer Directories & Knowledge Hubs (रिसोर्सेज एवं बुक्स)',
    default_badge: ['Resources', 'ffd700'],
    keywords: ['awesome', 'roadmap', 'interview', 'learning', 'books', 'datasets', 'apis', 'directory', 'cheatsheet', 'tutorial', 'curriculum', 'devtools', 'programming']
  }
];

const CUSTOM_REPOS = {
  'Genius-Trading-Wallah': {
    category: 'trading',
    desc: '🏛️ 100% Free Indian Stock Market, Forex, F&O & SMC Masterclass (880+ Lessons, Cheat Sheets & Pine Scripts).',
    stack: 'Markdown, MkDocs, Pine Script v5',
    badge_text: 'Flagship',
    badge_color: '00ff88'
  },
  'freellmapi': {
    category: 'free_tokens',
    desc: '⚡ 7.4 Billion free tokens/month router across 34 free providers & 635 endpoints behind one OpenAI-compatible /v1 endpoint.',
    stack: 'TypeScript, Node.js, Fastify, Docker',
    badge_text: '7.4B Tokens',
    badge_color: '00ff88'
  },
  'gpt4free': {
    category: 'free_tokens',
    desc: '🔥 Official gpt4free engine — access top-tier LLMs (Claude, GPT, DeepSeek, Gemini) without API subscription costs.',
    stack: 'Python, AsyncIO, Multi-Provider',
    badge_text: '66k Stars',
    badge_color: 'ffd700'
  },
  'free-for-dev': {
    category: 'free_tokens',
    desc: '🌐 Massive curated encyclopedia of every SaaS, PaaS, IaaS & API service offering free developer tiers and credits.',
    stack: 'Markdown, Open Directory',
    badge_text: '85k Stars',
    badge_color: '00e5ff'
  },
  'Claude-Code-Unlimited-Workflow': {
    category: 'free_tokens',
    desc: '⚡ High-speed, unlimited Claude Code developer workflow with Astro, Tailwind v4 and built-in engineering agent skills.',
    stack: 'Astro, TypeScript, Tailwind v4',
    badge_text: 'Workflow',
    badge_color: 'ff007f'
  },
  'open-dot': {
    category: 'ai_agents',
    desc: '🤖 Open-source personal AI agents that work on their own, on their own computers. Mac app, OpenAI + Composio.',
    stack: 'TypeScript',
    badge_text: 'AI-Agent',
    badge_color: '7928ca'
  },
  'AppFlowy': {
    category: 'ai_agents',
    desc: '🤖 Bring projects, wikis, and teams together with AI. AppFlowy is the AI collaborative workspace where you achieve more without losing control.',
    stack: 'Dart',
    badge_text: 'AI-Agent',
    badge_color: '7928ca'
  },
  'Agent-Reach': {
    category: 'ai_agents',
    desc: '🤖 Give your AI agent eyes to see the entire internet. Read & search Twitter, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu — one CLI, zero API fees.',
    stack: 'Python',
    badge_text: 'AI-Agent',
    badge_color: '7928ca'
  },
  'generative-ai-for-beginners': {
    category: 'ai_agents',
    desc: '🤖 21 In-Depth Lessons, Get Started Building with Generative AI (Microsoft Curriculum).',
    stack: 'Jupyter Notebook, Python, LLMs',
    badge_text: 'Curriculum',
    badge_color: '7928ca'
  },
  'awesome-llm-apps-Ai-Agents': {
    category: 'ai_agents',
    desc: '🤖 Curated collection of cutting-edge AI Agent architectures, autonomous reasoning loops & multi-agent systems.',
    stack: 'Python, LangChain, CrewAI, AutoGen',
    badge_text: 'Curated',
    badge_color: '00e5ff'
  },
  'Hands-On-LLM-Study': {
    category: 'ai_agents',
    desc: '🧠 Comprehensive study guide covering Transformer architectures, RAG vector search, Fine-Tuning (LoRA) & alignment.',
    stack: 'Python, PyTorch, Transformers, RAG',
    badge_text: 'Study Guide',
    badge_color: 'ffd700'
  },
  'handsOnLLM': {
    category: 'ai_agents',
    desc: '💻 Practical Jupyter notebooks, code implementations, vector DB indexing & open-source LLM experimentation.',
    stack: 'Python, Jupyter, LlamaIndex, FAISS',
    badge_text: 'Code Lab',
    badge_color: 'ff007f'
  },
  'n8n-workflow-templates': {
    category: 'automation',
    desc: '⚡ Production-ready n8n workflow automation templates for AI agents, multi-model LLMs, webhooks & CRM sync.',
    stack: 'n8n, Webhooks, REST APIs, JSON',
    badge_text: 'Templates',
    badge_color: '00ff88'
  },
  'n8n-workflows': {
    category: 'automation',
    desc: '🐳 Enterprise-grade automated pipeline suite with custom Docker containers, Python API server & background jobs.',
    stack: 'Docker, Python, FastAPI, n8n',
    badge_text: 'Engine',
    badge_color: '00e5ff'
  },
  'instagram-reels-notifier': {
    category: 'automation',
    desc: '🎬 24/7 Cloud Auto-Pilot Instagram Reels Tracker & Telegram Notifier powered by GitHub Actions & Node.js.',
    stack: 'Node.js, GitHub Actions Cron',
    badge_text: '24/7 Cloud',
    badge_color: '00e5ff'
  },
  'wordcraft': {
    category: 'office',
    desc: '📝 100% Free Pure Rust clean-room Microsoft Word alternative — Native .docx support, classic Ribbon UI, zero telemetry, lightning fast.',
    stack: 'Rust, Native Win32, docx',
    badge_text: 'MS Word Alt',
    badge_color: '00ff88'
  },
  'projects_realestate': {
    category: 'resources',
    desc: '🛠️ Build and Deploy a Real Estate React & Next.js Application.',
    stack: 'JavaScript, React, Next.js',
    badge_text: 'DevTools',
    badge_color: '00e5ff'
  },
  'freeCodeCamp': {
    category: 'resources',
    desc: '⚡ FreeCodeCamp.org open-source codebase and curriculum for learning to code.',
    stack: 'TypeScript, Full-Stack',
    badge_text: 'DevTools',
    badge_color: '00e5ff'
  },
  'developer-roadmap': {
    category: 'resources',
    desc: '⚡ Interactive roadmaps, guides and other educational content for developers.',
    stack: 'TypeScript, Web Guides',
    badge_text: 'DevTools',
    badge_color: '00e5ff'
  },
  'project-based-learning': {
    category: 'resources',
    desc: '📚 Curated list of project-based tutorials in diverse programming languages.',
    stack: 'Python, Multi-Stack',
    badge_text: 'Resources',
    badge_color: 'ffd700'
  },
  'coding-interview-university': {
    category: 'resources',
    desc: '🛠️ A complete computer science study plan to become a software engineer.',
    stack: 'Multi-Stack, CS Fundamentals',
    badge_text: 'DevTools',
    badge_color: '00e5ff'
  },
  'free-programming-books': {
    category: 'resources',
    desc: '📚 Freely available programming books, courses & cheatsheets.',
    stack: 'Open Directory, Books',
    badge_text: 'Resources',
    badge_color: 'ffd700'
  },
  'awesome-python': {
    category: 'resources',
    desc: '📚 The definitive list that answers "I want to do X in Python, which tool should I use?"',
    stack: 'Python Ecosystem',
    badge_text: 'Resources',
    badge_color: 'ffd700'
  },
  'system-design-primer': {
    category: 'resources',
    desc: '🛠️ Learn how to design large-scale systems. Prep for system design interviews.',
    stack: 'Python, Distributed Systems',
    badge_text: 'DevTools',
    badge_color: '00e5ff'
  },
  'public-apis': {
    category: 'resources',
    desc: '📚 A collective list of free APIs for developers.',
    stack: 'REST APIs, Open Data',
    badge_text: 'Resources',
    badge_color: 'ffd700'
  },
  'build-your-own-x': {
    category: 'resources',
    desc: '📚 Master programming by recreating your favorite technologies from scratch.',
    stack: 'Markdown, Hands-on CS',
    badge_text: 'Resources',
    badge_color: 'ffd700'
  },
  'awesome-free-apps': {
    category: 'resources',
    desc: '📚 Curated list of the best free apps for PC and mobile.',
    stack: 'Curated Apps, Productivity',
    badge_text: 'Resources',
    badge_color: 'ffd700'
  },
  'awesome-public-datasets': {
    category: 'resources',
    desc: '📚 A topic-centric list of high-quality open datasets for AI & ML.',
    stack: 'Big Data, ML Datasets',
    badge_text: 'Resources',
    badge_color: 'ffd700'
  },
  'Useful-Websites': {
    category: 'resources',
    desc: '🌐 Hand-curated directory of essential developer tools, free API suites, design resources & trading utilities.',
    stack: 'Markdown, Curated Links',
    badge_text: 'Directory',
    badge_color: 'ffd700'
  },
  'Pragramming': {
    category: 'resources',
    desc: '📚 Massive collection of free programming books, system design roadmaps & computer science curriculum.',
    stack: 'Markdown, CS Library',
    badge_text: 'Library',
    badge_color: '9cf'
  }
};

async function fetchRepositories(username) {
  const token = process.env.GITHUB_TOKEN;
  let repos = [];
  let page = 1;

  try {
    while (true) {
      const url = `https://api.github.com/users/${username}/repos?per_page=100&page=${page}&sort=updated`;
      const headers = { 'User-Agent': 'AutoCatalogSync' };
      if (token) headers['Authorization'] = `token ${token}`;

      const res = await fetch(url, { headers });
      if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
      const data = await res.json();
      if (!data || data.length === 0) break;
      repos = repos.concat(data);
      page++;
      if (data.length < 100) break;
    }
    return repos;
  } catch (err) {
    console.warn(`Direct fetch failed (${err.message}). Trying gh CLI fallback...`);
    try {
      const out = execSync(`gh repo list ${username} --limit 200 --json name,description,repositoryTopics,primaryLanguage,isFork,url`, { encoding: 'utf-8' });
      const ghRepos = JSON.parse(out);
      return ghRepos.map(r => ({
        name: r.name,
        description: r.description,
        language: r.primaryLanguage ? r.primaryLanguage.name : null,
        topics: r.repositoryTopics ? r.repositoryTopics.map(t => t.name) : []
      }));
    } catch (cliErr) {
      console.error('All fetch strategies failed:', cliErr);
      return repos;
    }
  }
}

function classifyRepo(repo) {
  const name = repo.name || '';
  const desc = (repo.description || '').toLowerCase();
  const topics = (repo.topics || []).map(t => t.toLowerCase());
  const combined = `${name.toLowerCase()} ${desc} ${topics.join(' ')}`;

  if (CUSTOM_REPOS[name]) {
    const catId = CUSTOM_REPOS[name].category;
    const found = CATEGORIES.find(c => c.id === catId);
    if (found) return found;
  }

  for (const cat of CATEGORIES) {
    for (const kw of cat.keywords) {
      if (combined.includes(kw.toLowerCase())) {
        return cat;
      }
    }
  }

  return CATEGORIES[CATEGORIES.length - 1]; // Default to resources
}

function buildMarkdownCatalog(repos) {
  const grouped = {};
  for (const cat of CATEGORIES) grouped[cat.id] = [];

  for (const r of repos) {
    const name = r.name || '';
    if (name === USERNAME) continue; // Exclude profile README repo itself

    const cat = classifyRepo(r);
    let desc, stack, badgeText, badgeColor;

    if (CUSTOM_REPOS[name]) {
      const c = CUSTOM_REPOS[name];
      desc = c.desc;
      stack = c.stack;
      badgeText = c.badge_text;
      badgeColor = c.badge_color;
    } else {
      desc = `⚡ ${r.description || 'Open-source project.'}`;
      stack = r.language || 'Multi-Stack';
      badgeText = cat.default_badge[0];
      badgeColor = cat.default_badge[1];
    }

    const url = `https://github.com/${USERNAME}/${name}`;
    const badgeUrl = `https://img.shields.io/badge/${encodeURIComponent(badgeText)}-${badgeColor}?style=flat-square`;
    const row = `| [**${name}**](${url}) | ${desc} | ${stack} | ![${badgeText}](${badgeUrl}) |`;
    grouped[cat.id].push(row);
  }

  const lines = [
    '## 🗂️ Curated Repository Catalog (व्यवस्थित रिपोजिटरी डायरेक्टरी)',
    '',
    '> *नीचे सभी उपयोगी रिपोजिटरीज़ को उनकी विशेषज्ञता और डोमेन के आधार पर 6 मुख्य श्रेणियों में व्यवस्थित किया गया है (Auto-Synced via GitHub Actions):*',
    ''
  ];

  for (const cat of CATEGORIES) {
    const rows = grouped[cat.id];
    if (!rows || rows.length === 0) continue;

    lines.push(`### ${cat.title}`);
    lines.push('| Repository | Description & Highlights | Core Stack | Status |');
    lines.push('|---|---|---|:---:|');
    for (const row of rows) lines.push(row);
    lines.push('');
    lines.push('---');
    lines.push('');
  }

  return lines.join('\n');
}

function updateReadme(readmePath, catalogMd) {
  let content = fs.readFileSync(readmePath, 'utf-8');
  const startTag = '<!-- AUTO-CATALOG:START -->';
  const endTag = '<!-- AUTO-CATALOG:END -->';

  let updated;
  if (content.includes(startTag) && content.includes(endTag)) {
    const regex = new RegExp(`${startTag}[\\s\\S]*?${endTag}`, 'g');
    updated = content.replace(regex, `${startTag}\n\n${catalogMd}\n\n${endTag}`);
  } else {
    // Replace section between header and Spotlight
    const regex = /## 🗂️ Curated Repository Catalog[\s\S]*?(?=## 🎬 Featured Innovations Spotlight|## 🎬 Cloud Auto-Pilot Spotlight)/;
    if (regex.test(content)) {
      updated = content.replace(regex, `${startTag}\n\n${catalogMd}\n\n${endTag}\n\n`);
    } else {
      console.error('Could not find insertion marker in README.md');
      return false;
    }
  }

  fs.writeFileSync(readmePath, updated, 'utf-8');
  return true;
}

async function main() {
  const rootDir = path.resolve(__dirname, '..');
  const readmePath = path.join(rootDir, 'README.md');

  console.log(`Discovering all repositories for ${USERNAME}...`);
  const repos = await fetchRepositories(USERNAME);
  console.log(`Found ${repos.length} public repositories.`);

  console.log('Generating categorized markdown table...');
  const catalogMd = buildMarkdownCatalog(repos);

  console.log('Syncing into README.md...');
  if (updateReadme(readmePath, catalogMd)) {
    console.log('✅ Successfully updated README.md with categorized catalog!');
  } else {
    process.exit(1);
  }
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
