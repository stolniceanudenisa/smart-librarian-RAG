import { useRef, useState } from "react";
import {
  IonPage, IonHeader, IonToolbar, IonTitle,
  IonContent, IonButton
} from "@ionic/react";
import { stt } from "../api";

export default function STT() {
  const fileRef = useRef<HTMLInputElement | null>(null);
  const [text, setText] = useState("");

  const pick = () => fileRef.current?.click();

  const onFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (!f) return;
    const r = await stt(f);
    setText(r.text);
  };

  return (
    <IonPage>
      <IonHeader className="app-header">
        <IonToolbar>
          <IonTitle className="container">Speech → Text (STT)</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent className="container ion-padding">
        <input type="file" ref={fileRef} style={{ display: "none" }} accept="audio/*" onChange={onFile} />
        <IonButton onClick={pick}>Upload audio</IonButton>
        <pre style={{ marginTop: 16, background: "var(--card)", padding: 12, borderRadius: 12 }}>
{text || "Transcript will appear here…"}
        </pre>
      </IonContent>
    </IonPage>
  );
}
