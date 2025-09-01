import { useRef, useState } from "react";
import {
  IonPage, IonHeader, IonToolbar, IonTitle,
  IonContent, IonList, IonItem, IonLabel, IonInput, IonButton
} from "@ionic/react";
import { stt, image } from "../api";

export default function Media() {
  const fileRef = useRef<HTMLInputElement | null>(null);
  const [transcript, setTranscript] = useState("");
  const [prompt, setPrompt] = useState("a cozy reading nook with warm light and stacks of vintage books");
  const [imgUrl, setImgUrl] = useState<string | null>(null);

  const onPick = () => fileRef.current?.click();

  const onFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (!f) return;
    try {
      const r = await stt(f);
      setTranscript(r.text);
    } catch (err: any) {
      alert(err.message || err.toString());
    }
  };

  const onGenerate = async () => {
    try {
      const url = await image(prompt);
      setImgUrl(url);
    } catch (err: any) {
      alert(err.message || err.toString());
    }
  };

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Smart Librarian — Media</IonTitle>
        </IonToolbar>
      </IonHeader>

      <IonContent className="ion-padding">
        <IonList>
          <h3>Speech → Text</h3>
          <input ref={fileRef} type="file" accept="audio/*" style={{ display: "none" }} onChange={onFile} />
          <IonButton onClick={onPick}>Upload audio</IonButton>
          <p><b>Transcript:</b> {transcript}</p>

          <h3>Text → Image</h3>
          <IonItem>
            <IonLabel position="stacked">Prompt</IonLabel>
            <IonInput value={prompt} onIonInput={(e) => setPrompt(String(e.detail.value))} />
          </IonItem>
          <IonButton onClick={onGenerate}>Generate image</IonButton>
          {imgUrl && <img src={imgUrl} alt="generated" style={{ width: "100%", marginTop: 12, borderRadius: 12 }} />}
        </IonList>
      </IonContent>
    </IonPage>
  );
}
