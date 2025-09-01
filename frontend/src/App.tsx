import {
  IonApp,
  IonTabs,
  IonTabBar,
  IonTabButton,
  IonIcon,
  IonLabel,
  IonRouterOutlet,
} from "@ionic/react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { chatbubblesOutline, volumeHighOutline, micOutline, imagesOutline } from "ionicons/icons";
import Chat from "./pages/Chat";
import TTS from "./pages/TTS";
import STT from "./pages/STT";
import ImageGen from "./pages/ImageGen";
 

export default function App() {
  return (
    <IonApp>
      <BrowserRouter>
        <IonTabs>
          <IonRouterOutlet>
            <Routes>
              <Route path="/chat" element={<Chat />} />
              <Route path="/tts" element={<TTS />} />
              <Route path="/stt" element={<STT />} />
              <Route path="/image" element={<ImageGen />} />
              <Route path="*" element={<Navigate to="/chat" replace />} />
            </Routes>
          </IonRouterOutlet>

          <IonTabBar slot="bottom">
            <IonTabButton tab="chat" href="/chat">
              <IonIcon icon={chatbubblesOutline} />
              <IonLabel>Chat</IonLabel>
            </IonTabButton>
            <IonTabButton tab="tts" href="/tts">
              <IonIcon icon={volumeHighOutline} />
              <IonLabel>TTS</IonLabel>
            </IonTabButton>
            <IonTabButton tab="stt" href="/stt">
              <IonIcon icon={micOutline} />
              <IonLabel>STT</IonLabel>
            </IonTabButton>
            <IonTabButton tab="image" href="/image">
              <IonIcon icon={imagesOutline} />
              <IonLabel>Image</IonLabel>
            </IonTabButton>
          </IonTabBar>
        </IonTabs>
      </BrowserRouter>
    </IonApp>
  );
}
