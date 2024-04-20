"use client"
import Checklist from "@/components/Checklist";
import Transcript from "@/components/Transcript";
import { useEffect, useState } from "react";
import { ref } from "firebase/database";
import { database } from "@/firebase";
import { useObjectVal } from "react-firebase-hooks/database";

export default function Page() {
  const [sessionID, setSessionID] = useState<number>(1);
  const [value, loading, error] = useObjectVal(ref(database, '/'));
  const [transcription, setTranscription] = useState([]);
  const [checklist, setChecklist] = useState([]);

  useEffect(() => {
    if (value) {
      const sessions = value["Session"]
      const session = sessions[sessionID]
      setTranscription(session["Transcript"])
      setChecklist(session["Checklist"])
    }
  }, [value])

  return (
    <div className="flex h-full">
      <div className="flex flex-col gap-4 pt-4 pl-6 pr-10">
        <h2 className="inline-block text-xl sm:text-2xl font-bold text-slate-800">
          Session Transcriptition
        </h2>
        <Transcript transcript={transcription} />
        
      </div>

      <div className="flex gap-10">
        <div className="bg-gray-200 w-[1.5px] rounded-full" />

        <div className="flex flex-col gap-6 pt-4">
          <h2 className="inline-block text-xl sm:text-2xl font-bold text-slate-800">
            Prescription Patient Checklist
          </h2>
          <Checklist checklist={checklist} />
        </div>
      </div>
    </div>
  );

}