"""Engineering the Empire: a responsive career timeline web app.

Uses only Python's standard library. Routes:
  /        -> timeline UI
  /health  -> JSON health endpoint for Docker/Jenkins
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit
import json
import os

APP_VERSION = os.getenv("APP_VERSION", "v3")

MILESTONES = [
    {
        "date": "2017–2020",
        "year": "01",
        "title": "Mechanical Engineering — Diploma",
        "category": "FOUNDATION",
        "description": "Built the first engineering foundation through a Diploma in Mechanical Engineering at Quantum Global Campus.",
        "detail": "76.7% · Mechanical Engineering",
        "tags": ["Engineering", "Fundamentals"],
    },
    {
        "date": "2020–2023",
        "year": "02",
        "title": "B.Tech in Mechanical Engineering",
        "category": "EDUCATION",
        "description": "Completed a B.Tech at Kurukshetra University. The degree became a foundation—not a boundary—for the next chapter.",
        "detail": "CGPA 7.87 · Graduated 2023",
        "tags": ["Problem-solving", "Systems thinking"],
    },
    {
        "date": "2023–2024",
        "year": "03",
        "title": "Discipline, purpose & self-discovery",
        "category": "PERSONAL GROWTH",
        "description": "Explored structured spiritual practice and discipline through ISKCON training, learning consistency, service, and self-reflection.",
        "detail": "A chapter of inner work and clarity",
        "tags": ["Discipline", "Reflection"],
    },
    {
        "date": "2024",
        "year": "04",
        "title": "Acting, communication & performance",
        "category": "CREATIVE DEVELOPMENT",
        "description": "Invested in acting and performing arts, public speaking, personality development, and understanding human behaviour.",
        "detail": "Learning to communicate with confidence",
        "tags": ["Communication", "Creativity"],
    },
    {
        "date": "2023–2025",
        "year": "05",
        "title": "Business thinking & experimentation",
        "category": "EXPLORATION",
        "description": "Studied business fundamentals and explored startup ideas. Not every experiment produced an outcome, but each sharpened the questions worth pursuing.",
        "detail": "Learning through exploration—not claiming overnight success",
        "tags": ["Business", "Experimentation"],
    },
    {
        "date": "2025",
        "year": "06",
        "title": "Reset, job search & Python",
        "category": "TURNING POINT",
        "description": "After a difficult job-search period, began learning Python independently and worked toward a more technical, hands-on career direction.",
        "detail": "Start small. Build proof. Keep going.",
        "tags": ["Python", "Resilience"],
    },
    {
        "date": "2026",
        "year": "07",
        "title": "DevOps labs & CI/CD projects",
        "category": "TECHNICAL BUILDING",
        "description": "Practised Linux, Git, Docker, Jenkins, AWS, Kubernetes, Terraform, testing, container health checks, and image security scanning through guided labs and projects.",
        "detail": "Learning by building and documenting real work",
        "tags": ["Linux", "Docker", "Jenkins", "Cloud"],
    },
    {
        "date": "2026 →",
        "year": "08",
        "title": "Product Design Engineer — next chapter",
        "category": "PRESENT",
        "description": "Started a Product Design Engineer role at VVDN Technologies while continuing to evaluate how engineering, automation, and software skills can work together.",
        "detail": "The path is still being built",
        "tags": ["Engineering", "Automation", "Growth"],
    },
]

def render_timeline():
    """Return the complete responsive HTML page."""
    cards = []
    for item in MILESTONES:
        tags = "".join(f'<span class="tag">{tag}</span>' for tag in item["tags"])
        cards.append(
            f"""
            <article class="milestone">
              <div class="marker"><span>{item["year"]}</span></div>
              <div class="card">
                <div class="card-top">
                  <span class="category">{item["category"]}</span>
                  <span class="date">{item["date"]}</span>
                </div>
                <h3>{item["title"]}</h3>
                <p>{item["description"]}</p>
                <div class="detail">{item["detail"]}</div>
                <div class="tags">{tags}</div>
              </div>
            </article>
            """
        )

    timeline = "\n".join(cards)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#101113">
<meta name="description" content="Naresh Yadav's evolving career timeline: engineering, creative work, Python, DevOps projects, and product design.">
<title>Engineering the Empire — Naresh Yadav</title>
<style>
:root {{
  --bg: #f4f1eb; --ink: #191a1d; --muted: #66686e; --line: #d8d2c8;
  --orange: #ff6a00; --card: #fffdfa; --dark: #101113; --soft: #ece6dc;
}}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{ margin: 0; background: var(--bg); color: var(--ink); font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; line-height: 1.6; }}
a {{ color: inherit; }}
.hero {{ background: radial-gradient(ellipse at 78% 18%, rgba(255,106,0,.23), transparent 33%), var(--dark); color: #fff; padding: 28px 22px 76px; overflow: hidden; }}
.nav, .hero-inner, main, footer {{ max-width: 1040px; margin: 0 auto; }}
.nav {{ display: flex; align-items: center; justify-content: space-between; gap: 16px; }}
.brand {{ font-size: .82rem; letter-spacing: .16em; text-transform: uppercase; font-weight: 800; }}
.brand-mark {{ color: var(--orange); }}
.nav-pill {{ border: 1px solid #45464a; color: #d8d8da; border-radius: 99px; padding: 7px 12px; font-size: .75rem; }}
.hero-inner {{ padding-top: 68px; }}
.eyebrow {{ color: #ff9b55; font-size: .75rem; font-weight: 800; letter-spacing: .19em; text-transform: uppercase; }}
h1 {{ font-size: clamp(2.8rem, 8vw, 5.9rem); line-height: .98; letter-spacing: -.065em; max-width: 800px; margin: 18px 0 20px; }}
h1 em {{ color: var(--orange); font-style: normal; }}
.intro {{ max-width: 620px; color: #c8c8cb; font-size: clamp(1rem, 2.3vw, 1.18rem); }}
.hero-bottom {{ display: flex; align-items: center; flex-wrap: wrap; gap: 12px; margin-top: 30px; }}
.button {{ display: inline-flex; align-items: center; justify-content: center; border-radius: 8px; padding: 11px 16px; text-decoration: none; font-weight: 800; font-size: .9rem; }}
.button-primary {{ background: var(--orange); color: #161616; }}
.button-quiet {{ border: 1px solid #45464a; color: #fff; }}
main {{ padding: 0 22px 70px; }}
.overview {{ display: grid; grid-template-columns: repeat(3,1fr); gap: 12px; margin-top: -36px; position: relative; }}
.stat {{ background: var(--card); border: 1px solid #e5dfd5; padding: 18px; border-radius: 13px; box-shadow: 0 10px 26px rgba(24,20,12,.045); }}
.stat strong {{ display: block; font-size: 1.4rem; letter-spacing: -.04em; }}
.stat span {{ color: var(--muted); font-size: .78rem; }}
.section-head {{ display: flex; justify-content: space-between; align-items: end; gap: 20px; margin: 64px 0 28px; }}
.section-head h2 {{ margin: 0; font-size: clamp(1.8rem, 4vw, 2.7rem); letter-spacing: -.05em; line-height: 1.1; }}
.section-head p {{ color: var(--muted); margin: 8px 0 0; max-width: 460px; }}
.live-note {{ color: #7a4b2b; background: #ffeadb; border-radius: 8px; padding: 9px 12px; font-size: .78rem; font-weight: 750; white-space: nowrap; }}
.timeline {{ position: relative; max-width: 850px; margin: 0 auto; }}
.timeline::before {{ content: ""; position: absolute; top: 8px; bottom: 8px; left: 26px; width: 2px; background: linear-gradient(var(--orange), #d8d2c8 85%); }}
.milestone {{ display: grid; grid-template-columns: 54px 1fr; gap: 20px; position: relative; margin-bottom: 20px; }}
.marker {{ width: 54px; height: 54px; border-radius: 50%; background: var(--dark); border: 4px solid var(--bg); color: var(--orange); display: grid; place-items: center; z-index: 1; font-weight: 900; font-size: .72rem; box-shadow: 0 0 0 1px #d7d0c5; }}
.card {{ background: var(--card); border: 1px solid #e3ddd3; border-radius: 15px; padding: 22px 24px; transition: transform .18s ease, box-shadow .18s ease; }}
.card:hover {{ transform: translateY(-3px); box-shadow: 0 14px 32px rgba(24,20,12,.07); }}
.card-top {{ display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap; }}
.category {{ color: #b54b00; font-size: .68rem; letter-spacing: .13em; font-weight: 900; }}
.date {{ font-size: .8rem; color: var(--muted); font-weight: 700; }}
.card h3 {{ margin: 9px 0 8px; font-size: clamp(1.12rem, 2.5vw, 1.45rem); letter-spacing: -.035em; line-height: 1.25; }}
.card p {{ margin: 0; color: #56575d; }}
.detail {{ margin-top: 14px; border-left: 3px solid var(--orange); padding-left: 11px; font-size: .86rem; font-weight: 750; }}
.tags {{ display: flex; gap: 7px; flex-wrap: wrap; margin-top: 15px; }}
.tag {{ background: #f0ece5; color: #4c4a46; padding: 4px 9px; border-radius: 99px; font-size: .72rem; font-weight: 700; }}
.manifesto {{ margin: 64px 0 0; background: var(--dark); color: white; padding: clamp(24px, 5vw, 44px); border-radius: 18px; position: relative; overflow: hidden; }}
.manifesto::after {{ content: "∞"; position: absolute; right: 20px; bottom: -85px; font-size: 15rem; line-height: 1; color: rgba(255,106,0,.10); }}
.manifesto small {{ color: #ff9b55; text-transform: uppercase; letter-spacing: .16em; font-weight: 800; }}
.manifesto h2 {{ max-width: 680px; font-size: clamp(1.7rem, 4vw, 3rem); line-height: 1.12; letter-spacing: -.05em; margin: 14px 0; position: relative; z-index: 1; }}
.manifesto p {{ color: #c8c8cb; max-width: 600px; position: relative; z-index: 1; }}
footer {{ padding: 0 22px 34px; color: var(--muted); display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap; font-size: .8rem; }}
footer strong {{ color: var(--ink); }}
@media (max-width: 640px) {{
 .hero {{ padding-bottom: 64px; }} .hero-inner {{ padding-top: 50px; }}
 .overview {{ grid-template-columns: 1fr; margin-top: -28px; gap: 8px; }}
 .stat {{ padding: 13px 16px; display: flex; justify-content: space-between; align-items: center; }}
 .stat strong {{ font-size: 1.1rem; }} .section-head {{ display: block; margin-top: 48px; }}
 .live-note {{ display: inline-block; margin-top: 14px; white-space: normal; }}
 .timeline::before {{ left: 19px; }} .milestone {{ grid-template-columns: 40px 1fr; gap: 12px; }}
 .marker {{ width: 40px; height: 40px; border-width: 3px; font-size: .62rem; }}
 .card {{ padding: 17px; border-radius: 12px; }} .card-top {{ align-items: flex-start; }}
 .nav-pill {{ display: none; }} footer {{ display: block; }} footer span {{ display: block; margin-top: 5px; }}
}}
@media (prefers-reduced-motion: reduce) {{ html {{ scroll-behavior: auto; }} *, *::before, *::after {{ transition: none !important; }} }}
</style>
</head>
<body>
<header class="hero" id="top">
  <nav class="nav">
    <div class="brand"><span class="brand-mark">●</span> Engineering the Empire</div>
    <div class="nav-pill">A living career timeline · 2017—Now</div>
  </nav>
  <div class="hero-inner">
    <div class="eyebrow">The journey is the proof</div>
    <h1>Not a straight line.<br><em>A built life.</em></h1>
    <p class="intro">I'm Naresh Yadav. From mechanical engineering to creative exploration, Python, DevOps projects, and product design—this is a record of the work, the pivots, and the person I'm building along the way.</p>
    <div class="hero-bottom">
      <a class="button button-primary" href="#timeline">Explore the timeline ↓</a>
      <a class="button button-quiet" href="#principle">The principle</a>
    </div>
  </div>
</header>
<main>
  <section class="overview" aria-label="Timeline overview">
    <div class="stat"><strong>2017 → Now</strong><span>Still in progress</span></div>
    <div class="stat"><strong>Many chapters</strong><span>One evolving direction</span></div>
    <div class="stat"><strong>Build · Learn · Document</strong><span>The working philosophy</span></div>
  </section>
  <section id="timeline">
    <div class="section-head">
      <div>
        <h2>The chapters that<br>shaped the path.</h2>
        <p>Not every detour looks productive while you're in it. This timeline captures the learning, not a claim that every step was easy.</p>
      </div>
      <div class="live-note">IN PROGRESS — NOT THE FINISH LINE</div>
    </div>
    <div class="timeline">
      {timeline}
    </div>
  </section>
  <section class="manifesto" id="principle">
    <small>The principle</small>
    <h2>Build the person. Document the process. Teach the lesson. Build the brand. Eventually, build the company.</h2>
    <p>This timeline will change as the work changes. The goal isn't to pretend the path was perfect; it's to make progress visible, honest, and useful.</p>
  </section>
</main>
<footer>
  <strong>Naresh Yadav · Engineering the Empire</strong>
  <span>Built with Python's standard library · App {APP_VERSION}</span>
</footer>
</body>
</html>
"""


def route_response(path):
    """Return (status_code, content_type, response_body) for a URL path."""
    clean_path = urlsplit(path).path
    if clean_path in ("/", "/index.html"):
        return 200, "text/html; charset=utf-8", render_timeline()
    if clean_path == "/health":
        body = json.dumps({"status": "ok", "version": APP_VERSION})
        return 200, "application/json; charset=utf-8", body
    if clean_path == "/favicon.ico":
        return 204, "image/x-icon", ""
    return 404, "text/plain; charset=utf-8", "Not found"


class TimelineHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        status, content_type, body = route_response(self.path)
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(encoded)

    def log_message(self, fmt, *args):
        print("[http] %s - %s" % (self.address_string(), fmt % args))


def main():
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    server = HTTPServer((host, port), TimelineHandler)
    print(f"Engineering the Empire timeline running on http://{host}:{port} ({APP_VERSION})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

