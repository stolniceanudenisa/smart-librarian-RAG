import { useEffect, useRef, useState } from "react";
import {
  IonPage, IonHeader, IonToolbar, IonTitle,
  IonContent, IonInput, IonButton, IonItem, IonLabel
} from "@ionic/react";
import { chat, tts, type ChatResponse  } from "../api";

type Message = {
  id: string;
  role: "user" | "assistant";
  text: string;
  meta?: string;
};

const now = () => new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

export default function Chat() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([
    { id: crypto.randomUUID(), role: "assistant", text: "Hi! Tell me what kind of book you’re in the mood for.", meta: now() }
  ]);
  const [loading, setLoading] = useState(false);
  const [voice, setVoice] = useState("alloy");
  const listRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, loading]);

  const send = async () => {
    const q = input.trim();
    if (!q || loading) return;
    setInput("");

    const userMsg: Message = { id: crypto.randomUUID(), role: "user", text: q, meta: now() };
    setMessages((m) => [...m, userMsg]);
    setLoading(true);

    // optimistic typing indicator
    const typingId = crypto.randomUUID();
    setMessages((m) => [
      ...m,
      { id: typingId, role: "assistant", text: "typing", meta: "…" },
    ]);

    try {
      const r: ChatResponse = await chat(q);
      const answer = `${r.title ?? "Recommendation"}\n\n${r.rationale ?? ""}\n\n${r.full_summary ?? ""}`.trim();

      // replace typing bubble with real response
      setMessages((m) =>
        m.map(x => x.id === typingId ? { id: crypto.randomUUID(), role: "assistant", text: answer, meta: now() } : x)
      );
    } catch (e: any) {
      setMessages((m) =>
        m.map(x => x.id === typingId ? { id: crypto.randomUUID(), role: "assistant", text: `Error: ${e.message || e}`, meta: now() } : x)
      );
    } finally {
      setLoading(false);
    }
  };

  const listen = async () => {
    const last = [...messages].reverse().find(m => m.role === "assistant");
    if (!last) return;
    const audio = await tts(last.text, voice);
    audio.play();
  };

  return (
    <IonPage>
      <IonHeader className="app-header">
        <IonToolbar>
          <IonTitle className="container">Smart Librarian — Chat</IonTitle>
        </IonToolbar>
      </IonHeader>

      <IonContent fullscreen className="container">
        <div className="chat-card">
          <div className="messages" ref={listRef}>
            {messages.map((m) => (
              <div key={m.id} className={`msg-row ${m.role}`}>
                {m.role === "assistant" && <div className="avatar assistant">A</div>}
                <div className={`bubble ${m.role}`}>
                  {m.text === "typing" ? (
                    <div className="typing">
                      <span className="dot"></span>
                      <span className="dot"></span>
                      <span className="dot"></span>
                    </div>
                  ) : (
                    <div>{m.text}</div>
                  )}
                  <div className="meta">{m.meta}</div>
                </div>
                {m.role === "user" && <div className="avatar">U</div>}
              </div>
            ))}
          </div>

          <div className="input-bar">
            <div className="row">
              <IonInput
                value={input}
                placeholder="I want a book about friendship and magic"
                onIonInput={(e) => setInput(String(e.detail.value ?? ""))}
              />
              <IonButton className="send-btn" onClick={send} disabled={loading}>Send</IonButton>
            </div>

            <IonItem lines="none" style={{ marginTop: 8 }}>
              <IonLabel position="stacked">TTS Voice</IonLabel>
              <IonInput value={voice} onIonInput={(e) => setVoice(String(e.detail.value ?? "alloy"))} />
              <IonButton onClick={listen} style={{ marginLeft: 8 }}>Listen</IonButton>
            </IonItem>
          </div>
        </div>
      </IonContent>
    </IonPage>
  );
}
