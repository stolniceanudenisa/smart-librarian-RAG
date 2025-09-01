import { useState } from "react";
import {
  IonPage, IonHeader, IonToolbar, IonTitle,
  IonContent, IonItem, IonLabel, IonInput, IonTextarea, IonButton
} from "@ionic/react";
import { tts } from "../api";

export default function TTS() {
  const [text, setText] = useState("Hello from Smart Librarian!");
  const [voice, setVoice] = useState("alloy");

  const play = async () => {
    const audio = await tts(text, voice);
    audio.play();
  };

  return (
    <IonPage>
      <IonHeader className="app-header">
        <IonToolbar>
          <IonTitle className="container">Text → Speech (TTS)</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent className="container ion-padding">
        <IonItem>
          <IonLabel position="stacked">Voice</IonLabel>
          <IonInput value={voice} onIonInput={(e) => setVoice(String(e.detail.value ?? ""))} />
        </IonItem>
        <IonItem>
          <IonLabel position="stacked">Text</IonLabel>
          <IonTextarea autoGrow value={text} onIonInput={(e) => setText(String(e.detail.value ?? ""))} />
        </IonItem>
        <IonButton onClick={play} style={{ marginTop: 12 }}>Play</IonButton>
      </IonContent>
    </IonPage>
  );
}
