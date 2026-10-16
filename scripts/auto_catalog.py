#!/usr/bin/env python3
"""
Auto-Catalog Synchronizer for Satyender Parihar's GitHub Profile README.
Automatically discovers all public repositories of Satyenderparihar,
categorizes them into structured domains, and updates the Profile README.
"""

import json
import os
import re
import sys
import urllib.request

USERNAME = "Satyenderparihar"

CATEGORIES = [
    {
        "id": "trading",
        "title": "📈 1. Financial Markets & Trading Systems (ट्रेडिंग एवं फिनटेक)",
        "default_badge": ("Trading", "00ff88"),
        "keywords": ["trading", "market", "forex", "stock", "smc", "nifty", "pine", "crypto", "finance", "fvg", "order-block"],
    },
    {
        "id": "free_tokens",
        "title": "🎁 2. Free LLM Tokens & Zero-Cost AI Routing (फ्री टोकन्स एवं AI राउटर्स)",
        "default_badge": ("AI Router", "00ff88"),
        "keywords": ["freellmapi", "gpt4free", "free-for-dev", "claude-code", "tokens", "router", "free-tier"],
    },
    {
        "id": "ai_agents",
        "title": "🤖 3. AI Agents & Large Language Models (एआई एजेंट्स एवं एलएलएम)",
        "default_badge": ("AI-Agent", "7928ca"),
        "keywords": ["agent", "ai-agent", "agentic", "llm", "rag", "appflowy", "transformers", "langchain", "crewai", "genai", "generative", "lora", "handsonllm"],
    },
    {
        "id": "automation",
        "title": "⚡ 4. Workflow Automation & Low-Code Pipelines (वर्कफ़्लो ऑटोमेशन)",
        "default_badge": ("Automation", "00ff88"),
        "keywords": ["workflow", "automation", "n8n", "pipeline", "notifier", "reels", "bot", "crawler", "extractor", "cron", "webhook"],
    },
    {
        "id": "office",
        "title": "📝 5. Free Office Suites & Desktop Productivity (फ्री ऑफिस एवं प्रोडक्टिविटी टूल्स)",
        "default_badge": ("Productivity", "00ff88"),
        "keywords": ["office", "word", "excel", "powerpoint", "wordcraft", "gridcraft", "deckcraft", "photocraft", "pdf", "docx", "xlsx", "sheet", "document", "editor", "productivity", "writer"],
    },
    {
        "id": "resources",
        "title": "📚 6. Developer Directories & Knowledge Hubs (रिसोर्सेज एवं बुक्स)",
        "default_badge": ("Resources", "ffd700"),
        "keywords": ["awesome", "roadmap", "interview", "learning", "books", "datasets", "apis", "directory", "cheatsheet", "tutorial", "curriculum", "devtools", "programming"],
    },
    {
        "id": "youtube_media",
        "title": "🎬 7. YouTube Automation & Social Media Bots (यूट्यूब एवं मीडिया बॉट्स)",
        "default_badge": ("YouTube Bot", "ff0000"),
        "keywords": ["youtube", "ytwatchbot", "yt-watch-bot", "studio", "video", "shorts", "faceless", "media", "speech", "transcript", "caption"],
    },
]

# Custom curated metadata for top flagship repos to keep premium look
CUSTOM_REPOS = {
    "Genius-Trading-Wallah": {
        "category": "trading",
        "desc": "🏛️ 100% Free Indian Stock Market, Forex, F&O & SMC Masterclass (880+ Lessons, Cheat Sheets & Pine Scripts).",
        "stack": "Markdown, MkDocs, Pine Script v5",
        "badge_text": "Flagship",
        "badge_color": "00ff88",
    },
    "freellmapi": {
        "category": "free_tokens",
        "desc": "⚡ 7.4 Billion free tokens/month router across 34 free providers & 635 endpoints behind one OpenAI-compatible /v1 endpoint.",
        "stack": "TypeScript, Node.js, Fastify, Docker",
        "badge_text": "7.4B Tokens",
        "badge_color": "00ff88",
    },
    "gpt4free": {
        "category": "free_tokens",
        "desc": "🔥 Official gpt4free engine — access top-tier LLMs (Claude, GPT, DeepSeek, Gemini) without API subscription costs.",
        "stack": "Python, AsyncIO, Multi-Provider",
        "badge_text": "66k Stars",
        "badge_color": "ffd700",
    },
    "free-for-dev": {
        "category": "free_tokens",
        "desc": "🌐 Massive curated encyclopedia of every SaaS, PaaS, IaaS & API service offering free developer tiers and credits.",
        "stack": "Markdown, Open Directory",
        "badge_text": "85k Stars",
        "badge_color": "00e5ff",
    },
    "Claude-Code-Unlimited-Workflow": {
        "category": "free_tokens",
        "desc": "⚡ High-speed, unlimited Claude Code developer workflow with Astro, Tailwind v4 and built-in engineering agent skills.",
        "stack": "Astro, TypeScript, Tailwind v4",
        "badge_text": "Workflow",
        "badge_color": "ff007f",
    },
    "open-dot": {
        "category": "ai_agents",
        "desc": "🤖 Open-source personal AI agents that work on their own, on their own computers. Mac app, OpenAI + Composio.",
        "stack": "TypeScript",
        "badge_text": "AI-Agent",
        "badge_color": "7928ca",
    },
    "AppFlowy": {
        "category": "ai_agents",
        "desc": "🤖 Bring projects, wikis, and teams together with AI. AppFlowy is the AI collaborative workspace where you achieve more without losing control.",
        "stack": "Dart",
        "badge_text": "AI-Agent",
        "badge_color": "7928ca",
    },
    "Agent-Reach": {
        "category": "ai_agents",
        "desc": "🤖 Give your AI agent eyes to see the entire internet. Read & search Twitter, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu — one CLI, zero API fees.",
        "stack": "Python",
        "badge_text": "AI-Agent",
        "badge_color": "7928ca",
    },
    "generative-ai-for-beginners": {
        "category": "ai_agents",
        "desc": "🤖 21 In-Depth Lessons, Get Started Building with Generative AI (Microsoft Curriculum).",
        "stack": "Jupyter Notebook, Python, LLMs",
        "badge_text": "Curriculum",
        "badge_color": "7928ca",
    },
    "awesome-llm-apps-Ai-Agents": {
        "category": "ai_agents",
        "desc": "🤖 Curated collection of cutting-edge AI Agent architectures, autonomous reasoning loops & multi-agent systems.",
        "stack": "Python, LangChain, CrewAI, AutoGen",
        "badge_text": "Curated",
        "badge_color": "00e5ff",
    },
    "Hands-On-LLM-Study": {
        "category": "ai_agents",
        "desc": "🧠 Comprehensive study guide covering Transformer architectures, RAG vector search, Fine-Tuning (LoRA) & alignment.",
        "stack": "Python, PyTorch, Transformers, RAG",
        "badge_text": "Study Guide",
        "badge_color": "ffd700",
    },
    "handsOnLLM": {
        "category": "ai_agents",
        "desc": "💻 Practical Jupyter notebooks, code implementations, vector DB indexing & open-source LLM experimentation.",
        "stack": "Python, Jupyter, LlamaIndex, FAISS",
        "badge_text": "Code Lab",
        "badge_color": "ff007f",
    },
    "n8n-workflow-templates": {
        "category": "automation",
        "desc": "⚡ Production-ready n8n workflow automation templates for AI agents, multi-model LLMs, webhooks & CRM sync.",
        "stack": "n8n, Webhooks, REST APIs, JSON",
        "badge_text": "Templates",
        "badge_color": "00ff88",
    },
    "n8n-workflows": {
        "category": "automation",
        "desc": "🐳 Enterprise-grade automated pipeline suite with custom Docker containers, Python API server & background jobs.",
        "stack": "Docker, Python, FastAPI, n8n",
        "badge_text": "Engine",
        "badge_color": "00e5ff",
    },
    "instagram-reels-notifier": {
        "category": "automation",
        "desc": "🎬 24/7 Cloud Auto-Pilot Instagram Reels Tracker & Telegram Notifier powered by GitHub Actions & Node.js.",
        "stack": "Node.js, GitHub Actions Cron",
        "badge_text": "24/7 Cloud",
        "badge_color": "00e5ff",
    },
    "wordcraft": {
        "category": "office",
        "desc": "📝 100% Free Pure Rust clean-room Microsoft Word alternative — Native .docx support, classic Ribbon UI, zero telemetry, lightning fast.",
        "stack": "Rust, Native Win32, docx",
        "badge_text": "MS Word Alt",
        "badge_color": "00ff88",
    },
    "projects_realestate": {
        "category": "resources",
        "desc": "🛠️ Build and Deploy a Real Estate React & Next.js Application.",
        "stack": "JavaScript, React, Next.js",
        "badge_text": "DevTools",
        "badge_color": "00e5ff",
    },
    "freeCodeCamp": {
        "category": "resources",
        "desc": "⚡ FreeCodeCamp.org open-source codebase and curriculum for learning to code.",
        "stack": "TypeScript, Full-Stack",
        "badge_text": "DevTools",
        "badge_color": "00e5ff",
    },
    "developer-roadmap": {
        "category": "resources",
        "desc": "⚡ Interactive roadmaps, guides and other educational content for developers.",
        "stack": "TypeScript, Web Guides",
        "badge_text": "DevTools",
        "badge_color": "00e5ff",
    },
    "project-based-learning": {
        "category": "resources",
        "desc": "📚 Curated list of project-based tutorials in diverse programming languages.",
        "stack": "Python, Multi-Stack",
        "badge_text": "Resources",
        "badge_color": "ffd700",
    },
    "coding-interview-university": {
        "category": "resources",
        "desc": "🛠️ A complete computer science study plan to become a software engineer.",
        "stack": "Multi-Stack, CS Fundamentals",
        "badge_text": "DevTools",
        "badge_color": "00e5ff",
    },
    "free-programming-books": {
        "category": "resources",
        "desc": "📚 Freely available programming books, courses & cheatsheets.",
        "stack": "Open Directory, Books",
        "badge_text": "Resources",
        "badge_color": "ffd700",
    },
    "awesome-python": {
        "category": "resources",
        "desc": "📚 The definitive list that answers 'I want to do X in Python, which tool should I use?'",
        "stack": "Python Ecosystem",
        "badge_text": "Resources",
        "badge_color": "ffd700",
    },
    "system-design-primer": {
        "category": "resources",
        "desc": "🛠️ Learn how to design large-scale systems. Prep for system design interviews.",
        "stack": "Python, Distributed Systems",
        "badge_text": "DevTools",
        "badge_color": "00e5ff",
    },
    "public-apis": {
        "category": "resources",
        "desc": "📚 A collective collective list of free APIs for developers.",
        "stack": "REST APIs, Open Data",
        "badge_text": "Resources",
        "badge_color": "ffd700",
    },
    "build-your-own-x": {
        "category": "resources",
        "desc": "📚 Master programming by recreating your favorite technologies from scratch.",
        "stack": "Markdown, Hands-on CS",
        "badge_text": "Resources",
        "badge_color": "ffd700",
    },
    "awesome-free-apps": {
        "category": "resources",
        "desc": "📚 Curated list of the best free apps for PC and mobile.",
        "stack": "Curated Apps, Productivity",
        "badge_text": "Resources",
        "badge_color": "ffd700",
    },
    "awesome-public-datasets": {
        "category": "resources",
        "desc": "📚 A topic-centric list of high-quality open datasets for AI & ML.",
        "stack": "Big Data, ML Datasets",
        "badge_text": "Resources",
        "badge_color": "ffd700",
    },
    "Useful-Websites": {
        "category": "resources",
        "desc": "🌐 Hand-curated directory of essential developer tools, free API suites, design resources & trading utilities.",
        "stack": "Markdown, Curated Links",
        "badge_text": "Directory",
        "badge_color": "ffd700",
    },
    "Pragramming": {
        "category": "resources",
        "desc": "📚 Massive collection of free programming books, system design roadmaps & computer science curriculum.",
        "stack": "Markdown, CS Library",
        "badge_text": "Library",
        "badge_color": "9cf",
    },
    "youtube-agentic-ai-studio": {
        "category": "youtube_media",
        "desc": "🎬 Fully Autonomous AI YouTube Studio — Automated Viral Research, Hindi Scriptwriting, Edge-TTS Narration, Dynamic Candlestick Visuals & Auto-Upload.",
        "stack": "Python, Flask, Edge-TTS, MoviePy, Gemini Flash, FFmpeg",
        "badge_text": "AI Studio",
        "badge_color": "ff0000",
    },
    "ytWatchBot": {
        "category": "youtube_media",
        "desc": "📺 Autonomous Telegram Bot for YouTube Channels — Real-time Channel Monitoring, Instant Video/Shorts/Livestream Alerts & PubSubHubbub Webhooks.",
        "stack": "TypeScript, Node.js, Telegram Bot API, PubSub, MariaDB",
        "badge_text": "Telegram Bot",
        "badge_color": "ff0000",
    },
}

def fetch_repositories(username):
    token = os.environ.get("GITHUB_TOKEN")
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}&sort=updated"
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "AutoCatalogSync")
        if token:
            req.add_header("Authorization", f"token {token}")
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if not data:
                    break
                repos.extend(data)
                page += 1
                if len(data) < 100:
                    break
        except Exception as e:
            print(f"Error fetching repos from GitHub API: {e}", file=sys.stderr)
            # Try gh CLI fallback
            try:
                import subprocess
                cmd = f"gh repo list {username} --limit 200 --json name,description,repositoryTopics,primaryLanguage,isFork,url"
                out = subprocess.check_output(cmd, shell=True).decode("utf-8")
                gh_repos = json.loads(out)
                # Normalize structure
                for r in gh_repos:
                    lang = r.get("primaryLanguage")
                    r["language"] = lang.get("name") if lang else None
                    topics = r.get("repositoryTopics")
                    r["topics"] = [t["name"] for t in topics] if topics else []
                return gh_repos
            except Exception as e2:
                print(f"Fallback gh cli also failed: {e2}", file=sys.stderr)
                return repos
    return repos

def classify_repo(repo):
    name = repo.get("name", "")
    desc = (repo.get("description") or "").lower()
    topics = [t.lower() for t in repo.get("topics", [])]
    text = f"{name.lower()} {desc} {' '.join(topics)}"

    # Check custom overrides first
    if name in CUSTOM_REPOS:
        cat_id = CUSTOM_REPOS[name]["category"]
        for cat in CATEGORIES:
            if cat["id"] == cat_id:
                return cat

    # Keyword matching against categories in priority order
    for cat in CATEGORIES:
        for kw in cat["keywords"]:
            if kw.lower() in text:
                return cat

    # Default to developer resources
    return CATEGORIES[-1]

def build_markdown_catalog(repos):
    grouped = {cat["id"]: [] for cat in CATEGORIES}

    for r in repos:
        name = r.get("name", "")
        if name == USERNAME:
            continue  # Exclude the profile repo itself

        cat = classify_repo(r)
        cat_id = cat["id"]

        # Determine presentation details
        if name in CUSTOM_REPOS:
            c = CUSTOM_REPOS[name]
            desc = c["desc"]
            stack = c["stack"]
            badge_text = c["badge_text"]
            badge_color = c["badge_color"]
        else:
            raw_desc = r.get("description") or "Open source project."
            desc = f"⚡ {raw_desc}"
            stack = r.get("language") or "Multi-Stack"
            b_text, b_color = cat["default_badge"]
            badge_text = b_text
            badge_color = b_color

        url = f"https://github.com/{USERNAME}/{name}"
        badge_url = f"https://img.shields.io/badge/{badge_text.replace(' ', '%20')}-{badge_color}?style=flat-square"
        
        row = f"| [**{name}**]({url}) | {desc} | {stack} | ![{badge_text}]({badge_url}) |"
        grouped[cat_id].append(row)

    md_lines = []
    md_lines.append("## 🗂️ Curated Repository Catalog (व्यवस्थित रिपोजिटरी डायरेक्टरी)")
    md_lines.append("")
    md_lines.append("> *नीचे सभी उपयोगी रिपोजिटरीज़ को उनकी विशेषज्ञता और डोमेन के आधार पर 6 मुख्य श्रेणियों में व्यवस्थित किया गया है (Auto-Synced via GitHub Actions):*")
    md_lines.append("")

    for cat in CATEGORIES:
        cat_id = cat["id"]
        rows = grouped[cat_id]
        if not rows:
            continue
        md_lines.append(f"### {cat['title']}")
        md_lines.append("| Repository | Description & Highlights | Core Stack | Status |")
        md_lines.append("|---|---|---|:---:|")
        for row in rows:
            md_lines.append(row)
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")

    return "\n".join(md_lines)

def update_readme(readme_path, new_catalog_md):
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    start_tag = "<!-- AUTO-CATALOG:START -->"
    end_tag = "<!-- AUTO-CATALOG:END -->"

    if start_tag in content and end_tag in content:
        pattern = re.compile(rf"{re.escape(start_tag)}.*?{re.escape(end_tag)}", re.DOTALL)
        updated = pattern.sub(f"{start_tag}\n\n{new_catalog_md}\n\n{end_tag}", content)
    else:
        # Replace the existing section between header and Spotlight
        pattern = re.compile(r"## 🗂️ Curated Repository Catalog.*?(?=## 🎬 Featured Innovations Spotlight|## 🎬 Cloud Auto-Pilot Spotlight)", re.DOTALL)
        if pattern.search(content):
            updated = pattern.sub(f"{start_tag}\n\n{new_catalog_md}\n\n{end_tag}\n\n", content)
        else:
            print("Could not find insertion marker in README.md", file=sys.stderr)
            return False

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated)
    return True

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    readme_path = os.path.join(root_dir, "README.md")

    print(f"Fetching repositories for user '{USERNAME}'...")
    repos = fetch_repositories(USERNAME)
    print(f"Total repositories found: {len(repos)}")

    print("Generating catalog markdown...")
    catalog_md = build_markdown_catalog(repos)

    print("Updating README.md...")
    if update_readme(readme_path, catalog_md):
        print("Successfully updated README.md with categorized catalog!")
    else:
        print("Failed to update README.md.")
        sys.exit(1)

if __name__ == "__main__":
    main()
