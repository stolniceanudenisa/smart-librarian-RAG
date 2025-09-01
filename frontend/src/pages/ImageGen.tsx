import { useState } from "react";
import {
  IonPage, IonHeader, IonToolbar, IonTitle,
  IonContent, IonItem, IonLabel, IonInput, IonButton
} from "@ionic/react";
import { image } from "../api";

export default function ImageGen() {
  const [prompt, setPrompt] = useState("a cozy reading nook with warm light and vintage books");
  const [url, setUrl] = useState<string | null>(null);

  const gen = async () => {
    const u = await image(prompt);
    setUrl(u);
  };

  return (
    <IonPage>
      <IonHeader className="app-header">
        <IonToolbar>
          <IonTitle className="container">Text → Image</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent className="container ion-padding">
        <IonItem>
          <IonLabel position="stacked">Prompt</IonLabel>
          <IonInput value={prompt} onIonInput={(e) => setPrompt(String(e.detail.value ?? ""))} />
        </IonItem>
        <IonButton onClick={gen} style={{ marginTop: 12 }}>Generate</IonButton>
        {url && <img src={url} alt="generated" style={{ width: "100%", borderRadius: 12, marginTop: 12 }} />}
      </IonContent>
    </IonPage>
  );
}
