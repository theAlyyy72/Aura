import { useState } from "react";
import {
  Home, MessageSquare, Mic, Wrench, Settings,
  Palette, LayoutDashboard, Sparkles, Send,
  Volume2, Activity, Cpu, Zap, Clock, Menu
} from "lucide-react";
import "./App.css";

const API = "http://127.0.0.1:8000";

function Orb() {
  return (
    <div className="orb-wrap">
      <div className="orb-halo" />
      <div className="orb">
        <div className="orb-core" />
        <div className="orb-shine" />
        <div className="orb-orbit orbit-one" />
        <div className="orb-orbit orbit-two" />
        <div className="orb-orbit orbit-three" />
      </div>
      <div className="orb-shadow" />
    </div>
  );
}

function VoiceRing({ listening }) {
  return (
    <div className={`ring-visual ${listening ? "listening" : ""}`}>
      <div className="ring-glow" />
      <div className="ring-circle ring-outer" />
      <div className="ring-circle ring-middle" />
      <div className="ring-circle ring-inner" />
      <div className="ring-center">
        <div className="ring-core" />
      </div>
      {Array.from({ length: 24 }).map((_, i) => (
        <span
          key={i}
          className="ring-dot"
          style={{ "--i": i }}
        />
      ))}
    </div>
  );
}

function App() {
  const [page, setPage] = useState("Home");
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [listening, setListening] = useState(false);
  const [loading, setLoading] = useState(false);
  const [accent, setAccent] = useState("#a855f7");

  const sendMessage = async (text = message) => {
    if (!text.trim() || loading) return;

    setMessages(prev => [...prev, { role: "user", text }]);
    setMessage("");
    setLoading(true);
    setPage("Chat");

    try {
      const response = await fetch(`${API}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
      });

      if (!response.ok) throw new Error("API request failed");

      const data = await response.json();

      setMessages(prev => [
        ...prev,
        { role: "assistant", text: data.reply || "No response received." }
      ]);
    } catch (error) {
      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          text: "I couldn't connect to AURA's backend. Please check that the Python API is running on port 8000."
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const startVoice = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Voice recognition is not supported in this browser.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;

    recognition.onstart = () => setListening(true);
    recognition.onend = () => setListening(false);

    recognition.onresult = (event) => {
      const spokenText = event.results[0][0].transcript;
      sendMessage(spokenText);
    };

    recognition.onerror = () => setListening(false);
    recognition.start();
  };

  const navItems = [
    { name: "Home", icon: Home },
    { name: "Chat", icon: MessageSquare },
    { name: "Voice", icon: Mic },
    { name: "Dashboard", icon: LayoutDashboard },
    { name: "Tools", icon: Wrench },
    { name: "Settings", icon: Settings }
  ];

  return (
    <div className="app" style={{ "--accent": accent }}>
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon"><Sparkles size={23} /></div>
          <span>AURA</span>
        </div>

        <div className="nav-label">WORKSPACE</div>

        <nav>
          {navItems.map(item => {
            const Icon = item.icon;
            return (
              <button
                key={item.name}
                className={`nav-item ${page === item.name ? "active" : ""}`}
                onClick={() => setPage(item.name)}
              >
                <Icon size={19} />
                <span>{item.name}</span>
              </button>
            );
          })}
        </nav>

        <div className="sidebar-bottom">
          <div className="system-mini">
            <span className="online-dot" />
            <span>All systems online</span>
          </div>
          <button className="nav-item" onClick={() => setPage("Settings")}>
            <Palette size={19} />
            <span>Customize</span>
          </button>
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <div className="top-left">
            <button className="mobile-menu"><Menu /></button>
            <div>
              <span className="eyebrow">YOUR PERSONAL AI</span>
              <h2>{page}</h2>
            </div>
          </div>
          <div className="top-right">
            <span className="status"><span className="online-dot" /> ONLINE</span>
            <div className="avatar">A</div>
          </div>
        </header>

        {page === "Home" && (
          <section className="home-page">
            <div className="welcome-row">
              <div>
                <span className="eyebrow">WELCOME TO YOUR UNIVERSE</span>
                <h1>Meet your intelligence.<br />
                  <span className="gradient-text">Meet AURA.</span>
                </h1>
                <p>Your AI companion. Your world. Your intelligence.</p>
              </div>
              <div className="home-orb"><Orb /></div>
            </div>

            <div className="home-grid">
              <div className="glass-card home-card">
                <div className="card-heading">
                  <div>
                    <span className="eyebrow">YOUR WORKSPACE</span>
                    <h3>Explore AURA</h3>
                  </div>
                  <Sparkles className="purple-icon" />
                </div>

                <div className="feature-grid">
                  <button className="feature-card" onClick={() => setPage("Chat")}>
                    <MessageSquare />
                    <strong>AI Chat</strong>
                    <span>Talk with your AI</span>
                  </button>
                  <button className="feature-card" onClick={() => setPage("Voice")}>
                    <Mic />
                    <strong>Voice Command</strong>
                    <span>Speak with AURA</span>
                  </button>
                  <button className="feature-card" onClick={() => setPage("Dashboard")}>
                    <Activity />
                    <strong>Analytics</strong>
                    <span>Explore system activity</span>
                  </button>
                  <button className="feature-card" onClick={() => setPage("Tools")}>
                    <Zap />
                    <strong>AI Tools</strong>
                    <span>Your smart toolkit</span>
                  </button>
                </div>
              </div>

              <div className="glass-card ring-card">
                <div className="card-heading">
                  <div>
                    <span className="eyebrow">VOICE INTERFACE</span>
                    <h3>The Ring</h3>
                  </div>
                  <span className="live-tag">LIVE</span>
                </div>
                <VoiceRing listening={listening} />
                <h2 className="ring-title">AURA VOICE</h2>
                <p className="muted">
                  {listening ? "Listening to your voice..." : "Your voice. Your command."}
                </p>
                <button className="voice-button" onClick={startVoice}>
                  <Mic size={20} />
                  {listening ? "Listening..." : "Start talking"}
                </button>
              </div>
            </div>

            <div className="bottom-note">
              <span className="online-dot" /> AURA CORE IS READY
              <span>POWERED BY YOUR AI ENGINE</span>
            </div>
          </section>
        )}

        {page === "Voice" && (
          <section className="voice-page glass-card">
            <span className="eyebrow">REAL-TIME VOICE INTERFACE</span>
            <h1>Enter the <span className="gradient-text">Ring.</span></h1>
            <p className="muted">Talk naturally with your personal AI assistant.</p>
            <VoiceRing listening={listening} />
            <h2>{listening ? "LISTENING..." : "AURA IS READY"}</h2>
            <p className="muted">Press the microphone to begin</p>
            <button className="voice-button large" onClick={startVoice}>
              <Mic /> {listening ? "Listening..." : "Activate Voice"}
            </button>
          </section>
        )}

        {page === "Chat" && (
          <section className="chat-page glass-card">
            <div className="chat-heading">
              <div>
                <span className="eyebrow">AURA INTELLIGENCE</span>
                <h1>Ask AURA anything.</h1>
              </div>
              <Sparkles className="purple-icon" size={28} />
            </div>

            <div className="chat-messages">
              {messages.length === 0 && (
                <div className="empty-chat">
                  <Orb />
                  <h2>How can I help you today?</h2>
                  <p className="muted">Ask a question or give AURA a command.</p>
                </div>
              )}

              {messages.map((msg, i) => (
                <div key={i} className={`message ${msg.role}`}>
                  <div className="message-avatar">
                    {msg.role === "user" ? "Y" : <Sparkles size={17} />}
                  </div>
                  <div className="message-text">{msg.text}</div>
                </div>
              ))}
              {loading && <div className="loading-text">AURA is thinking...</div>}
            </div>

            <form className="chat-input" onSubmit={e => {
              e.preventDefault();
              sendMessage();
            }}>
              <input
                value={message}
                onChange={e => setMessage(e.target.value)}
                placeholder="Message AURA..."
              />
              <button type="button" className="input-icon" onClick={startVoice}>
                <Mic />
              </button>
              <button type="submit" className="send-button" disabled={loading}>
                <Send size={19} />
              </button>
            </form>
          </section>
        )}

        {page === "Dashboard" && (
          <section className="dashboard-page">
            <div className="page-intro">
              <span className="eyebrow">SYSTEM OVERVIEW</span>
              <h1>Your <span className="gradient-text">Dashboard.</span></h1>
            </div>
            <div className="stats-grid">
              <Stat icon={Activity} title="AI Status" value="ONLINE" />
              <Stat icon={MessageSquare} title="Conversations" value={messages.length.toString()} />
              <Stat icon={Cpu} title="Core Engine" value="ACTIVE" />
              <Stat icon={Zap} title="Response Mode" value="READY" />
            </div>
            <div className="glass-card dashboard-info">
              <h3><Activity size={20} /> System Activity</h3>
              <div className="activity-bars">
                {[40, 65, 48, 80, 56, 92, 68, 75, 50, 88, 64, 95].map((v, i) =>
                  <div key={i} style={{ height: `${v}%` }} />
                )}
              </div>
              <p className="muted">Visual system activity preview</p>
            </div>
          </section>
        )}

        {page === "Tools" && (
          <section className="dashboard-page">
            <div className="page-intro">
              <span className="eyebrow">YOUR AI TOOLKIT</span>
              <h1>Smart <span className="gradient-text">Tools.</span></h1>
            </div>
            <div className="feature-grid tools-grid">
              {["Web Search", "App Control", "File Assistant", "System Commands"].map((tool, i) => (
                <div className="glass-card tool-card" key={tool}>
                  <Wrench />
                  <h3>{tool}</h3>
                  <p className="muted">Connect your AURA tools and capabilities.</p>
                  <span className="live-tag">TOOL {i + 1}</span>
                </div>
              ))}
            </div>
          </section>
        )}

        {page === "Settings" && (
          <section className="dashboard-page">
            <div className="page-intro">
              <span className="eyebrow">PERSONALIZE YOUR EXPERIENCE</span>
              <h1>AURA <span className="gradient-text">Settings.</span></h1>
            </div>
            <div className="glass-card settings-card">
              <h3><Palette /> Accent colour</h3>
              <p className="muted">Choose your interface glow colour.</p>
              <div className="color-options">
                {["#a855f7", "#168bff", "#00d6b4", "#ff4c9a", "#e6a23c"].map(color =>
                  <button
                    key={color}
                    className={`color-choice ${accent === color ? "selected" : ""}`}
                    style={{ background: color }}
                    onClick={() => setAccent(color)}
                  />
                )}
              </div>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

function Stat({ icon: Icon, title, value }) {
  return (
    <div className="glass-card stat-card">
      <Icon size={23} />
      <span className="muted">{title}</span>
      <strong>{value}</strong>
    </div>
  );
}

export default App;