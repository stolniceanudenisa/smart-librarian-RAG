const BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

export type ChatResponse = {
  title?: string;
  rationale?: string;
  full_summary?: string;
};

export async function chat(query: string): Promise<ChatResponse> {
  const r = await fetch(`${BASE}/chat/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function tts(text: string, voice?: string): Promise<HTMLAudioElement> {
  const r = await fetch(`${BASE}/media/tts`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, voice }),
  });
  if (!r.ok) throw new Error(await r.text());
  const blob = await r.blob();
  return new Audio(URL.createObjectURL(blob));
}

export async function stt(file: File): Promise<{ text: string }> {
  const fd = new FormData();
  fd.append("audio", file);
  const r = await fetch(`${BASE}/media/stt`, { method: "POST", body: fd });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function image(prompt: string, size = "1024x1024"): Promise<string> {
  const r = await fetch(`${BASE}/media/image`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt, size }),
  });
  if (!r.ok) throw new Error(await r.text());
  const blob = await r.blob();
  return URL.createObjectURL(blob);
}
